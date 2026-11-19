"""Static scan: imports and I/O-capable names in the five discovery assistant modules."""
import ast, glob, json
bad = {"socket","http","urllib","requests","httpx","subprocess","sqlite3","os","pathlib","shutil","azure","openai","datetime","time","random","tempfile","ssl","smtplib"}
out = {}
for f in sorted(glob.glob("../../../../src/core/src/zava_forward/core/discovery_assistant_*.py")):
    t = ast.parse(open(f).read()); imps = set(); calls = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import): imps |= {a.name for a in n.names}
        if isinstance(n, ast.ImportFrom): imps.add(n.module or "")
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {"open","exec","eval","__import__","print"}: calls.add(n.func.id)
    out[f.split("/")[-1]] = {"imports": sorted(imps), "flagged_imports": sorted(i for i in imps if i.split(".")[0] in bad), "builtin_io_calls": sorted(calls)}
print(json.dumps(out, indent=1)); json.dump(out, open("static_scan.json","w"), indent=1)
