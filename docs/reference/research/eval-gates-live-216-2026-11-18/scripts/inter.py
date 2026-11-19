import pexpect, sys, base64, zlib, json, re, time
REP=sys.argv[1]
case=json.load(open("case_clean.json"))
batches=[json.load(open(f"bundle{i}.json"))["cases"] for i in range(4)]
code=open("inner_run.py").read()
blob=base64.b64encode(zlib.compress(json.dumps({"case":case,"batches":batches,"code":code},separators=(",",":")).encode(),9)).decode()
boot=("import base64,zlib,json,re\n"
"d=json.loads(zlib.decompress(base64.b64decode(open('/scratch/d216.b64').read())))\n"
"for b in d['batches']:\n"
" open('/scratch/r216.bundle','w').write(base64.b64encode(json.dumps({'case':d['case'],'cases':b}).encode()).decode())\n"
" exec(d['code'],{'__name__':'x'})\n")
c=pexpect.spawn("az",["containerapp","exec","-n","ca-cutover-test-demo-api","-g","ama","--replica",REP],encoding="utf-8",timeout=900,dimensions=(50,60000))
c.expect(r"[#\$] ",timeout=120)
def sh(cmd,t=60):
    c.sendline(cmd); c.expect(r"DONE\d+",timeout=t)
c.sendline("stty -echo; PS1=''; echo READY"); c.expect("READY")
sh("rm -f /scratch/d216.b64; echo DONE1")
for i in range(0,len(blob),900):
    sh("printf %s '"+blob[i:i+900]+"' >> /scratch/d216.b64; echo DONE2")
sh("wc -c < /scratch/d216.b64; echo DONE3")
print("staged",c.before.strip()[-30:],"expected",len(blob))
sh("echo "+base64.b64encode(boot.encode()).decode()+" | base64 -d > /scratch/b.py; echo DONE4")
c.sendline("python3 /scratch/b.py; echo DONE5")
c.expect(r"DONE5",timeout=850)
out=c.before.replace("\r","").replace("\n","")
open("execall.log","w").write(c.before[-3000:])
ms=re.findall(r"RESULT216 (\S+) ENDRESULT216",out)
for i,m in enumerate(ms): open(f"raw{i}.json","wb").write(base64.b64decode(m))
print("results",len(ms))
c.sendline("exit")
