"""Run from src/core/tests: shows what each funding reader reports for each funding_ok value."""

import tempfile

from building_fixture import fixture, open_store
from zava_forward.core import chat_case_answers, taskqueues

ABSENT = object()
for value in (True, False, None, "yes", 1, "false", ABSENT):
    label = "<absent>" if value is ABSENT else repr(value)
    with tempfile.TemporaryDirectory() as folder:
        store = open_store(folder, False, fixture())
        case = store.cases["ZF-2"]
        case["stage"] = "Final checks before ordering"
        if value is ABSENT:
            case.pop("funding_ok")
        else:
            case["funding_ok"] = value
        try:
            home = store.home_case_view(store.data["staff"][0], "ZF-2")["home"]["funding_confirmed"]
        except Exception as exc:
            home = f"{type(exc).__name__}({exc})"
        detail = {} if value is ABSENT else {"funding_ok": value}
        chat = chat_case_answers.case_facts(detail, reason_visible=False).get("funding_ok")
        ctx = taskqueues.context(
            case,
            as_of="2026-10-16",
            reason_ok=True,
            policy=__import__("zava_forward.core.ranking", fromlist=["CURRENT"]).CURRENT,
            stock_queries=[],
            building_reasons=[],
            resident_reasons=[],
            technical_missing=[],
            handoff=None,
        )
        queue = any(b["step"] == "Final checks: funding" for b in ctx["blockers"])
        print(f"funding_ok={label:10} home={home!r:22} chat={chat!r:15} queue_funding_blocker={queue}")
