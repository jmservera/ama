"""Live demo probe for issue 531 criterion 7 (loading feedback and HAX briefing). Credentials read at runtime, never printed.

Synthetic simulations are labelled: route holds/aborts only delay or block requests in the browser; the server is not changed.
"""
import hashlib, json, os, re, time
from playwright.sync_api import sync_playwright

APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
OUT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.abspath(os.path.join(OUT, "../../../../../src/api/src/zava_forward/api/web"))
home = os.path.expanduser("~")
rd = lambda n: open(os.path.join(home, n)).read().split("\n")[0].strip()
USER, PW = rd(".ama-test-user-id"), rd(".ama-test-user")
AXE = open(os.path.join(home, ".local/share/ama/phase-witness/axe.min.js")).read()
EMAIL = re.compile(r"[\w.+-]+@[\w.-]+")
res = {"steps": []}


def clean(t):
    t = EMAIL.sub("[email]", t or "")
    return t.replace(USER, "[user]")


def step(name, **kw):
    res["steps"].append({"step": name, **kw})
    print(name, json.dumps(kw)[:300], flush=True)


def login(page):
    page.fill("input[name=loginfmt]", USER); page.click("#idSIButton9")
    page.wait_for_selector("input[name=passwd]", timeout=30000)
    page.fill("input[name=passwd]", PW); page.click("#idSIButton9")
    page.wait_for_selector("#idSIButton9"); page.click("#idSIButton9")
    page.wait_for_url(re.compile("^" + re.escape(APP)), timeout=60000, wait_until="commit")
    page.wait_for_timeout(3000)


def open_workbench(pg):
    pg.goto(APP + "/", wait_until="networkidle")
    pg.get_by_text("Sign in to the workbench").first.click(); pg.wait_for_timeout(3000)
    pg.locator("[data-test-id], .table-row, .tile").first.click()
    pg.wait_for_url(lambda u: u.startswith(APP + "/app"), timeout=60000)
    pg.wait_for_selector(".briefing [data-record-id]", timeout=90000)


def shot(pg, name):
    pg.screenshot(path=os.path.join(OUT, name))


def run_axe(pg, selector):
    return pg.evaluate(AXE + """;(async(sel)=>{const r=await axe.run(document.querySelector(sel),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return {version:axe.version,violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.length})),passes:r.passes.length}})""" + f"({json.dumps(selector)})")


