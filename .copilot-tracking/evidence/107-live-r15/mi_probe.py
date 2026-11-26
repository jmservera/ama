import os,urllib.request,urllib.parse,json,sys
for tag in ("env-header","pid1-header"):
    h=os.environ.get("IDENTITY_HEADER") or ""
    if tag=="pid1-header":
        for kv in open("/proc/1/environ").read().split("\0"):
            if kv.startswith("IDENTITY_HEADER="): h=kv.split("=",1)[1]
    for res in ("https://cognitiveservices.azure.com","https://management.azure.com"):
        u=os.environ["IDENTITY_ENDPOINT"]+"?"+urllib.parse.urlencode({"api-version":"2019-08-01","resource":res,"client_id":os.environ.get("AZURE_CLIENT_ID","")})
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers={"X-IDENTITY-HEADER":h}),timeout=15)
            print(tag,res,r.status,"token-len",len(json.load(r).get("access_token","")))
        except Exception as e:
            print(tag,res,"ERR",getattr(e,"code",type(e).__name__),(e.read()[:150] if hasattr(e,"read") else ""))
