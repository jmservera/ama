"""Capture-free /api/me predicate for owner-authorized employee acceptance runners."""

BINDING = r"""async expected => {
  const out = {expectationValid:false, responseOk:false, schemaValid:false,
    providerMatches:false, expectedIdentity:false, employeeRole:false,
    notViewOnly:false, displayEmailMatches:false, rosterBound:false,
    transportFailed:false, jsonFailed:false, authenticated:false};
  const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
  const guid = x => typeof x === 'string' && x.length === 36 &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(x);
  out.expectationValid = object(expected) && guid(expected.tid) && guid(expected.oid);
  if (!out.expectationValid) return out;
  let r;
  try {
    r = await fetch('/api/me', {redirect:'error', signal:AbortSignal.timeout(120000)});
  } catch {
    out.transportFailed = true;
    return out;
  }
  out.responseOk = r.status === 200 && r.redirected === false &&
    (r.headers.get('content-type') || '').split(';')[0].trim().toLowerCase() ===
      'application/json';
  if (!out.responseOk) return out;
  let d;
  try {
    d = await r.json();
  } catch {
    out.jsonFailed = true;
    return out;
  }
  const u = object(d) && object(d.user) ? d.user : {};
  const a = object(d) && object(d.account) ? d.account : {};
  out.schemaValid = object(d) && object(d.user) && object(d.account) &&
    typeof a.email === 'string' && typeof u.code === 'string' && !!u.code &&
    typeof u.email === 'string' && !!u.email && guid(u.tid) && guid(u.oid) &&
    u.identity_source === 'entra' && typeof u.view_only === 'boolean' &&
    Array.isArray(u.app_roles) && u.app_roles.every(role => typeof role === 'string');
  out.providerMatches = a.provider === 'trusted-proxy' && u.auth_provider === 'trusted-proxy';
  out.expectedIdentity = guid(u.tid) && guid(u.oid) &&
    u.tid.toLowerCase() === expected.tid.toLowerCase() &&
    u.oid.toLowerCase() === expected.oid.toLowerCase();
  out.employeeRole = u.role === 'Retrofit Programme Manager' &&
    Array.isArray(u.app_roles) && u.app_roles.includes('ZavaForward.ProgrammeManager');
  out.notViewOnly = u.view_only === false;
  out.displayEmailMatches = typeof a.email === 'string' && !!a.email.trim() &&
    typeof expected.email === 'string' && !!expected.email.trim() &&
    a.email.trim().toLowerCase() === expected.email.trim().toLowerCase();
  out.rosterBound = object(u.bound) && typeof u.bound.code === 'string' &&
    !!u.bound.code && typeof u.bound.email === 'string' && !!u.bound.email;
  out.authenticated = out.schemaValid && out.providerMatches && out.expectedIdentity &&
    out.employeeRole && out.notViewOnly;
  return out;
}"""
