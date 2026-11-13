const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[2] + "/role-screens.js", "utf8");
const assert = require("node:assert");
const row = (n) => ({id: "C-" + n, address: n + " Test Street", work: {owner: "Owen", queues: [],
  returned: {reason: "Reason " + n, sender: "Sender"}, handoff: null}});
async function run(total) {
  const calls = [];
  const context = vm.createContext({
    location: {hash: "#/screens?screen=programme-queue"}, history: {replaceState() {}},
    URLSearchParams, Intl, AbortController, Date,
    routeController: new AbortController(), me: {user: {role: "Retrofit Programme Manager"}},
    api: async (path) => {
      calls.push(path);
      if (path.startsWith("/api/coordinator")) return {as_of: "x", audit_integrity: "Intact", funnel: []};
      const offset = Number(new URL(path, "http://x").searchParams.get("offset"));
      const n = Math.max(0, Math.min(50, total - offset));
      return {total, items: Array.from({length: n}, (_, i) => row(offset + i + 1))};
    },
    h: (tag, attrs, ...kids) => {
      const node = {tag, attrs, kids: kids.flat(Infinity).filter(k => k !== false && k !== null && k !== undefined)};
      Object.defineProperty(node, "replaceChildren", {value: (...k) => { node.kids = k; }});
      Object.defineProperty(node, "textContent", {set: (v) => { node.kids = [v]; }});
      return node;
    }
  });
  vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('programme-queue');", context);
  const ov = await context.__s.overview(new AbortController().signal);
  const find = (n, p, o = []) => { if (n && typeof n === "object") { if (p(n)) o.push(n); (n.kids || []).forEach(k => find(k, p, o)); } return o; };
  const btn = (id) => find(ov, n => n.attrs && n.attrs.id === id)[0];
  const txt = (n) => JSON.stringify(n);
  const status = () => JSON.parse(JSON.stringify(find(ov, n => n.attrs && n.attrs.id === "programme-page-status")[0])).kids.join("");
  const rows = () => { const b = find(ov, n => n.tag === "tbody")[0]; return b ? b.kids.length : 0; };
  const settle = () => new Promise(r => setTimeout(r, 0));
  const pageCalls = () => calls.filter(c => c.startsWith("/api/cases")).length;
  const attrsOf = (id) => { const b = btn(id); if (!b) return null;
    const a = {...b.attrs}; delete a.onclick; return {attrs: a, hasDisabled: "disabled" in b.attrs, hasAriaDisabled: "aria-disabled" in b.attrs, label: b.kids.join("")}; };
  const snap = (label) => ({label, status: status(), prev: attrsOf("programme-prev"), next: attrsOf("programme-next")});
  const out = [];
  out.push(snap("page1"));
  return {ov, btn, status, rows, settle, pageCalls, snap, out, txt};
}
(async () => {
  const res = {};
  // 120 cases: pages at offset 0, 50, 100
  const t = await run(120);
  res.start = t.snap("start");
  assert.match(res.start.status, /Showing cases 1 to 50 of 120/);
  assert.strictEqual(t.rows(), 50);
  let c0 = t.pageCalls(); t.btn("programme-prev").attrs.onclick(); await t.settle();
  res.prevAtStartCalls = t.pageCalls() - c0; assert.strictEqual(res.prevAtStartCalls, 0);
  t.btn("programme-next").attrs.onclick(); await t.settle();
  res.middle = t.snap("middle");
  assert.match(res.middle.status, /Showing cases 51 to 100 of 120/);
  assert.ok(t.txt(t.ov).includes("Reason 51"));
  t.btn("programme-next").attrs.onclick(); await t.settle();
  res.last = t.snap("last");
  assert.match(res.last.status, /Showing cases 101 to 120 of 120/);
  assert.strictEqual(t.rows(), 20);
  c0 = t.pageCalls(); t.btn("programme-next").attrs.onclick(); await t.settle();
  res.nextAtEndCalls = t.pageCalls() - c0; assert.strictEqual(res.nextAtEndCalls, 0);
  assert.match(t.status(), /Showing cases 101 to 120 of 120/);
  t.btn("programme-prev").attrs.onclick(); await t.settle();
  assert.match(t.status(), /Showing cases 51 to 100 of 120/);
  // empty and single page: no pager
  for (const total of [0, 50]) {
    const e = await run(total);
    res["total" + total] = {status: e.status(), prev: e.btn("programme-prev") || null, next: e.btn("programme-next") || null, rows: e.rows()};
    assert.strictEqual(res["total" + total].prev, null);
    assert.strictEqual(res["total" + total].next, null);
  }
  assert.match(res.total0.status, /Showing cases 0 to 0 of 0/);
  assert.match(res.total50.status, /Showing cases 1 to 50 of 50/);
  console.log(JSON.stringify(res, null, 1));
})().catch(e => { console.error(e); process.exitCode = 1; });
