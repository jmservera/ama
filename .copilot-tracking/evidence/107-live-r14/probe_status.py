import json, urllib.request, urllib.error
from zava_forward.agents import heldout_aoai
l = json.load(open("listing_after_raw.json")); b = l["assistants"][0]["binding"]
tok = heldout_aoai.get_token("az-cli")
url = f"{b['endpoint']}/openai/deployments/{b['deployment']}/chat/completions?api-version={heldout_aoai.API_VERSION}"
req = urllib.request.Request(url, data=json.dumps(dict(messages=[dict(role="user", content="Say hi.")], max_tokens=5, temperature=0)).encode(), method="POST", headers={"Content-Type":"application/json","Authorization":"Bearer "+tok})
try:
    r = urllib.request.urlopen(req, timeout=60); body = json.loads(r.read()); print("http", r.status, "served:", body.get("model"), "usage:", body.get("usage"))
except urllib.error.HTTPError as e:
    try: err = json.loads(e.read()).get("error", {})
    except Exception: err = {}
    print("http", e.code, err.get("code"), str(err.get("message"))[:160])
except Exception as e:
    print("exc", type(e).__name__, str(e)[:150])
