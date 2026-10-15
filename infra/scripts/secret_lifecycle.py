#!/usr/bin/env python3
"""Key Vault secret lifecycle checks: inventory, rotation due dates and access review records.

Reads Azure CLI JSON from files so it can be tested offline. Never reads or prints secret values.

  secret_lifecycle.py check --inventory infra/secret-inventory.json --secrets secrets.json [--now ISO]
      secrets.json is `az keyvault secret list --vault-name V -o json`.
  secret_lifecycle.py review --inventory infra/secret-inventory.json --assignments roles.json --reviewer NAME [--now ISO]
      roles.json is `az role assignment list --scope <vault id> --include-inherited -o json`.
  secret_lifecycle.py rotation-plan --vault V --app-id ID
      prints the ordered, zero-downtime rotation steps (no secret is created).
"""
import argparse
import datetime as dt
import json
import sys

DATA_ROLES = {
    "Key Vault Secrets User": "read",
    "Key Vault Secrets Officer": "write",
    "Key Vault Administrator": "admin",
    "Key Vault Reader": "metadata",
    "Owner": "no data-plane access",
}
REQUIRED = ("name", "owner", "rotationIntervalDays", "expiryAlertDays")


def parse_time(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def validate_inventory(inventory):
    problems = []
    for entry in inventory.get("secrets", []):
        for key in REQUIRED:
            if not entry.get(key):
                problems.append(f"{entry.get('name', '?')}: missing {key}")
    if not inventory.get("secrets"):
        problems.append("inventory has no secrets")
    return problems


def check_secrets(inventory, listed, now):
    """Findings for each inventoried secret, using only metadata (never values)."""
    findings = []
    by_name = {item["name"]: item for item in listed}
    for entry in inventory["secrets"]:
        item = by_name.get(entry["name"])
        if item is None:
            findings.append((entry["name"], "missing", "secret not present in the vault"))
            continue
        attrs = item.get("attributes", {})
        if not attrs.get("enabled", True):
            findings.append((entry["name"], "disabled", "secret is disabled"))
        expires = attrs.get("expires")
        if not expires:
            findings.append((entry["name"], "no-expiry", "no expiry date is set"))
        else:
            left = (parse_time(expires) - now).days
            if left < 0:
                findings.append((entry["name"], "expired", f"expired {-left} days ago"))
            elif left <= entry["expiryAlertDays"]:
                findings.append((entry["name"], "expiring", f"{left} days left, inside the {entry['expiryAlertDays']} day alert window"))
        updated = attrs.get("updated") or attrs.get("created")
        if updated:
            age = (now - parse_time(updated)).days
            if age > entry["rotationIntervalDays"]:
                findings.append((entry["name"], "rotation-overdue", f"{age} days since last change, interval {entry['rotationIntervalDays']}"))
    return findings


def access_review(inventory, assignments, reviewer, now):
    rows = []
    for item in assignments:
        role = item.get("roleDefinitionName", "")
        rows.append({
            "principalId": item.get("principalId"),
            "principalType": item.get("principalType"),
            "role": role,
            "access": DATA_ROLES.get(role, "unclassified, needs justification"),
            "scope": item.get("scope"),
            "decision": "pending",
        })
    return {
        "reviewedAt": now.isoformat(),
        "reviewer": reviewer,
        "nextReviewDue": (now + dt.timedelta(days=inventory["reviewIntervalDays"])).date().isoformat(),
        "assignments": rows,
        "note": "Each decision stays pending until a named human marks keep or remove.",
    }


def rotation_plan(vault, app_id):
    return [
        f"1. az ad app credential reset --id {app_id} --append --display-name container-apps-auth-NEW --years 1 (old credential stays valid)",
        f"2. Store the value as a new version of entra-client-secret in {vault} with --expires; never print it",
        "3. Wait for the versionless reference to refresh (up to 30 minutes) or restart the active revision",
        "4. Sign in through /sign-in and confirm /app and a data API return 200 for an authorised user",
        f"5. Only then az ad app credential delete --id {app_id} --key-id <old key id>",
        "6. Record the rotation date and operator in the rotation log",
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=["check", "review", "rotation-plan"])
    parser.add_argument("--inventory", default="infra/secret-inventory.json")
    parser.add_argument("--secrets")
    parser.add_argument("--assignments")
    parser.add_argument("--reviewer", default="")
    parser.add_argument("--vault", default="<vault>")
    parser.add_argument("--app-id", default="<app id>")
    parser.add_argument("--now", default=None)
    args = parser.parse_args(argv)
    now = parse_time(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    if args.command == "rotation-plan":
        print("\n".join(rotation_plan(args.vault, args.app_id)))
        return 0
    inventory = load(args.inventory)
    problems = validate_inventory(inventory)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 2
    if args.command == "check":
        findings = check_secrets(inventory, load(args.secrets), now)
        for name, kind, detail in findings:
            print(f"{name}: {kind}: {detail}")
        return 1 if findings else 0
    if not args.reviewer:
        print("--reviewer is required", file=sys.stderr)
        return 2
    print(json.dumps(access_review(inventory, load(args.assignments), args.reviewer, now), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
