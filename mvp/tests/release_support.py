"""Constructed release records for offline tests. Fixtures are labelled synthetic and grant no real authorisation."""
import json
import time

from zavaforward_mvp import assistant_release as rel
from zavaforward_mvp import assistants


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
    from zavaforward_mvp.ai_registry import LEGACY
    ai = ai or store.ai
    db = store.assistant_connection()
    try:
        for ddl in rel.SQLITE_DDL:
            db.execute(ddl)
        for cap in assistants.REGISTRY if tasks is None else tasks:
            rec = fixture(cap, assistants.runtime_binding(cap, ai), model, cls, **over)
            db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES (?,?,'active',?,1)",
                       (f"fx-{cap}", cap, rel.canonical(rec)))
        if legacy and getattr(ai, "endpoint", ""):
            for t in LEGACY:
                rec = fixture(f"legacy:{t}", dict(provider="azure-openai", endpoint=ai.endpoint, deployment=ai.fast),
                              model, "actual", **{k: v for k, v in over.items() if k != "cls"})
                for k in rel.BOUND:
                    rec.setdefault(k, "n/a")
                db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES (?,?,'active',?,1)",
                           (f"fx-legacy-{t}", f"legacy:{t}", rel.canonical(rec)))
    finally:
        db.close()
