"""Constructed release records for offline tests. Fixtures are labelled synthetic and grant no real authorisation."""
import json
import time

from zava_forward.core import assistant_release as rel
from zava_forward.core import assistants


def fixture(task, binding, model="test-model", cls="constructed-fixture", expires=None, **over):
    rec = dict(binding, task=task, evidence_class=cls, evidence=["constructed-fixture:synthetic-demo"],
               residual_risk_decision="Accept", residual_risk_note="Constructed fixture; not a real decision.",
               serving_model=model, approver=dict(name="Fixture Approver", email="approver@example.test",
                                                  role="Retrofit Programme Manager"),
               expires=expires or time.time() + 86400, recorded_at=0, actual_authorisation=cls == "actual")
    rec.update(over)
    return rec


def install(store, ai=None, model="test-model", cls="constructed-fixture", tasks=None, legacy=True, **over):
    """Insert active releases directly on a SQL store (all assistants and, if the AI is live, legacy tasks)."""
    from zava_forward.core.ai_registry import LEGACY, legacy_binding
    ai = ai or store.ai
    db = store.assistant_connection()
    try:
        if hasattr(store, "_env"):
            for ddl in rel.MSSQL_DDL:
                db.execute(f"IF OBJECT_ID(N'assistant_releases', N'U') IS NULL {ddl}")
        else:
            for ddl in rel.SQLITE_DDL:
                db.execute(ddl)
        db.execute("DELETE FROM assistant_releases WHERE id LIKE 'fx-%'")
        for cap in assistants.REGISTRY if tasks is None else tasks:
            rec = fixture(cap, assistants.runtime_binding(cap, ai), model, cls, **over)
            db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES (?,?,'active',?,1)",
                       (f"fx-{cap}", cap, rel.canonical(rec)))
        if legacy and getattr(ai, "endpoint", ""):
            for t in LEGACY:
                for dep in {ai.fast, getattr(ai, "strong", ai.fast)}:
                    rec = fixture(f"legacy:{t}", legacy_binding(t, ai, dep),
                                  model, "actual", **{k: v for k, v in over.items() if k != "cls"})
                    db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES (?,?,'active',?,1)",
                               (f"fx-legacy-{t}-{dep}", f"legacy:{t}", rel.canonical(rec)))
    finally:
        db.close()
