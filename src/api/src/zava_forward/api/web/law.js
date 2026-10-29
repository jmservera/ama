(function () {
  const out = document.getElementById("law-out");
  const status = document.getElementById("law-status");
  const ready = () => {
    document.getElementById("startup")?.remove();
    document.dispatchEvent(new Event("workspace-ready"));
  };
  const el = (tag, text, cls) => { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (cls) n.className = cls; return n; };
  const get = async (path) => {
    const r = await fetch(path, { credentials: "same-origin" });
    const body = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(body.error || "Could not load.");
    return body;
  };
  const show = (nodes, label) => { ready(); out.replaceChildren(...nodes); status.textContent = label; out.focus(); };
  const meta = (s) => el("p", ["Status: " + s.status, "Completeness: " + s.completeness, "Effective: " + (s.effective || "not stated"), "Retrieved: " + s.retrieved, "Version " + (s.version || "")].join(" | "), "muted");
  const caveats = (s) => (s.caveats || []).map((c) => el("p", c, "banner"));

  async function list() {
    const d = await get("/api/law/sources");
    const nodes = [el("h2", "Sources held")];
    const ul = el("ul");
    d.sources.forEach((s) => {
      const li = el("li"), b = el("button", s.title, "alt");
      b.type = "button";
      b.addEventListener("click", AsyncAction.handler(() => open(s.id).catch(fail)));
      li.append(b, meta(s), ...caveats(s));
      ul.append(li);
    });
    nodes.push(ul, el("h2", "No source held"));
    const gl = el("ul");
    d.gaps.forEach((g) => { const li = el("li"); li.append(el("strong", g.topic), el("p", g.answer + " " + g.reason)); gl.append(li); });
    nodes.push(gl);
    show(nodes, d.sources.length + " sources and " + d.gaps.length + " gaps shown.");
  }
  async function open(id) {
    const d = await get("/api/law/sources/" + encodeURIComponent(id));
    const nodes = [el("h2", d.source.title)];
    const v = d.versions[0];
    nodes.push(el("p", "Official source: " + (d.source.official_url || "not recorded"), "muted"), meta(v), ...caveats(v));
    nodes.push(el("p", "Owner: " + d.source.owner + ". Content hash: " + v.content_hash, "muted"));
    const ul = el("ul");
    d.provisions.forEach((p) => {
      const li = el("li"), b = el("button", p.heading_path, "alt");
      b.type = "button";
      b.addEventListener("click", AsyncAction.handler(() => text(p.id).catch(fail)));
      li.append(b); ul.append(li);
    });
    nodes.push(ul);
    show(nodes, d.provisions.length + " provisions in " + d.source.title + ".");
  }
  async function text(pid) {
    const p = await get("/api/law/provisions/" + encodeURIComponent(pid));
    show([el("h2", p.heading_path), meta(p), ...caveats(p), el("pre", p.text)], "Provision " + p.heading_path + " shown.");
  }
  async function find(q) {
    const d = await get("/api/law/search?q=" + encodeURIComponent(q));
    const nodes = [el("h2", "Search results")];
    d.caveats.forEach((c) => nodes.push(el("p", c, "banner")));
    d.no_source_held.forEach((g) => nodes.push(el("p", g.topic + ": " + g.answer, "banner")));
    if (d.answer) nodes.push(el("p", d.answer));
    const ul = el("ul");
    d.results.forEach((r) => {
      const li = el("li"), b = el("button", r.title + ": " + r.heading_path, "alt");
      b.type = "button";
      b.addEventListener("click", AsyncAction.handler(() => text(r.id).catch(fail)));
      li.append(b); ul.append(li);
    });
    nodes.push(ul);
    show(nodes, d.results.length + " results.");
  }
  const fail = (e) => { ready(); status.textContent = `${e.message}. Try All sources or search again.`; };
  if (typeof AsyncAction === "undefined" || !AsyncAction
      || !["handler", "run"].every(method => typeof AsyncAction[method] === "function")) {
    const message = "Required law viewer file did not load: /async-action.js. Reload this page to try again. If this continues, contact application support.";
    const reload = el("button", "Reload law viewer");
    reload.type = "button";
    reload.addEventListener("click", () => location.reload());
    const error = el("p", message, "err");
    error.setAttribute("role", "alert");
    document.getElementById("law-form").querySelectorAll("input, button").forEach(control => { control.disabled = true; });
    document.getElementById("law-form").addEventListener("submit", event => event.preventDefault());
    show([el("h2", "Law viewer unavailable"), error, reload], message);
    return;
  }
  document.getElementById("law-all").addEventListener("click", AsyncAction.handler(() => list().catch(fail)));
  document.getElementById("law-form").addEventListener("submit", AsyncAction.handler((e) => { e.preventDefault(); return find(document.getElementById("law-q").value).catch(fail); }));
  AsyncAction.run(null, () => list().catch(fail), "Loading sources");
}());