with sync_playwright() as p:
    b = p.chromium.launch()
    c = b.new_context(viewport={"width": 1366, "height": 900}); pg = c.new_page()
    pg.goto(APP + "/api/me", wait_until="domcontentloaded"); login(pg)
    state = c.storage_state()

    # Deployed assets versus this branch (main at 9f175bd3d).
    parity = {}
    for f in ("workspace-shell.js", "app.js", "async-action.js", "style.css"):
        r = c.request.get(f"{APP}/{f}")
        local = open(os.path.join(WEB, f), "rb").read()
        parity[f] = {"status": r.status, "match": r.status == 200 and hashlib.sha256(r.body()).hexdigest() == hashlib.sha256(local).hexdigest()}
    step("asset_parity_with_branch", **parity)

    # P1: static shell before scripts run (JavaScript disabled) and with app.js held (cold-start simulation).
    nojs = b.new_context(viewport={"width": 1366, "height": 900}, storage_state=state, java_script_enabled=False); npg = nojs.new_page()
    npg.goto(APP + "/app", wait_until="domcontentloaded")
    step("shell_without_javascript", heading=npg.inner_text("#startup h1"), status=npg.inner_text("#startup-status"),
         role=npg.get_attribute("#startup-status", "role"), live=npg.get_attribute("#startup-status", "aria-live"),
         noscript_text_in_dom="JavaScript is required" in npg.content(), body_blank=len(npg.inner_text("body").strip()) == 0)
    shot(npg, "shell-no-javascript-1366.png"); nojs.close()

    hold = b.new_context(viewport={"width": 1366, "height": 900}, storage_state=state); hp = hold.new_page()
    held = []
    hp.route("**/app.js*", lambda route: held.append(route))
    t0 = time.time()
    hp.goto(APP + "/app", wait_until="commit")
    hp.wait_for_selector("#startup-status", timeout=20000)
    snap = lambda: dict(t=round(time.time() - t0, 1), status=hp.inner_text("#startup-status"), retry_visible=hp.locator("#startup-retry").is_visible(),
                        retry_name=hp.locator("#startup-retry").inner_text(), live=hp.get_attribute("#startup-status", "aria-live"),
                        role=hp.get_attribute("#startup-status", "role"), body_chars=len(hp.inner_text("body").strip()))
    step("coldstart_sim_t_initial", **snap()); shot(hp, "coldstart-sim-initial-1366.png")
    hp.wait_for_timeout(5000); step("coldstart_sim_after_slow_threshold", **snap()); shot(hp, "coldstart-sim-slow-1366.png")
    hp.wait_for_timeout(11000); step("coldstart_sim_after_deadline", **snap()); shot(hp, "coldstart-sim-deadline-1366.png")
    for r in held: r.continue_()
    try:
        hp.wait_for_selector("#startup", state="detached", timeout=90000)
        hp.wait_for_selector(".briefing [data-record-id]", timeout=90000)
        step("coldstart_sim_released", shell_removed=True, briefing_visible=True, t=round(time.time() - t0, 1))
    except Exception as e:
        step("coldstart_sim_released", error=str(e)[:200])
    hold.close()

    # P2 main briefing on the live page.
    pg = c.new_page(); pg.goto(APP + "/app", wait_until="domcontentloaded"); open_workbench(pg); pg.wait_for_timeout(1500)
    br = pg.locator(".briefing")
    info = pg.evaluate("""()=>{const b=document.querySelector('.briefing');const t=e=>e?(e.textContent||'').trim():null;
      return {heading:t(b.querySelector('h2')),status:t(b.querySelector('.briefing-status')),aiLabel:t(b.querySelector('.ai-label')),
       basis:[...b.querySelectorAll('.briefing-basis dt')].map((d,i)=>d.textContent+': '+b.querySelectorAll('.briefing-basis dd')[i].textContent),
       prepared:t(b.querySelector('time')),preparedDatetime:b.querySelector('time')?.getAttribute('datetime'),
       sectionHeading:[...b.querySelectorAll('h3')].map(t),
       statements:b.querySelectorAll('.briefing-statements > li').length,
       sourceSummaries:[...b.querySelectorAll('details > summary')].map(t),
       notReviewed:b.querySelector('[data-record-id]')?.dataset.reviewState,
       draftLabel:[...b.querySelectorAll('p')].map(t).filter(x=>/not approved/i.test(x)).slice(0,3),
       confidence:[...b.querySelectorAll('p')].map(t).filter(x=>/Confidence/.test(x)),
       buttons:[...b.querySelectorAll('button')].filter(x=>x.offsetParent).map(t),
       toggleOptions:[...b.querySelectorAll('select option, input[type=radio]')].map(x=>x.textContent||x.value),
       textareasVisible:[...b.querySelectorAll('textarea')].filter(x=>x.offsetParent).length}}""")
    info = json.loads(clean(json.dumps(info)))
    step("briefing_structure", **info)
    shot(pg, "briefing-live-1366.png")
    first = br.locator("details").first
    first.locator("summary").click()
    links = first.evaluate("""d=>[...d.querySelectorAll('li')].map(li=>({text:li.textContent.trim().slice(0,160),links:[...li.querySelectorAll('a')].map(a=>a.getAttribute('href'))}))""")
    step("source_list_expanded", sources=json.loads(clean(json.dumps(links)))); br.scroll_into_view_if_needed(); shot(pg, "briefing-source-expanded-1366.png")

    # P3 review controls: explicit wording, text box only where needed, reason required; nothing submitted.
    reviews = []
    pg.on("request", lambda r: reviews.append(r.url) if "/api/ai/review/" in r.url else None)
    grp = br.get_by_role("group", name="Review this draft")
    step("review_controls_initial", group_visible=grp.is_visible(), buttons=[x.inner_text() for x in grp.get_by_role("button").all()], textareas_visible=br.locator("textarea:visible").count())
    br.get_by_role("button", name="Edit this draft", exact=True).click()
    step("edit_opened", labels=[x.inner_text() for x in br.locator("label:visible").all()], textareas=br.locator("textarea:visible").count(),
         submit=[x.inner_text() for x in br.locator("button:visible").all()])
    save = br.get_by_role("button", name="Save edited draft review", exact=True); save.click(); pg.wait_for_timeout(500)
    reason = br.get_by_label("Reason", exact=True)
    step("edit_empty_reason_refused", aria_invalid=reason.get_attribute("aria-invalid"), focused=reason.evaluate("e=>e===document.activeElement"), review_requests=len(reviews))
    shot(pg, "briefing-edit-open-1366.png")
    br.get_by_role("button", name="Cancel review", exact=True).click(); pg.wait_for_timeout(300)
    br.get_by_role("button", name="Do not use this draft", exact=True).click()
    step("reject_opened", labels=[x.inner_text() for x in br.locator("label:visible").all()], edited_draft_hidden=br.get_by_label("Edited draft", exact=True).is_hidden(),
         submit=[x.inner_text() for x in br.locator("button:visible").all()])
    br.get_by_role("button", name="Record rejection", exact=True).click(); pg.wait_for_timeout(500)
    step("reject_empty_reason_refused", aria_invalid=br.get_by_label("Reason", exact=True).get_attribute("aria-invalid"), review_requests=len(reviews))
    br.get_by_role("button", name="Cancel review", exact=True).click(); pg.wait_for_timeout(300)
    step("review_cancelled_no_submission", review_requests=len(reviews), group_visible=grp.is_visible())

    # P4 async feedback: hold /api/briefing on refresh.
    held2 = []
    pg.route("**/api/briefing*", lambda route: held2.append(route))
    br.get_by_role("button", name="Refresh briefing", exact=True).click(); pg.wait_for_timeout(80)
    early = dict(status=clean(br.locator(".briefing-status").inner_text()), content_busy=br.locator("> *[aria-busy=true]").count(),
                 spinner=pg.locator(".briefing .async-spinner, .async-feedback .async-spinner").count(), toggle_disabled=pg.evaluate("[...document.querySelectorAll('.briefing select, .briefing input')].map(e=>e.disabled)"))
    pg.wait_for_timeout(500)
    late = dict(spinner=pg.locator(".async-feedback .async-spinner").count(), feedback=[clean(x.inner_text()) for x in pg.locator(".async-feedback").all()],
                workspace_status=clean(pg.inner_text("#workspace-status")), aria_busy=pg.evaluate("!!document.querySelector('.briefing [aria-busy=true]')"))
    step("refresh_pending_feedback", early=early, after_500ms=late); shot(pg, "briefing-refresh-pending-1366.png")
    for r in held2: r.continue_()
    pg.wait_for_function("()=>!document.querySelector('.briefing [aria-busy=true]')", timeout=60000)
    step("refresh_finished", status=clean(br.locator(".briefing-status").inner_text()))
    pg.unroute("**/api/briefing*")

    # P5 unverified / AI labelling: SIMULATED by rewriting the live /api/briefing response in the browser.
    def mutate(route):
        r = route.fetch(); j = r.json()
        j["source"] = "ai"; j["verified"] = False; j["validated"] = False
        for s in j.get("statements", [])[:1]:
            s["unresolved"] = ["ZF-SIM-0000: Stage"]
        route.fulfill(response=r, json=j)
    pg.route("**/api/briefing*", mutate)
    br.get_by_role("button", name="Refresh briefing", exact=True).click(); pg.wait_for_timeout(4000)
    sim = pg.evaluate("""()=>{const b=document.querySelector('.briefing');const t=e=>e?(e.textContent||'').trim():null;return {aiLabel:t(b.querySelector('.ai-label')),
      h3:[...b.querySelectorAll('h3')].map(t),wording:[...b.querySelectorAll('.briefing-basis dd')].map(t),
      unverified:[...b.querySelectorAll('.flag, .err, [role=status]')].map(t).filter(x=>/Unverified|do not match/.test(x||''))}}""")
    step("simulated_ai_unverified_rendering", note="SIMULATION: live response rewritten in the browser; no server AI call", **json.loads(clean(json.dumps(sim))))
    shot(pg, "briefing-simulated-ai-unverified-1366.png")
    pg.unroute("**/api/briefing*")

    # P6 axe and reduced motion on the live briefing (back to the real response).
    br.get_by_role("button", name="Refresh briefing", exact=True).click(); pg.wait_for_timeout(4000)
    step("axe_wcag22aa_briefing", **run_axe(pg, ".briefing"))
    step("axe_wcag22aa_page", **run_axe(pg, "body"))
    pg.emulate_media(reduced_motion="reduce")
    rm = pg.evaluate("""()=>{const s=document.createElement('span');s.className='async-spinner';document.body.append(s);const cs=getComputedStyle(s);const o={name:cs.animationName,dur:cs.animationDuration,count:cs.animationIterationCount};s.remove();return o}""")
    pg.emulate_media(reduced_motion="no-preference")
    nm = pg.evaluate("""()=>{const s=document.createElement('span');s.className='async-spinner';document.body.append(s);const cs=getComputedStyle(s);const o={name:cs.animationName,dur:cs.animationDuration,count:cs.animationIterationCount};s.remove();return o}""")
    step("spinner_reduced_motion", reduce=rm, no_preference=nm)

    # P7 script retry and persistent failure: ops.js blocked in the browser; open a case.
    cid = pg.evaluate("""async()=>{const r=await fetch('/api/cases');const j=await r.json();return (j.items||j)[0].id}""")
    rc = b.new_context(viewport={"width": 1366, "height": 900}, storage_state=state); rp = rc.new_page()
    ops = []
    rp.route("**/ops.js*", lambda route: (ops.append(route.request.url), route.abort()))
    rp.goto(APP + "/app", wait_until="domcontentloaded"); rp.wait_for_timeout(500)
    try:
        rp.wait_for_selector("#startup", state="detached", timeout=60000)
    except Exception as e:
        step("retry_sim_note", shell_not_removed=str(e)[:100])
    rp.wait_for_timeout(1500)
    rp.evaluate("(id)=>{location.hash='#/case/'+id}", cid)
    seen = []
    for _ in range(40):
        s = clean(rp.inner_text("#workspace-status"))
        if s and (not seen or seen[-1] != s): seen.append(s)
        rp.wait_for_timeout(250)
    errs = clean(" | ".join(x.inner_text() for x in rp.locator("[role=alert], .err").all()))
    step("script_retry_persistent_failure_sim", note="SIMULATION: /ops.js aborted in the browser", ops_requests=len(ops), status_sequence=seen, alerts=errs[:600],
         reload_button=[x.inner_text() for x in rp.get_by_role("button").all() if "eload" in x.inner_text() or "Try" in x.inner_text()])
    shot(rp, "script-retry-failure-1366.png")
    rc.close()
    json.dump(res, open(os.path.join(OUT, "live_531_probe.json"), "w"), indent=1)
    b.close()
