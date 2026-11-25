"""Run the merged real-AI harness once, live, under the owner hard cap. Token comes from the existing az login; never printed."""
import json, sys
from datetime import datetime, timedelta, timezone
sys.path[:0] = ["../../../src/api/checks"]
import assistant_real_ai_acceptance as h
from zava_forward.agents import heldout_aoai

listing = json.load(open("listing_after_raw.json"))
b = listing["assistants"][0]["binding"]
auth = dict(approved_by="Juan Manuel Servera, project owner", authority_ref="owner-decision:2026-11-25 demo real-AI batch, hard cap 200000 tokens",
            model="gpt-4.1-nano", endpoint=b["endpoint"], deployment=b["deployment"],
            expires_utc=(datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
            max_calls=5, max_total_tokens=200000, max_prompt_tokens=400, max_completion_tokens=200,
            max_budget_usd="1.00", currency="USD", input_usd_per_1m="0.10", output_usd_per_1m="0.40")
json.dump(auth, open("harness_authorization.json", "w"), indent=1)
token = heldout_aoai.get_token("az-cli")
provider = heldout_aoai.make_provider(b["endpoint"], b["deployment"], "gpt-4.1-nano", token)
report = h.run(auth, listing, "live", provider, True)
t = json.dumps(report, indent=1, sort_keys=True)
open("harness_report.json", "w").write(t); print(t)
