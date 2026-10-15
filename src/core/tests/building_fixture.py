"""Wholly fictional building and two independent home cases for issue 75."""

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store


def fixture() -> dict[str, Any]:
    data: dict[str, Any] = deepcopy(DATA)
    data["cases"] = data["cases"][1:3]
    for home in data["cases"]:
        home["building_id"] = "SYN-B1"
        home["decision"]["status"] = "Accepted"
        home["funding_ok"] = True
        home["cost_allocation"] = [
            {"shared_cost_id": "COST-1", "amount_gbp": "6000.00", "source": "SYN-ALLOCATION"}
        ]
    data["cases"][1]["quality"] = [
        {
            "measure": "Loft insulation",
            "state": "Accepted",
            "source": "SYN-QA-SIBLING",
            "submitted_by": "Synthetic provider",
            "recorded_by": "Synthetic recorder",
            "recorded_by_code": "SYN-RECORDER",
            "accepted_by": "Synthetic independent inspector",
            "checklist_version": "QC-LOFT v1",
            "items": [],
            "history": [],
            "aftercare": [],
            "defect": None,
            "handover": None,
        }
    ]
    data["cases"][1]["documents"] = [
        {
            "id": "SIBLING-EVIDENCE",
            "name": "Synthetic survey metadata only",
            "kind": "Survey",
            "source": "SYN-EVIDENCE",
            "at": "2026-10-15",
            "by": "Synthetic surveyor",
        }
    ]
    data["procurement"] = {
        "packages": [
            {
                "id": pid,
                "name": pid,
                "period_from": "2026-01-01",
                "period_to": "2099-12-31",
                "scope": "Synthetic scope",
                "scope_version": 1,
                "scope_history": [],
                "contract_ref": "SYN-CONTRACT",
                "capacity": {
                    "Test Ltd": {
                        "offered": 5,
                        "committed": 5,
                        "evidence": "SYN-CAPACITY",
                        "by": "Pam Lead",
                        "at": "2026-10-15",
                        "history": [],
                    }
                },
            }
            for pid in ("PKG-SHARED", "PKG-OTHER")
        ],
        "work_orders": [],
    }
    data["buildings"] = [
        {
            "id": "SYN-B1",
            "name": "Fictional exercise block",
            "version": 1,
            "source": "SYN-BUILDING-REGISTER",
            "systems": [{"id": "SYS-1", "label": "Shared ventilation", "source": "SYN-SURVEY"}],
            "dependencies": [],
            "holds": [],
            "works": [
                {
                    "id": "WORK-1",
                    "label": "Shared ventilation renewal",
                    "status": "Proposed",
                    "owner": "Synthetic coordinator",
                    "source": "SYN-SCOPE",
                    "case_ids": ["ZF-2"],
                    "package_ids": ["PKG-SHARED"],
                }
            ],
            "costs": [
                {
                    "id": "COST-1",
                    "work_id": "WORK-1",
                    "amount_gbp": "12000.00",
                    "source": "SYN-ESTIMATE",
                }
            ],
        }
    ]
    return data


def hold() -> dict[str, Any]:
    return {
        "id": "HOLD-1",
        "label": "Competent review pending",
        "status": "Open",
        "owner": "Synthetic safety reviewer",
        "source": "SYN-REVIEW",
        "case_ids": ["ZF-2"],
        "package_ids": ["PKG-SHARED"],
    }


def open_store(folder: str, sql: bool, data: dict[str, Any] | None = None) -> Any:
    seed = Path(folder) / "synthetic.json"
    if data is not None:
        seed.write_text(json.dumps(data), encoding="utf-8")
    factory: Any = SqlStore if sql else Store
    return factory(str(seed), str(Path(folder) / "state.db")) if sql else factory(str(seed))
