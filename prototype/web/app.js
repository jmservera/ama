// Minimal read-only client for the workbench API health and proposal list. Authority stays server-side.
async function health(base) {
  const res = await fetch(`${base}/healthz`);
  return res.json();
}
if (typeof module !== 'undefined') module.exports = { health };
