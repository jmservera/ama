import json
from api import H, session
JS="""async([m,p,b])=>{const r=await fetch(p,{method:m,headers:{'Content-Type':'application/json','X-ZF-CSRF':'1'},body:b?JSON.stringify(b):undefined});let t=await r.text();try{t=JSON.parse(t)}catch(e){};return [r.status,t]}"""
def open_page():
    pw,c=session(); pg=c.new_page(); pg.goto(H+"/app"); pg.wait_for_load_state("networkidle"); return pw,c,pg
def call(pg,m,p,b=None): return pg.evaluate(JS,[m,p,b])
