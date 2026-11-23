"""Issue 2257: repeated same-session reads of /api/map, /api/stats and /api/facets to locate server-side 500s. Credentials are read at runtime and never printed."""
import json, os, time
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "live_probe.py")).read().split("results = []")[0])
JS = """async()=>{const out={};
for (const [k,u] of [['map','/api/map?zoom=5'],['stats','/api/stats'],['facets','/api/facets']]) {
  out[k]=[];
  for (let i=0;i<40;i++){const t=performance.now();
    try{const r=await fetch(u);out[k].push([r.status,Math.round(performance.now()-t)]);}catch(e){out[k].push(['fail',0]);}}}
out.parallel=[];
const rs=await Promise.all(Array.from({length:6},()=>fetch('/api/map?zoom=5').then(r=>r.status).catch(()=>'fail')));
out.parallel=rs;return out;}"""
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(); page = ctx.new_page(); login(page)
    page.goto(EMP + "/app#/overview", wait_until="load"); page.wait_for_timeout(8000)
    res = page.evaluate(JS); b.close()
summary = {k: {"statuses": sorted({str(x[0]) for x in v}), "non200": sum(1 for x in v if x[0] != 200), "n": len(v), "max_ms": max(x[1] for x in v)} for k, v in res.items() if k != "parallel"}
summary["parallel_map"] = res["parallel"]; summary["utc"] = time.strftime("%H:%M:%S", time.gmtime())
json.dump(summary, open(os.path.join(OUT, "load-probe-result.json"), "w"), indent=1); print(json.dumps(summary))
