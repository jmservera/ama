"""Synthetic exact-base semantic probe; no application data or inference."""

import copy
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from dataset import DATA
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store


def main() -> None:
    failed = []
    data = copy.deepcopy(DATA)
    data["as_of"] = "2026-10-16"
    data["cases"] = []
    for stage in ("Contacting resident", "Final checks before ordering"):
        for kind in ("funding", "technical"):
            case = copy.deepcopy(DATA["cases"][2])
            case.update(id=f"{stage.split()[0]}-{kind}", stage=stage)
            if kind == "funding":
                case["funding_ok"] = False
            else:
                case["technical"]["signoffs"].pop("coordination")
            data["cases"].append(case)
    for factory in (Store, SqlStore):
        with tempfile.TemporaryDirectory(prefix="issue76-probe-") as tmp:
            seed = Path(tmp) / "synthetic.json"
            seed.write_text(json.dumps(data))
            store = (
                factory(str(seed), str(seed.with_suffix(".sqlite")))
                if factory is SqlStore
                else factory(str(seed))
            )
            try:
                with patch("zava_forward.core.controls.today", return_value="2026-10-16"):
                    members = {
                        row["id"]
                        for row in store.list_cases(
                            data["staff"][1], "all", filters={"queue": "blocked"}
                        )
                    }
                    for cid, case in store.cases.items():
                        work = store.work_context(case, data["staff"][1])
                        expected = case["stage"] == "Final checks before ordering"
                        current = any(row["current_stop"] for row in work["blockers"])
                        coherent = (cid in members) == expected == current
                        print(json.dumps(dict(
                            store=factory.__name__, case=cid, expected_blocked=expected,
                            member=cid in members, current_stop=current,
                            reason=work["reason"], next_action=work["next_action"],
                            requirements=len(work["blockers"]), coherent=coherent,
                        ), sort_keys=True))
                        if not coherent:
                            failed.append(f"{factory.__name__}:{cid}")
            finally:
                if isinstance(store, SqlStore):
                    store.db.close()
    if failed:
        raise SystemExit("Semantic failures: " + ", ".join(failed))


if __name__ == "__main__":
    main()
