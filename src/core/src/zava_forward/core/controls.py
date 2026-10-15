"""Shared checks for the controlled workflows: finance, grants, sign-offs and resident decisions.

These helpers keep the rules in one place: one record at a time (FR-007), a
different person for each approval (CON-007), plain-word refusals, and amounts
and text that are cleaned before they are stored.
"""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

FINANCE_ROLES = ("Grants and Evidence Officer", "Retrofit Programme Manager", "Programme Support Officer")
FINANCE_APPROVERS = ("Retrofit Programme Manager", "Programme Support Officer")
RESIDENT_ROLES = ("Resident Liaison Officer", "Retrofit Coordinator", "Retrofit Programme Manager", "Programme Support Officer")
BULK_KEYS = ("case_ids", "ids", "items", "all")


def today():
    return date.today().isoformat()


def now():
    return datetime.now().isoformat(timespec="minutes")


def refuse_bulk(body):
    """Approvals, commitments, payments, claims and complaint closure are never bulk actions (FR-007, AC-010)."""
    if any(k in (body or {}) for k in BULK_KEYS):
        raise PermissionError("This can only be done for one record at a time. Open the case and do it there.")


def require_role(user, roles, what):
    if user["role"] not in roles:
        raise PermissionError(f"Only {what} can do this.")


def different_person(user, other, what):
    if other and other.lower() == user["email"].lower():
        raise PermissionError(f"A different person must {what}. You prepared this one.")


def text(value, label, limit=300, required=True):
    value = (value or "").strip()[:limit] if isinstance(value, str) else ""
    if required and not value:
        raise ValueError(f"Add {label}.")
    return value


def money(value, label="the amount"):
    try:
        d = Decimal(str(value).replace(",", "").replace("£", "").strip())
    except (InvalidOperation, ValueError):
        raise ValueError(f"Enter {label} as a number of pounds.")
    if not d.is_finite() or d <= 0 or d > Decimal("100000000"):
        raise ValueError(f"Enter {label} as a number of pounds above zero.")
    return float(d.quantize(Decimal("0.01")))


def quantity(value):
    try:
        q = float(value)
    except (TypeError, ValueError):
        raise ValueError("Enter the quantity as a number.")
    if not 0 < q <= 1_000_000:
        raise ValueError("Enter a quantity above zero.")
    return q


def next_id(items, prefix):
    return f"{prefix}-{len(items) + 1}"


def find(items, item_id, label):
    for i in items:
        if i["id"] == item_id:
            return i
    raise ValueError(f"That {label} was not found.")


def choice(value, options, label):
    if value not in options:
        raise ValueError(f"Choose {label} from the list.")
    return value
