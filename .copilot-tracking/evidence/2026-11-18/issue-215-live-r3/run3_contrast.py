"""Issue 215 run 3: manual contrast-ratio check of the three elements axe reported as incomplete in the home chat dialog. Redacted."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "..", "issue-215-live", "employee_proof.py")).read().split("r = {}")[0]
exec(src)
OUT = HERE
AXE = open(os.environ.get("AXE_JS", "axe.min.js")).read()
TAGS = "{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}}"
r = {}
with sync_playwright() as p:
    b = p.chromium.launch(); c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    pg.goto(APP + "/sign-in", wait_until="domcontentloaded"); pg.wait_for_timeout(3000)
    if pg.locator("text=Pick an account").count(): pg.locator("[data-test-id], .table-row, div[role=button]").first.click()
    pg.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(4000)
    pg.goto(APP + "/app#/case/ZF-2025-0331"); pg.wait_for_timeout(5000)
    pg.locator("#employee-chat-launcher").focus(); pg.keyboard.press("Enter"); pg.wait_for_timeout(3000)
    JS = """()=>{const lum=c=>{const [r,g,b]=c.match(/[\\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*r+0.7152*g+0.0722*b};
    const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;const m=c.match(/[\\d.]+/g);if(m&&(m.length<4||+m[3]>0.99)&&c!=='rgba(0, 0, 0, 0)')return c;e=e.parentElement}return 'rgb(255,255,255)'};
    return ['#chat-demo-disclaimer','#employee-chat-question','#employee-chat-unsupported'].map(s=>{const e=document.querySelector(s);const f=getComputedStyle(e).color,b=bg(e);const a=lum(f),c=lum(b);return {sel:s,fg:f,bg:b,ratio:+((Math.max(a,c)+0.05)/(Math.min(a,c)+0.05)).toFixed(2),size:getComputedStyle(e).fontSize}})}"""
    r["manual_contrast"] = pg.evaluate(JS)
    b.close()
json.dump(r, open(f"{OUT}/run3-contrast.json", "w"), indent=1); print(json.dumps(r, indent=1))
