import { AppError, commands } from './domain.mjs';

export const prohibitedActions = commands.map(item => item.action);
export function currentEvidence(home) {
  const f = home.facts;
  const referenced = [f.assessment.evidenceId, f.installation?.evidenceId,
    f.quality?.evidenceId, f.handover?.evidenceId];
  return home.evidence.filter(item => ['stock', 'hazard'].includes(item.kind)
    || (item.kind === 'design' && item.version === f.design?.version)
    || referenced.includes(item.id));
}
export function validateDraft(draft, home) {
  const keys = ['mode', 'status', 'citations', 'findings', 'draft', 'prohibitedActions'];
  if (!draft || Object.keys(draft).length !== keys.length || Object.keys(draft).some(key => !keys.includes(key))
    || draft.mode !== 'simulator' || draft.status !== 'draft' || typeof draft.draft !== 'string'
    || !Array.isArray(draft.findings) || !Array.isArray(draft.citations)
    || !Array.isArray(draft.prohibitedActions)
    || draft.prohibitedActions.length !== prohibitedActions.length
    || prohibitedActions.some(action => !draft.prohibitedActions.includes(action))
    || draft.findings.some(item => !item || Object.keys(item).sort().join(',') !== 'code,message,owner'
      || !['code', 'message', 'owner'].every(key => typeof item[key] === 'string'))) {
    throw new AppError(503, 'ASSISTANT_INVALID', 'Simulator output failed its closed schema.', home.owner);
  }
  const sources = new Set(currentEvidence(home).map(item => item.id));
  if (!draft.citations.length || draft.citations.some(id => typeof id !== 'string' || !sources.has(id))) {
    throw new AppError(503, 'ASSISTANT_INVALID', 'Draft citations do not resolve against current case evidence.', home.owner);
  }
  if (prohibitedActions.some(action => draft.draft.includes(action))) {
    throw new AppError(503, 'ASSISTANT_INVALID', 'Draft contained a prohibited command instruction.', home.owner);
  }
  return draft;
}
export function buildDraft(home) {
  const approved = currentEvidence(home);
  const findings = home.blockers.map(item => ({ code: item.code, message: item.message, owner: item.owner }));
  const draft = {
    mode: 'simulator', status: 'draft', citations: approved.map(item => item.id), findings,
    draft: `Synthetic review draft for ${home.id} at ${home.stage}. ${findings.length ? `${findings.length} current predicate(s) require named human review.` : 'No current lifecycle blocker found in this constructed record.'} Evidence references require human review. This deterministic simulator has made no approval, contact, payment, claim or safety decision.`,
    prohibitedActions,
  };
  return validateDraft(draft, home);
}
export function runAssistant(store, id, role, body, generator = buildDraft) {
  if (!body || typeof body !== 'object' || Array.isArray(body) || Object.keys(body).length !== 1 ||
    !['draft', 'disabled', 'failure'].includes(body.mode)) throw new AppError(400, 'INVALID_PAYLOAD', 'Assistant accepts only mode: draft, disabled or failure.');
  const home = store.detail(id, role);
  if (body.mode === 'draft') {
    try { return validateDraft(generator(home), home); }
    catch (error) {
      const task = store.fallback(id, role, 'failure');
      throw new AppError(503, 'ASSISTANT_INVALID', 'Simulator failed validation. Manual evidence review is required.', task.owner, { taskId: task.id });
    }
  }
  const task = store.fallback(id, role, body.mode);
  throw new AppError(503, body.mode === 'disabled' ? 'ASSISTANT_DISABLED' : 'ASSISTANT_UNAVAILABLE',
    'Simulator is unavailable; an owned manual-review task is recorded. No completion or approval was generated.',
    task.owner, { taskId: task.id });
}
