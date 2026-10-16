"""Presentation metadata for existing server-authorized workbench destinations."""

from typing import TypedDict

from zava_forward.core import projection
from zava_forward.core.workflows import MANAGER_ROLES


class Destination(TypedDict):
    href: str
    label: str
    scope: str


def navigation(user: dict[str, str]) -> list[Destination]:
    """Describe navigation, never grant access or substitute for endpoint checks."""
    if not projection.allowed(user, "cases"):
        return []
    if projection.is_contractor(user):
        return [Destination(href="#/", label="My jobs", scope="Assigned contractor jobs")]
    links = [
        ("#/", "My cases", "My assigned cases", "cases"),
        ("#/all", "All cases", "All permitted open cases", "cases"),
        ("#/overview", "Overview", "Programme overview", "stats"),
        (
            "#/visits",
            "Visits",
            "Programme visits" if user["role"] in MANAGER_ROLES else "My visits",
            "visits",
        ),
        ("#/funding", "Funding", "Programme funding evidence", "funding"),
    ]
    if user["role"] in projection.FINANCE_VIEW:
        links.append(("#/finance", "Finance", "Finance review queue", "finance_queue"))
    if user["role"] in MANAGER_ROLES:
        links.extend(
            [
                ("#/capacity", "Capacity and work orders", "Programme capacity", "packages"),
                ("#/closed", "Closed cases", "Closed case directory", "cases"),
            ]
        )
    links.extend(
        [
            ("#/assistants", "Assistant proposals", "My permitted proposals", "assistants"),
            ("#/time", "Time capture", "My time records", "time"),
        ]
    )
    return [
        Destination(href=href, label=label, scope=scope)
        for href, label, scope, kind in links
        if projection.allowed(user, kind)
    ]
