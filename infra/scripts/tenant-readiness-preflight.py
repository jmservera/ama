#!/usr/bin/env python3
"""Read-only tenant readiness preflight for the Zava Forward API's Entra sign-in prerequisites.

Inspects, with the Azure CLI session that is already signed in, whether the deployed API's
audience is a real Entra application (a UUID, not the literal systemAssignedIdentity), whether
the single-tenant registration, the manifest app-role contract and the required callback can be
read, and whether an edge callback has the forward-proxy configuration it needs.

Read-only boundary:
* Only exact built-in Azure CLI templates run: account show, containerapp show,
  containerapp auth show and Graph GET lookups with fixed $select lists. Nothing logs in,
  writes, resets credentials, reads secret values, lists role assignments or reads staff.
* Output is a closed schema of check ids, statuses, fixed reason codes, booleans, counts and
  contract role keys. Tenant, client and object identifiers stay in memory and are never printed.
* Statuses: ready, absent (Graph answered with no match), denied (permission refused),
  unknown (not inspectable or not signed in), mismatch (read but different), not-applicable.
  Any status other than ready or not-applicable is a human blocker; exit code 1.
  A clean report is a prerequisite signal only: it does not establish tenant setup, credential
  delivery, staff binding, sign-in, or any #349 acceptance criterion. Tenant authority remains
  a human decision; this tool never grants, creates or changes anything.

Example:
  python3 infra/scripts/tenant-readiness-preflight.py -g <resource-group> -n <api-app> \\
      [--public-url https://<edge-host>] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

MANIFEST = Path(__file__).resolve().parents[1] / "entra" / "app-registration.json"
GRAPH = "https://graph.microsoft.com/v1.0"
ROLE_PREFIX = "ZavaForward."
BLOCKING = {"absent", "denied", "unknown", "mismatch"}
NAME = re.compile(r"[A-Za-z0-9._()-]{1,90}")
ROLE_KEY = re.compile(r"ZavaForward\.[A-Za-z]{1,40}")
LABEL = r"(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
APP_SELECT = "appId,signInAudience,identifierUris,web,api,appRoles"
SP_SELECT = "appRoleAssignmentRequired"
ACCOUNT_ARGV = ["account", "show", "--query", "{tenantId:tenantId}"]
FQDN_QUERY = "{fqdn:properties.configuration.ingress.fqdn}"
AUTH_QUERY = (
    "{enabled:platform.enabled,"
    "clientId:identityProviders.azureActiveDirectory.registration.clientId,"
    "issuer:identityProviders.azureActiveDirectory.registration.openIdIssuer,"
    "secretSet:identityProviders.azureActiveDirectory.registration.clientSecretSettingName!=null,"
    "audiences:identityProviders.azureActiveDirectory.validation.allowedAudiences,"
    "proxy:httpSettings.forwardProxy.convention,"
    "proxyHost:httpSettings.forwardProxy.customHostHeaderName,"
    "proxyProto:httpSettings.forwardProxy.customProtoHeaderName}"
)
GRAPH_URL = re.compile(
    re.escape(GRAPH) + r"/(applications|servicePrincipals)\?\$filter=appId eq '[0-9a-f-]{36}'"
    r"&\$select=([A-Za-z,]+)"
)
ALLOWED_SELECTS = {APP_SELECT, SP_SELECT}
CAPABILITY_URL = f"{GRAPH}/applications?$top=1&$select=appId"

Transport = Callable[[list[str]], tuple[int, str, str]]


class ReadOnlyViolation(ValueError):
    """Raised before execution when a call is not an exact built-in read-only template."""


def guard(argv: list[str]) -> None:
    """Accept only the checker's own fixed read-only command templates."""
    if not all(isinstance(token, str) for token in argv):
        raise ReadOnlyViolation("non-string argument")
    if argv == ACCOUNT_ARGV:
        return
    if (
        len(argv) == 8
        and argv[0] == "containerapp"
        and argv[2:3] == ["-g"]
        and argv[4:5] == ["-n"]
        and argv[6] == "--query"
        and NAME.fullmatch(argv[3])
        and NAME.fullmatch(argv[5])
        and (argv[1], argv[7]) in {("show", FQDN_QUERY)}
    ):
        return
    if (
        len(argv) == 9
        and argv[:3] == ["containerapp", "auth", "show"]
        and argv[3:4] == ["-g"]
        and argv[5:6] == ["-n"]
        and argv[7] == "--query"
        and argv[8] == AUTH_QUERY
        and NAME.fullmatch(argv[4])
        and NAME.fullmatch(argv[6])
    ):
        return
    if len(argv) == 5 and argv[:4] == ["rest", "--method", "GET", "--url"]:
        found = GRAPH_URL.fullmatch(argv[4])
        if argv[4] == CAPABILITY_URL or (found and found.group(2) in ALLOWED_SELECTS):
            return
    raise ReadOnlyViolation("call is not an allowed read-only template")


