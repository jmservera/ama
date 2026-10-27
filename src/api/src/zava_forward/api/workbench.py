"""Presentation metadata for existing server-authorized workbench destinations."""

from typing import TypedDict

from zava_forward.core import projection
from zava_forward.core.workflows import MANAGER_ROLES


class Destination(TypedDict, total=False):
    href: str
    label: str
    scope: str
    access: str


def navigation(user: dict[str, str]) -> list[Destination]:
    """Describe navigation, never grant access or substitute for endpoint checks.

    An application administrator sees every option; each carries whether the signed-in
    role actually reaches it, and the server still enforces the actual authority.
    """
    admin = bool(user.get("app_admin"))
    if not admin and not projection.allowed(user, "cases"):
        return []
    if projection.is_contractor(user):
        return [
            Destination(href="#/", label="My jobs", scope="Assigned contractor jobs"),
            Destination(
                href="#/screens", label="Specialist screens", scope="Installed assigned-job screens"
            ),
        ]
    manager = user.get("role") in MANAGER_ROLES
    links = [
        ("#/", "My cases", "My assigned cases", "cases", True),
        ("#/all", "All cases", "All permitted open cases", "cases", True),
        ("#/overview", "Overview", "Programme overview", "stats", True),
        ("#/visits", "Visits", "Programme visits" if manager else "My visits", "visits", True),
        ("#/funding", "Funding", "Programme funding evidence", "funding", True),
        (
            "#/finance",
            "Finance",
            "Finance review queue",
            "finance_queue",
            user.get("role") in projection.FINANCE_VIEW,
        ),
        ("#/capacity", "Capacity and work orders", "Programme capacity", "packages", manager),
        ("#/closed", "Closed cases", "Closed case directory", "cases", manager),
        ("#/assistants", "Assistant proposals", "My permitted proposals", "assistants", True),
        ("#/time", "Time capture", "My time records", "time", True),
        ("#/screens", "Specialist screens", "Installed role screens", "cases", True),
    ]
    out = []
    for href, label, scope, kind, role_ok in links:
        granted = bool(role_ok and projection.allowed(user, kind))
        if granted:
            dest = Destination(href=href, label=label, scope=scope)
            if admin:
                dest["access"] = "available"
            out.append(dest)
        elif admin:
            out.append(
                Destination(
                    href=href, label=label, scope=scope, access="needs a role with this authority"
                )
            )
    return out
