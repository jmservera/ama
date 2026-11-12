import test_form_review, sys
from zava_forward.core import form_export, forms
b = test_form_review.FormReview(); b.setUp()
store = b.stores[0]
draft, epc, area = b.prepare(store)
saved = form_export.draft_export(store, b.actor, "ZF-1", draft["draft_id"])
print([i for i in saved["open_issues"] if i["field_id"]=="area"])
doc = store.add_document(b.actor, "ZF-1", "s2.txt", "EPC", b"99", metadata=test_form_review.change_metadata(store, "ZF-1"))
req = test_form_review.batch(doc["id"]); req["candidates"]=[dict(field_id="area", raw_value="99", locator=dict(start=0,end=2))]
forms.stage_candidates(store, b.actor, "ZF-1", req)
now = form_export.draft_export(store, b.actor, "ZF-1", draft["draft_id"])
print([i for i in now["open_issues"] if i["field_id"]=="area"], now["content_sha256"]!=saved["content_sha256"])
print(form_export.export_freshness(store, b.actor, "ZF-1", saved))
