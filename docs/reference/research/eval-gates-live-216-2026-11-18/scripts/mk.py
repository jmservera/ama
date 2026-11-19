import json, base64
from pg import open_page, call
spec=json.load(open("/home/azureuser/source/ama-wt/issue-216-live-20261118T1416Z/docs/reference/research/eval-gates-live-216-2026-11-18/cases.json"))
pw,ctx,pg=open_page()
st,d=call(pg,"GET",f"/api/cases/{spec['case_id']}"); assert st==200
case=d if "id" in d else d
print(st, list(d.keys())[:8], d.get("id"))
non=[c for c in spec["cases"] if c["expect"]!="refused"]
ref=[c for c in spec["cases"] if c["expect"]=="refused"]
batches=[non[0:7],non[7:14],non[14:]]+[ref]
for i,b in enumerate(batches):
    json.dump({"case":case,"cases":[{"id":c["id"],"q":c["q"]} for c in b]},open(f"bundle{i}.json","w"))
print([len(b) for b in batches])
