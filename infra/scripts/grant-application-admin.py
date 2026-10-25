#!/usr/bin/env python3
"""Assign ZavaForward.ApplicationAdmin to one verified enabled member; dry-run unless --apply.

Adds only that single assignment. It never creates credentials or roles (run setup-entra.py first so
the role exists), never touches other assignments, and refuses a wrong tenant, app or principal.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("setup_entra", HERE / "setup-entra.py")
setup = importlib.util.module_from_spec(_spec)
sys.modules["setup_entra"] = setup
_spec.loader.exec_module(setup)

ROLE_VALUE = "ZavaForward.ApplicationAdmin"
GRAPH = setup.GRAPH
SetupError = setup.SetupError


def grant(graph, tenant: str, app_id: str, upn: str, expected_oid: str, *, apply: bool) -> str:
    tenant, app_id = setup.object_id(tenant), setup.object_id(app_id)
    expected_oid = setup.object_id(expected_oid)
    setup.token_permissions(graph, tenant)  # refuses a token from a different tenant
    sps = graph.rest(GRAPH + "servicePrincipals?$filter=" + quote(f"appId eq '{app_id}'", safe="=") + "&$select=id,appId,appRoles")
    rows = sps.get("value", [])
    if len(rows) != 1 or setup.object_id(rows[0].get("appId")) != app_id:
        raise SetupError("The enterprise app for the intended application id was not found uniquely.")
    sp = rows[0]
    roles = [r for r in sp.get("appRoles", []) if r.get("value") == ROLE_VALUE]
    if len(roles) != 1 or roles[0].get("isEnabled") is not True or "User" not in roles[0].get("allowedMemberTypes", []):
        raise SetupError("ApplicationAdmin is not an enabled user role on the enterprise app; run setup-entra.py first.")
    role_id = setup.object_id(roles[0]["id"])
    user = graph.rest(GRAPH + "users/" + quote(upn, safe="") + "?$select=id,accountEnabled,userType")
    if user.get("accountEnabled") is not True or user.get("userType") != "Member":
        raise SetupError("The principal is not an enabled tenant member; nothing was assigned.")
    principal = setup.object_id(user["id"])
    if principal != expected_oid:
        raise SetupError("The principal does not resolve to the expected object id; nothing was assigned.")
    resource = setup.object_id(sp["id"])
    path = f"servicePrincipals/{resource}/appRoleAssignedTo"
    if any(a.get("principalId") == principal and a.get("appRoleId") == role_id
           and a.get("resourceId", resource) == resource for a in graph.pages(path)):
        return "already-assigned"
    if not apply:
        return "would-assign"
    if not token_can_write(graph):
        setup.authority_help()
        raise SetupError("Assignment-write permission is missing; nothing was assigned.")
    graph.rest(GRAPH + path, method="POST", body={"principalId": principal, "resourceId": resource, "appRoleId": role_id})
    setup.wait_for(lambda: graph.pages(path),
                   lambda found: any(a.get("principalId") == principal and a.get("appRoleId") == role_id
                                     and a.get("resourceId", resource) == resource for a in found),
                   "The assignment is not yet verified; rerun before relying on it.")
    return "assigned"


def token_can_write(graph) -> bool:
    return bool(setup.token_permissions(graph).intersection(setup.ASSIGNMENT_WRITE))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tenant", required=True, help="intended tenant id")
    parser.add_argument("--app-id", required=True, help="intended application (client) id")
    parser.add_argument("--upn", required=True, help="admin user principal name, resolved then checked against the expected object id")
    parser.add_argument("--expected-oid", required=True, help="immutable object id of the intended admin; the assignment is refused unless the UPN resolves to it")
    parser.add_argument("--tenant-profile", type=Path, default=setup.PROFILE)
    parser.add_argument("--apply", action="store_true", help="write the assignment (default is a dry run)")
    args = parser.parse_args(argv)
    try:
        # Graph writes pass the request body through a private temporary file that Azure.call removes.
        body_directory = setup.private_path(args.tenant_profile, directory=True) if args.apply else None
        graph = setup.Azure(args.tenant_profile, body_directory=body_directory)
        print("result: " + grant(graph, args.tenant, args.app_id, args.upn, args.expected_oid, apply=args.apply))
    except SetupError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
