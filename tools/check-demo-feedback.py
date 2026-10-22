"""Offline checker for the minimum owner-feedback prerequisites (Refs #350).

Reads one explicitly supplied JSON evidence bundle and reports pass, fail,
blocked or not-run per check. It performs no network access, reads no
environment credentials, submits no writes and never activates AI. Evidence
is shaped like the real runtime responses; runtime schemas are imported from
the installed zava_forward packages rather than copied.

This is an offline harness, not deployed acceptance. A redirect, an auth
denial or the existence of a source asset is never a functional success, and
the overall verdict can never be pass in this slice: spend-bound and
fixed-administrator evidence have no runtime field and stay not-run.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

SCHEMA_VERSION = 1
MAX_EVIDENCE_BYTES = 1 << 20
DEFAULT_PROGRAMME_CASES = 980
STOCK_HOMES = 60000
PASS, FAIL, BLOCKED, NOT_RUN = "pass", "fail", "blocked", "not-run"
ORIGINS = ("synthetic-fixture", "deployed-capture")
TOP_KEYS = {"schema_version", "origin", "image", "me", "programme", "case_write", "ai"}
CHECKS = (
    "image_identity",
    "me_contract",
    "case_write_reload",
    "ai_evidence",
    "baseline_distinction",
)
GAPS = {
    "spend_bound": "No runtime field exists for a spend bound; evidence needs the deployed environment (#349, #360).",
    "admin_account": "No runtime field exists for the fixed administrator account; needs real tenant and staff (#349).",
}
EXIT_CODES = {FAIL: 1, BLOCKED: 2, NOT_RUN: 3}
IMAGE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*@(sha256:[0-9a-f]{64})$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
ME_KEYS = {"user", "counts", "staff", "account", "map", "navigation"}
ENDPOINT_NAMES = {
    "me": "/api/me",
    "programme": "/api/cases?view=all",
    "ai": "POST /api/ai/priority",
}


class Verdict(Exception):
    """Internal early exit carrying a check status and its reason."""

    def __init__(self, status, reason):
        super().__init__(reason)
        self.status = status
        self.reason = reason


def load_runtime():
    try:
        from zava_forward.api.workbench import navigation
        from zava_forward.core import projection, ranking, taskqueues
        from zava_forward.core.store import Store
    except ImportError as error:
        raise Verdict(
            BLOCKED,
            f"Installed zava_forward packages are unavailable ({error}); pip install src/core src/agents src/api.",
        ) from error
    return SimpleNamespace(
        projection=projection,
        ranking=ranking,
        taskqueues=taskqueues,
        navigation=navigation,
        rec_label=Store.REC_LABEL,
    )


def load_evidence(path):
    target = Path(path)
    if not target.is_file():
        raise Verdict(BLOCKED, f"Evidence file {path} is not a regular file.")
    try:
        size = target.stat().st_size
        if size > MAX_EVIDENCE_BYTES:
            raise Verdict(
                BLOCKED,
                f"Evidence file is {size} bytes; the limit is {MAX_EVIDENCE_BYTES}.",
            )
        text = target.read_bytes().decode("utf-8")
        data = json.loads(text)
    except OSError as error:
        raise Verdict(
            BLOCKED, f"Evidence file cannot be read: {error.strerror}."
        ) from error
    except UnicodeDecodeError as error:
        raise Verdict(BLOCKED, "Evidence file is not valid UTF-8.") from error
    except json.JSONDecodeError as error:
        raise Verdict(
            BLOCKED, f"Evidence file is not valid JSON: {error.msg}."
        ) from error
    if not isinstance(data, dict):
        raise Verdict(BLOCKED, "Evidence must be a JSON object.")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise Verdict(BLOCKED, f"Evidence schema_version must be {SCHEMA_VERSION}.")
    if data.get("origin") not in ORIGINS:
        raise Verdict(BLOCKED, f"Evidence origin must be one of {', '.join(ORIGINS)}.")
    unknown = sorted(set(data) - TOP_KEYS)
    if unknown:
        raise Verdict(
            BLOCKED, f"Evidence has unknown top-level keys: {', '.join(unknown)}."
        )
    return data


def response_body(slot, label):
    """Return the body of an authorised 200 response, or end the check."""
    if (
        not isinstance(slot, dict)
        or isinstance(slot.get("status"), bool)
        or not isinstance(slot.get("status"), int)
    ):
        raise Verdict(BLOCKED, f"{label} evidence needs an integer status and a body.")
    status = slot["status"]
    if 300 <= status < 400:
        raise Verdict(
            FAIL,
            f"{label} returned redirect {status}; a redirect is not an authorized functional success.",
        )
    if status in (401, 403):
        raise Verdict(
            FAIL,
            f"{label} returned {status}; an auth denial is not an authorized functional success.",
        )
    if status != 200:
        raise Verdict(FAIL, f"{label} returned status {status}, not 200.")
    if "body" not in slot:
        raise Verdict(BLOCKED, f"{label} evidence has no body.")
    return slot["body"]


def need_dict(value, label):
    if not isinstance(value, dict):
        raise Verdict(FAIL, f"{label} is not a JSON object.")
    return value


def nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def check_image(evidence, options):
    expected = options.expect_image_digest
    if expected is not None and not DIGEST_RE.match(expected):
        raise Verdict(BLOCKED, "--expect-image-digest must be sha256:<64 hex>.")
    image = evidence.get("image") if evidence is not None else None
    if image is None:
        if expected is not None:
            raise Verdict(
                BLOCKED,
                "An expected image digest was supplied but no image evidence was.",
            )
        raise Verdict(NOT_RUN, "No image evidence supplied.")
    reference = image.get("reference") if isinstance(image, dict) else None
    if not isinstance(reference, str):
        raise Verdict(BLOCKED, "image.reference must be a string.")
    match = IMAGE_RE.match(reference)
    if not match:
        raise Verdict(
            FAIL,
            "Image reference is not an immutable <name>@sha256:<64 hex> digest reference; a tag is not an identity.",
        )
    if expected is None:
        raise Verdict(
            BLOCKED,
            "Digest form is valid but no independent --expect-image-digest was supplied, so the self-declared reference proves nothing.",
        )
    if match.group(1) != expected:
        raise Verdict(FAIL, "Image digest does not match the expected digest.")
    return (
        PASS,
        "Image reference digest matches the expected digest; registry and running revision are not verified offline.",
    )


def check_me(evidence, options, runtime):
    body = need_dict(
        response_body(evidence["me"], ENDPOINT_NAMES["me"]), "/api/me body"
    )
    user = need_dict(body.get("user"), "/api/me user")
    projection = runtime.projection
    role = user.get("role")
    if role not in projection.STAFF_ROLES and role != projection.CONTRACTOR:
        raise Verdict(
            FAIL, f"Role {role!r} is neither a staff role nor the contractor role."
        )
    if options.expect_role is not None and role != options.expect_role:
        raise Verdict(
            FAIL, f"Role {role!r} is not the expected role {options.expect_role!r}."
        )
    contractor = projection.is_contractor(user)
    expected_keys = ME_KEYS if contractor else ME_KEYS | {"work_queues"}
    if set(body) != expected_keys:
        raise Verdict(
            FAIL,
            f"/api/me keys differ from the runtime contract: {sorted(set(body) ^ expected_keys)}.",
        )
    if not nonempty_str(user.get("name")):
        raise Verdict(FAIL, "/api/me user has no name.")
    if contractor:
        if (
            set(user) != {"name", "role", "contractor"}
            or body["counts"] != {}
            or body["staff"] != []
        ):
            raise Verdict(
                FAIL,
                "Contractor payload must be user{name,role,contractor} with empty counts and staff.",
            )
    else:
        counts = need_dict(body["counts"], "/api/me counts")
        if set(counts) != {"mine", "hazards", "open"} or not all(
            is_int(v) for v in counts.values()
        ):
            raise Verdict(FAIL, "Staff counts must be integer mine, hazards and open.")
        staff = body["staff"]
        if not isinstance(staff, list) or not all(
            isinstance(s, dict)
            and nonempty_str(s.get("email"))
            and nonempty_str(s.get("role"))
            for s in staff
        ):
            raise Verdict(FAIL, "Staff must be a list of objects with email and role.")
        if body["work_queues"] != runtime.taskqueues.contract(runtime.ranking.CURRENT):
            raise Verdict(
                FAIL,
                "work_queues differs from the current runtime task-queue contract.",
            )
    account = need_dict(body["account"], "/api/me account")
    if set(account) != {"name", "email", "provider"} or not nonempty_str(
        account.get("provider")
    ):
        raise Verdict(FAIL, "account must be {name, email, provider}.")
    if (
        evidence["origin"] == "deployed-capture"
        and account["provider"] != "trusted-proxy"
    ):
        raise Verdict(
            FAIL, "A deployed capture must come from the trusted-proxy provider."
        )
    tiles = need_dict(body["map"], "/api/me map")
    if set(tiles) != {"tiles", "attribution"}:
        raise Verdict(FAIL, "map must be {tiles, attribution}.")
    if body["navigation"] != runtime.navigation(user):
        raise Verdict(
            FAIL, "navigation differs from the runtime navigation for this role."
        )
    return PASS, f"/api/me matches the runtime contract for role {role}."


def stored_outcome(outcome):
    return outcome.strip()[:80]


def last_contact(detail, label):
    detail = need_dict(detail, label)
    contacts = detail.get("contacts")
    if not isinstance(contacts, list):
        raise Verdict(FAIL, f"{label} has no contacts list.")
    return contacts


def check_case_write(evidence, runtime):
    slot = evidence["case_write"]
    if not isinstance(slot, dict):
        raise Verdict(BLOCKED, "case_write evidence must be an object.")
    if slot.get("synthetic") is not True:
        raise Verdict(
            BLOCKED,
            "case_write evidence is not declared synthetic; it is not accepted.",
        )
    request = slot.get("request")
    if (
        not isinstance(request, dict)
        or not nonempty_str(request.get("outcome"))
        or not nonempty_str(request.get("channel"))
    ):
        raise Verdict(BLOCKED, "case_write.request needs outcome and channel.")
    case_id = slot.get("case_id")
    if not nonempty_str(case_id):
        raise Verdict(BLOCKED, "case_write.case_id is required.")
    bodies = {
        name: response_body(slot.get(name), name)
        for name in ("before", "write", "after", "audit_before", "audit_after")
    }
    before, written, after = (
        last_contact(bodies[n], f"case_write.{n}") for n in ("before", "write", "after")
    )
    for name in ("before", "write", "after"):
        if bodies[name].get("id") != case_id:
            raise Verdict(FAIL, f"case_write.{name} is not case {case_id}.")
    if len(written) != len(before) + 1:
        raise Verdict(FAIL, "The write response did not add exactly one contact.")
    expected_outcome = stored_outcome(request["outcome"])
    final = need_dict(after[-1], "reloaded last contact") if after else None
    if final is None or len(after) != len(written):
        raise Verdict(
            FAIL,
            "The reloaded case does not retain the contact count from the write response.",
        )
    note = request.get("note", "")
    if not isinstance(note, str):
        raise Verdict(BLOCKED, "case_write.request.note must be a string when given.")
    expected_note = note[:500]
    sent = need_dict(written[-1], "write response last contact")
    if sent.get("outcome") == runtime.projection.NOTE_HELD:
        raise Verdict(
            BLOCKED,
            "The write response outcome is held for this role, so the write cannot be compared from this role's view.",
        )
    if (
        sent.get("outcome") != expected_outcome
        or sent.get("channel") != request["channel"]
    ):
        raise Verdict(
            FAIL,
            "The write response last contact does not match the submitted outcome and channel.",
        )
    for label, contact_ in (("write response", sent), ("reloaded", final)):
        if contact_.get("note") == runtime.projection.NOTE_HELD:
            raise Verdict(
                BLOCKED,
                f"The {label} note is held for this role, so the submitted note cannot be compared from this role's view.",
            )
        if contact_.get("note") != expected_note:
            raise Verdict(
                FAIL,
                f"The {label} last contact note does not match the submitted note (stored as written, at most 500 characters).",
            )
    if final.get("outcome") == runtime.projection.NOTE_HELD:
        raise Verdict(
            BLOCKED,
            "The reloaded outcome is held for this role, so persistence cannot be shown from this role's view.",
        )
    if (
        final.get("outcome") != expected_outcome
        or final.get("channel") != request["channel"]
    ):
        raise Verdict(
            FAIL,
            "The reloaded last contact does not match the submitted outcome and channel.",
        )
    audits = {}
    for name in ("audit_before", "audit_after"):
        report = need_dict(bodies[name], f"case_write.{name}")
        if (
            report.get("intact") is not True
            or not is_int(report.get("entries"))
            or not nonempty_str(report.get("head"))
        ):
            raise Verdict(FAIL, f"case_write.{name} is not an intact ledger report.")
        audits[name] = report
    if (
        audits["audit_after"]["entries"] <= audits["audit_before"]["entries"]
        or audits["audit_after"]["head"] == audits["audit_before"]["head"]
    ):
        raise Verdict(
            FAIL, "The audit ledger did not grow and change head across the write."
        )
    if slot.get("restart_between_write_and_read") is not True:
        raise Verdict(
            BLOCKED,
            "No restart between write and reload is declared, so persistence is not shown (a fresh read is not durability).",
        )
    if any(sent.get(k) != final.get(k) for k in set(sent) | set(final)):
        raise Verdict(
            FAIL, "The write response last contact differs from the reloaded contact."
        )
    raise Verdict(
        BLOCKED,
        "Supplied snapshots are response-shape consistent, but SQL backing, a real restart and persistence cannot be verified offline from self-supplied responses; durability stays blocked until independently verifiable deployed evidence exists (#349, #360).",
    )


def check_ai(evidence, runtime):
    body = need_dict(response_body(evidence["ai"], ENDPOINT_NAMES["ai"]), "AI body")
    if "recommendation" in body and "source" not in body:
        raise Verdict(
            FAIL,
            "AI evidence must be the bare POST /api/ai/priority record, not the GET recommendation wrapper.",
        )
    source = body.get("source")
    if (
        source == "template"
        or body.get("fallback_reason")
        or body.get("mode") == "workflow-only"
    ):
        raise Verdict(
            FAIL,
            f"Response is a template or workflow-only result ({body.get('fallback_reason')!r}), not bounded AI evidence.",
        )
    if source != "ai":
        raise Verdict(FAIL, f"AI source is {source!r}, not 'ai'.")
    release = body.get("release")
    problems = []
    if not nonempty_str(body.get("model")):
        problems.append("model")
    if body.get("validated") is not True:
        problems.append("validated")
    if body.get("mode") != "ai":
        problems.append("mode")
    if not isinstance(release, dict) or not all(
        nonempty_str(release.get(k)) for k in ("id", "version", "digest")
    ):
        problems.append("release id/version/digest")
    if isinstance(body.get("latency_ms"), bool) or not isinstance(
        body.get("latency_ms"), (int, float)
    ):
        problems.append("latency_ms")
    if body.get("status") != "Proposed":
        problems.append("status")
    if body.get("label") != runtime.rec_label:
        problems.append("label")
    if body.get("quarantine") is not None:
        problems.append("quarantine")
    if body.get("release_denied") is not False:
        problems.append("release_denied")
    if body.get("epoch_current") is not True:
        problems.append("epoch_current")
    items = body.get("items")
    if (
        not isinstance(items, list)
        or not items
        or not all(
            isinstance(i, dict) and isinstance(i.get("cites"), list) and i["cites"]
            for i in items
        )
    ):
        problems.append("cited items")
    if problems:
        raise Verdict(
            FAIL,
            "AI record is not valid bounded-AI evidence: " + ", ".join(problems) + ".",
        )
    return (
        PASS,
        "Record is a validated, released, cited AI suggestion, not a template; model and release are self-reported by the capture.",
    )


def check_baseline(evidence, options):
    body = need_dict(
        response_body(evidence["programme"], ENDPOINT_NAMES["programme"]),
        "programme body",
    )
    total = body.get("total")
    if not is_int(total) or not isinstance(body.get("items"), list):
        raise Verdict(FAIL, "Programme page needs integer total and an items list.")
    if total == STOCK_HOMES and options.expect_programme_cases != STOCK_HOMES:
        raise Verdict(
            FAIL,
            f"Total {STOCK_HOMES} is the generated home stock, not the operational case programme.",
        )
    if total != options.expect_programme_cases:
        raise Verdict(
            FAIL,
            f"Open permitted cases total {total}, expected {options.expect_programme_cases}.",
        )
    return (
        PASS,
        f"Open permitted case total is {total}; the {STOCK_HOMES} generated homes are a separate baseline.",
    )


SLOTS = {
    "me_contract": "me",
    "case_write_reload": "case_write",
    "ai_evidence": "ai",
    "baseline_distinction": "programme",
}


def run_check(name, evidence, options, runtime_loader):
    if name != "image_identity":
        if evidence is None:
            return NOT_RUN, "No evidence file supplied."
        if SLOTS[name] not in evidence:
            return NOT_RUN, f"No {SLOTS[name]} evidence supplied."
    try:
        if name == "image_identity":
            return check_image(evidence, options)
        if name == "baseline_distinction":
            return check_baseline(evidence, options)
        runtime = runtime_loader()
        if name == "me_contract":
            return check_me(evidence, options, runtime)
        if name == "case_write_reload":
            return check_case_write(evidence, runtime)
        return check_ai(evidence, runtime)
    except Verdict as verdict:
        return verdict.status, verdict.reason


def overall_status(statuses):
    if FAIL in statuses:
        return FAIL
    if BLOCKED in statuses:
        return BLOCKED
    if all(s == NOT_RUN for s in statuses):
        return NOT_RUN
    return BLOCKED


def build_report(evidence_path, options, runtime_loader=load_runtime):
    evidence, load_error = None, None
    if evidence_path is not None:
        try:
            evidence = load_evidence(evidence_path)
        except Verdict as verdict:
            load_error = verdict.reason
    results = []
    for name in CHECKS:
        if load_error is not None:
            status, reason = BLOCKED, load_error
        else:
            status, reason = run_check(name, evidence, options, runtime_loader)
        results.append(dict(id=name, status=status, reason=reason))
    for name, reason in GAPS.items():
        results.append(dict(id=name, status=NOT_RUN, reason=reason))
    overall = overall_status([r["status"] for r in results])
    origin = evidence["origin"] if evidence else None
    self_declared = [
        "origin",
        "image.reference",
        "case_write.synthetic",
        "case_write.restart_between_write_and_read",
    ]
    return dict(
        schema_version=SCHEMA_VERSION,
        offline_only=True,
        acceptance="not-accepted",
        evidence_origin=origin,
        overall=overall,
        checks=results,
        gaps=sorted(GAPS),
        self_declared=self_declared,
        baselines=dict(
            programme_cases_expected=options.expect_programme_cases,
            generated_homes=STOCK_HOMES,
        ),
        note="Offline harness output; it is not deployed acceptance and leaves every original #350 criterion unmet.",
    )


def render_text(report):
    lines = [
        f"overall: {report['overall']} (acceptance: {report['acceptance']}, origin: {report['evidence_origin']})"
    ]
    lines += [f"{c['status']:8} {c['id']}: {c['reason']}" for c in report["checks"]]
    lines.append(report["note"])
    return "\n".join(lines)


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--evidence", help="JSON evidence bundle; omit to report every check not-run"
    )
    parser.add_argument(
        "--expect-image-digest", help="independently supplied sha256:<64 hex> digest"
    )
    parser.add_argument("--expect-role", help="role the /api/me capture must show")
    parser.add_argument(
        "--expect-programme-cases", type=int, default=DEFAULT_PROGRAMME_CASES
    )
    parser.add_argument("--format", choices=("json", "text"), default="json")
    return parser.parse_args(argv)


def main(argv=None):
    options = parse_args(sys.argv[1:] if argv is None else argv)
    report = build_report(options.evidence, options)
    print(
        render_text(report)
        if options.format == "text"
        else json.dumps(report, indent=2, sort_keys=True)
    )
    return EXIT_CODES[report["overall"]]


if __name__ == "__main__":
    sys.exit(main())
