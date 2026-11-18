import sys, threading, http.server, functools, json
from playwright.sync_api import sync_playwright
WEB="."
h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=WEB)
srv=http.server.ThreadingHTTPServer(("127.0.0.1",0),h); port=srv.server_address[1]
threading.Thread(target=srv.serve_forever,daemon=True).start()
js="""() => { const w=ChatWidget.create({id:'employee-chat',title:'Employee assistant',questionLabel:'Q',skillLabel:'S',resizable:true,stayOpen:true,size:{width:40,height:80}});
 w.beforeInput.append(w.node('small','Do not enter personal or sensitive resident information. Chat cannot approve or change records.',{id:'employee-chat-entry-warning',class:'chat-widget-meta'}));
 w.select.append(w.node('option','General work help',{value:'general'})); w.open(); w.fail && w.fail("Type a question first."); w.setStatus && w.setStatus("Asking the assistant."); document.querySelector("#employee-chat-question").value="abcd"; }"""
with sync_playwright() as p:
  b=p.chromium.launch()
  for vp in [(1366,900),(1366,700),(1280,720),(1920,1080)]:
    pg=b.new_page(viewport={"width":vp[0],"height":vp[1]})
    pg.goto(f"http://127.0.0.1:{port}/chat-widget-harness.html")
    pg.evaluate(js); pg.wait_for_timeout(300)
    r=pg.evaluate("""()=>{const f=document.getElementById('employee-chat-keys'),c=f.closest('form'),t=c.querySelector('.chat-widget-tools');
      const fr=f.getBoundingClientRect(),cr=c.getBoundingClientRect(),tr=t.getBoundingClientRect();
      const x=(fr.left+fr.right)/2,y=(fr.top+fr.bottom)/2; const top=document.elementFromPoint(x,y);
      const pr=document.getElementById("employee-chat").getBoundingClientRect();return {panel:[pr.top,pr.bottom],keys:[fr.top,fr.bottom],form:[cr.top,cr.bottom],tools:[tr.top,tr.bottom],formScroll:[c.scrollHeight,c.clientHeight],hitIsKeys:top===f,sc:c.scrollTop,hit:top&&top.tagName+'.'+top.className}}""")
    print(vp,json.dumps(r)); pg.screenshot(path=f"repro-{vp[0]}x{vp[1]}.png")
  b.close()