def az_transport(argv: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        ["az", *argv, "--output", "json"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout, result.stderr


def classify(returncode: int, stderr: str) -> tuple[str, str]:
    """Map a failure to a status and fixed reason without echoing service text."""
    text = stderr.lower()
    if any(
        k in text
        for k in (
            "forbidden",
            "authorization_requestdenied",
            "authorizationfailed",
            "insufficient privileges",
            "403",
        )
    ):
        return "denied", "permission-denied"
    if "az login" in text or "not logged in" in text or "no subscription" in text:
        return "unknown", "not-signed-in"
    if any(k in text for k in ("notfound", "not found", "could not be found")):
        return "absent", "not-found"
    return "unknown", "call-failed"


class Finding:
    def __init__(
        self, check: str, status: str, reason: str, facts: dict[str, Any] | None = None
    ) -> None:
        self.check, self.status, self.reason, self.facts = check, status, reason, facts or {}
        for value in self.facts.values():
            safe = isinstance(value, (bool, int)) or (
                isinstance(value, list) and all(ROLE_KEY.fullmatch(v) for v in value)
            )
            if not safe:
                raise ValueError("report facts are limited to booleans, counts and role keys")


class Call:
    """Outcome of one guarded read."""

    def __init__(self, status: str, reason: str, data: Any = None) -> None:
        self.status, self.reason, self.data = status, reason, data


class Az:
    def __init__(self, transport: Transport = az_transport) -> None:
        self._transport = transport

    def read(self, argv: list[str]) -> Call:
        guard(argv)
        try:
            code, out, err = self._transport(argv)
        except FileNotFoundError:
            return Call("unknown", "azure-cli-unavailable")
        except subprocess.TimeoutExpired:
            return Call("unknown", "timeout")
        except OSError:
            return Call("unknown", "call-failed")
        if code:
            return Call(*classify(code, err))
        try:
            return Call("ready", "read", json.loads(out))
        except ValueError:
            return Call("unknown", "malformed-response")


def valid_host(host: str) -> bool:
    return (
        isinstance(host, str)
        and len(host) <= 253
        and "." in host
        and all(re.fullmatch(LABEL, part) for part in host.split("."))
    )


def public_host(url: str) -> str | None:
    from urllib.parse import urlsplit

    try:
        parsed = urlsplit(url)
        host = parsed.hostname or ""
        port = parsed.port
    except ValueError:
        return None
    if (
        parsed.scheme != "https"
        or parsed.netloc != host
        or port is not None
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
        or not valid_host(host)
    ):
        return None
    return host


def as_uuid(value: object) -> str | None:
    if not isinstance(value, str) or not re.fullmatch(
        r"[0-9A-Fa-f]{8}(-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}", value
    ):
        return None
    try:
        return str(uuid.UUID(value))
    except ValueError:
        return None


def load_contract(manifest: Path) -> dict[str, Any]:
    data = json.loads(manifest.read_text(encoding="utf-8"))
    return {
        "roles": sorted(
            ROLE_PREFIX + r["key"] for r in [*data["appRoles"], *data["capabilityRoles"]]
        ),
        "audience": data["signInAudience"],
        "assignment_required": data["appRoleAssignmentRequired"],
        "callback_path": data["callbackPath"],
        "token_version": data["requestedAccessTokenVersion"],
    }


def role_contract(actual: object, expected: list[str]) -> Finding:
    roles = [r for r in actual if isinstance(r, dict)] if isinstance(actual, list) else []
    values = [r.get("value") for r in roles]
    missing = [v for v in expected if v not in values]
    duplicate = sorted({v for v in values if v in expected and values.count(v) > 1})
    present = [r for r in roles if r.get("value") in expected]
    disabled = sorted({r["value"] for r in present if r.get("isEnabled") is not True})
    wrong = sorted(
        {
            r["value"]
            for r in present
            if not isinstance(r.get("allowedMemberTypes"), list)
            or "User" not in r["allowedMemberTypes"]
        }
    )
    extra = [
        v for v in values if isinstance(v, str) and v.startswith(ROLE_PREFIX) and v not in expected
    ]
    facts = {
        "expected": len(expected),
        "missing": missing,
        "disabled": disabled,
        "wrong_member_type": wrong,
        "duplicate": duplicate,
        "extra": len(extra),
    }
    clean = not (missing or disabled or wrong or duplicate or extra)
    return Finding(
        "graph-app-roles",
        "ready" if clean else "mismatch",
        "role-contract-met" if clean else "role-contract-mismatch",
        facts,
    )


def run(
    az: Az, group: str, app: str, contract: dict[str, Any], public_url: str | None
) -> list[Finding]:
    out: list[Finding] = []

    def add(check: str, status: str, reason: str, **facts: Any) -> Finding:
        finding = Finding(check, status, reason, facts)
        out.append(finding)
        return finding

    def failed(check: str, call: Call) -> Finding:
        return add(check, call.status, call.reason)

    session = az.read(ACCOUNT_ARGV)
    tenant = (
        as_uuid(session.data.get("tenantId"))
        if session.status == "ready" and isinstance(session.data, dict)
        else None
    )
    if session.status != "ready":
        failed("az-session", session)
    else:
        add(
            "az-session",
            "ready" if tenant else "unknown",
            "tenant-resolved" if tenant else "tenant-unreadable",
        )

    fqdn_call = az.read(["containerapp", "show", "-g", group, "-n", app, "--query", FQDN_QUERY])
    fqdn = (
        fqdn_call.data.get("fqdn")
        if fqdn_call.status == "ready" and isinstance(fqdn_call.data, dict)
        else None
    )
    if fqdn_call.status != "ready":
        failed("api-ingress", fqdn_call)
    elif fqdn is None:
        add("api-ingress", "absent", "ingress-fqdn-absent")
    else:
        ok = valid_host(fqdn)
        add(
            "api-ingress",
            "ready" if ok else "mismatch",
            "ingress-fqdn-valid" if ok else "ingress-fqdn-invalid",
        )
        fqdn = fqdn if ok else None

    auth_call = az.read(
        ["containerapp", "auth", "show", "-g", group, "-n", app, "--query", AUTH_QUERY]
    )
    auth = (
        auth_call.data if auth_call.status == "ready" and isinstance(auth_call.data, dict) else {}
    )
    client = None
    if auth_call.status != "ready":
        for check in (
            "api-auth-enabled",
            "api-audience",
            "api-audience-allowed",
            "api-credential-setting",
            "api-issuer-tenant",
        ):
            failed(check, auth_call)
    else:
        enabled = auth.get("enabled") is True
        add(
            "api-auth-enabled",
            "ready" if enabled else "mismatch",
            "auth-enabled" if enabled else "auth-disabled",
        )
        raw = auth.get("clientId")
        client = as_uuid(raw)
        if client:
            add("api-audience", "ready", "uuid")
        elif raw is None or raw == "":
            add("api-audience", "absent", "audience-absent")
        elif isinstance(raw, str) and raw == "systemAssignedIdentity":
            add("api-audience", "mismatch", "system-assigned-identity-literal")
        else:
            add("api-audience", "mismatch", "audience-invalid")
        if client:
            allowed = {a.strip().lower() for a in auth.get("audiences") or [] if isinstance(a, str)}
            ok = client in allowed or f"api://{client}" in allowed
            add(
                "api-audience-allowed",
                "ready" if ok else "mismatch",
                "audience-allowed" if ok else "audience-not-allowed",
                count=len(allowed),
            )
        else:
            add("api-audience-allowed", "unknown", "blocked-by-api-audience")
        if auth.get("secretSet") is True:
            add("api-credential-setting", "ready", "credential-setting-present")
        else:
            add("api-credential-setting", "absent", "credential-setting-absent")
        issuer = auth.get("issuer")
        issuer_tenant = None
        if isinstance(issuer, str):
            found = re.search(r"login\.microsoftonline\.com/([0-9a-fA-F-]{36})/", issuer)
            issuer_tenant = as_uuid(found.group(1)) if found else None
        if tenant and issuer_tenant:
            same = tenant == issuer_tenant
            add(
                "api-issuer-tenant",
                "ready" if same else "mismatch",
                "issuer-matches-signed-in-tenant"
                if same
                else "issuer-differs-from-signed-in-tenant",
            )
        else:
            add("api-issuer-tenant", "unknown", "issuer-or-tenant-unreadable")

    host = public_host(public_url) if public_url else fqdn
    if public_url and host is None:
        add("callback-target", "mismatch", "public-url-invalid")
    elif host is None:
        add("callback-target", "unknown", "callback-host-unavailable")
    else:
        add("callback-target", "ready", "callback-target-derived")
    callback = f"https://{host}{contract['callback_path']}" if host else None

    if host and fqdn and host != fqdn:
        proxy_ok = (
            auth.get("proxy") == "Custom"
            and auth.get("proxyHost") == "X-Forwarded-Host"
            and auth.get("proxyProto") == "X-Forwarded-Proto"
        )
        add(
            "edge-forward-proxy",
            "ready" if proxy_ok else "mismatch",
            "forward-proxy-configured" if proxy_ok else "forward-proxy-required",
        )
    elif host and fqdn:
        add("edge-forward-proxy", "not-applicable", "callback-host-is-ingress-fqdn")
    else:
        add("edge-forward-proxy", "unknown", "blocked-by-callback-target")

    probe = az.read(["rest", "--method", "GET", "--url", CAPABILITY_URL])
    if probe.status == "ready":
        listed = isinstance(probe.data, dict) and isinstance(probe.data.get("value"), list)
        add(
            "graph-read-capability",
            "ready" if listed else "unknown",
            "application-lookup-readable" if listed else "malformed-response",
        )
    else:
        failed("graph-read-capability", probe)

    graph_checks = (
        "graph-sign-in-audience",
        "graph-identifier-uri",
        "graph-token-version",
        "graph-app-roles",
        "graph-callback",
        "graph-service-principal",
    )
    if client is None:
        add("graph-application", "unknown", "blocked-by-api-audience")
        for check in graph_checks:
            add(check, "unknown", "blocked-by-api-audience")
        return out

    app_call = az.read(
        [
            "rest",
            "--method",
            "GET",
            "--url",
            f"{GRAPH}/applications?$filter=appId eq '{client}'&$select={APP_SELECT}",
        ]
    )
    values = (
        app_call.data.get("value")
        if app_call.status == "ready" and isinstance(app_call.data, dict)
        else None
    )
    registration = (
        values[0] if isinstance(values, list) and values and isinstance(values[0], dict) else None
    )
    if app_call.status != "ready" or registration is None:
        if app_call.status == "ready":
            add(
                "graph-application",
                "absent" if isinstance(values, list) else "unknown",
                "registration-not-found" if isinstance(values, list) else "malformed-response",
            )
        else:
            failed("graph-application", app_call)
        for check in graph_checks:
            add(check, "unknown", "blocked-by-graph-application")
        return out
    add("graph-application", "ready", "registration-read")
    ok = registration.get("signInAudience") == contract["audience"]
    add(
        "graph-sign-in-audience",
        "ready" if ok else "mismatch",
        "single-tenant" if ok else "not-single-tenant",
    )
    ok = f"api://{client}" in [
        u.lower() for u in registration.get("identifierUris") or [] if isinstance(u, str)
    ]
    add(
        "graph-identifier-uri",
        "ready" if ok else "mismatch",
        "identifier-uri-present" if ok else "identifier-uri-missing",
    )
    api = registration.get("api") if isinstance(registration.get("api"), dict) else {}
    ok = api.get("requestedAccessTokenVersion") == contract["token_version"]
    add(
        "graph-token-version",
        "ready" if ok else "mismatch",
        "token-version-expected" if ok else "token-version-differs",
    )
    finding = role_contract(registration.get("appRoles"), contract["roles"])
    out.append(finding)
    web = registration.get("web") if isinstance(registration.get("web"), dict) else {}
    redirects = [r for r in web.get("redirectUris") or [] if isinstance(r, str)]
    if callback is None:
        add("graph-callback", "unknown", "blocked-by-callback-target")
    else:
        present = callback in redirects
        add(
            "graph-callback",
            "ready" if present else "absent",
            "callback-present" if present else "callback-missing",
            registered=len(redirects),
        )

    sp_call = az.read(
        [
            "rest",
            "--method",
            "GET",
            "--url",
            f"{GRAPH}/servicePrincipals?$filter=appId eq '{client}'&$select={SP_SELECT}",
        ]
    )
    sp_values = (
        sp_call.data.get("value")
        if sp_call.status == "ready" and isinstance(sp_call.data, dict)
        else None
    )
    if sp_call.status != "ready":
        failed("graph-service-principal", sp_call)
    elif not isinstance(sp_values, list) or not sp_values or not isinstance(sp_values[0], dict):
        add("graph-service-principal", "absent", "service-principal-not-found")
    else:
        required = sp_values[0].get("appRoleAssignmentRequired") is contract["assignment_required"]
        add(
            "graph-service-principal",
            "ready" if required else "mismatch",
            "assignment-required" if required else "assignment-requirement-differs",
        )
    return out


def overall(findings: list[Finding]) -> str:
    return "blocked" if any(f.status in BLOCKING for f in findings) else "ready"


def render(findings: list[Finding], as_json: bool) -> str:
    state = overall(findings)
    if as_json:
        return json.dumps(
            {
                "schema": 1,
                "readOnly": True,
                "overall": state,
                "acceptanceEstablished": False,
                "checks": [
                    {"check": f.check, "status": f.status, "reason": f.reason, "facts": f.facts}
                    for f in findings
                ],
            },
            indent=2,
        )
    lines = ["Tenant readiness preflight (read-only; identifiers are never printed)"]
    for f in findings:
        facts = " ".join(f"{k}={v}" for k, v in f.facts.items())
        lines.append(f"{f.status:<16}{f.check:<26}{f.reason}" + (f"  {facts}" if facts else ""))
    blockers = sum(f.status in BLOCKING for f in findings)
    lines.append(f"Overall: {state} ({blockers} non-ready check(s)).")
    lines.append(
        "Acceptance: not established. Tenant setup, credential delivery, staff binding and "
        "real-user sign-in remain human-gated; this tool changes nothing."
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None, transport: Transport = az_transport) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-g", "--resource-group", required=True, help="API resource group name")
    parser.add_argument("-n", "--app", required=True, help="API Container App name")
    parser.add_argument(
        "--public-url", help="optional public HTTPS origin (edge) whose callback is required"
    )
    parser.add_argument(
        "--manifest", type=Path, default=MANIFEST, help="app registration contract manifest"
    )
    parser.add_argument("--json", action="store_true", help="emit the closed JSON report")
    args = parser.parse_args(argv)
    for value in (args.resource_group, args.app):
        if not NAME.fullmatch(value):
            parser.error("resource group and app names must be plain Azure resource names")
    try:
        contract = load_contract(args.manifest)
    except (OSError, ValueError, KeyError, TypeError):
        parser.error("the contract manifest could not be read")
    findings = run(Az(transport), args.resource_group, args.app, contract, args.public_url)
    print(render(findings, args.json))
    return 0 if overall(findings) == "ready" else 1


if __name__ == "__main__":
    sys.exit(main())
