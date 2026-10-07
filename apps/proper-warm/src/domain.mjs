import { randomUUID } from 'node:crypto';

export const roles = ['programme_manager', 'data_owner', 'assessor', 'coordinator',
  'resident_officer', 'contract_manager', 'safety_officer', 'quality_reviewer',
  'finance', 'viewer', 'contractor'];
export const lifecycle = ['candidate', 'assessed', 'designed', 'resident_ready',
  'scheduled', 'installed', 'quality_accepted', 'handed_over'];
export const workflows = [
  ['prioritisation', 'Stock and prioritisation'], ['technical_readiness', 'Technical readiness'],
  ['resident_service', 'Resident service and access'], ['capacity', 'Supplier capacity'],
  ['hazards', 'Hazard referral'], ['quality', 'Quality and defects'],
  ['finance_grants', 'Finance and grants'], ['handoffs', 'Controlled handoffs'],
  ['portfolio', 'Portfolio and investment'],
].map(([id, label]) => ({ id, label }));

const field = (key, type, options, defaultValue) => ({
  key, type, ...(options ? { options } : {}), ...(defaultValue !== undefined ? { default: defaultValue } : {}),
});
const text = key => field(key, 'string');
const version = key => field(key, 'integer', undefined, 1);
const boolean = key => field(key, 'boolean', undefined, true);
const enumeration = (key, options) => field(key, 'string', options, options[0]);
const command = (action, permitted, fields = []) => ({
  action, label: action.replaceAll('_', ' '), roles: permitted,
  fields: [...fields, field('reason', 'string', undefined, 'Synthetic exercise decision'),
    field('source', 'string', undefined, 'EX-SOURCE-DEMO')],
});
export const commands = [
  command('resolve_conflict', ['data_owner'], [text('value')]),
  command('submit_assessment', ['assessor'], [text('evidenceId')]),
  command('approve_assessment', ['coordinator'], [text('evidenceId')]),
  command('approve_design', ['coordinator'], [version('designVersion')]),
  command('record_decision', ['resident_officer'], [
    enumeration('decision', ['accepted', 'declined', 'withdrawn']), field('measure', 'string', undefined, 'insulation'),
    version('designVersion')]),
  command('approve_package', ['finance'], [boolean('budgetApproved'), boolean('fundingConfirmed'), boolean('contractApproved')]),
  command('commit_capacity', ['contract_manager'], [field('slots', 'integer', undefined, 1), version('packageVersion')]),
  command('release_work', ['programme_manager'], [version('packageVersion')]),
  command('record_installation', ['contractor'], [text('evidenceId'), version('designVersion')]),
  command('record_quality', ['quality_reviewer'], [
    enumeration('outcome', ['accepted', 'returned']), text('evidenceId'), version('designVersion')]),
  command('accept_handover', ['quality_reviewer'], [text('evidenceId')]),
  command('match_invoice', ['finance'], [boolean('matched')]),
  command('record_grant', ['finance'], [
    enumeration('state', ['opportunity', 'awarded', 'claimed', 'received']), field('amount', 'number', undefined, 0)]),
  command('send_handoff', roles.filter(role => role !== 'viewer'), [enumeration('destination', roles.filter(role => role !== 'viewer'))]),
  ...['receive_handoff', 'accept_handoff', 'return_handoff'].map(action =>
    command(action, roles.filter(role => role !== 'viewer'), [text('handoffId')])),
  command('set_update', ['resident_officer'], [field('dueAt', 'datetime')]),
  command('record_appointment', ['resident_officer'], [text('appointmentId'), boolean('confirmed'), boolean('verified'),
    enumeration('outcome', ['resident_no_access', 'provider_no_show', 'cancelled', 'rescheduled', 'kept'])]),
  command('acknowledge_referral', ['safety_officer'], [text('referralId')]),
  command('return_case', ['coordinator', 'quality_reviewer'], [enumeration('target', ['assessed', 'installed'])]),
  command('advance', ['programme_manager']),
];
export const config = {
  roles, workflows, lifecycle, commands,
  banner: 'Synthetic local-only PoC. Demo roles are impersonation, not authentication. No live AI, safety decision, resident contact, payment or grant submission.',
};

export class AppError extends Error {
  constructor(status, code, message, owner = 'programme_manager', details = []) {
    super(message);
    Object.assign(this, { status, code, owner, details });
  }
}
const fail = (message, owner, code = 'GATE_BLOCKED') => {
  throw new AppError(422, code, message, owner, [{ code, message, owner }]);
};
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const nonempty = value => typeof value === 'string' && value.trim().length > 0 && value.length <= 4096;
export function validateRole(role) {
  if (!roles.includes(role)) throw new AppError(403, 'FORBIDDEN', 'Unknown demo role.');
}
export function validateEnvelope(envelope, role) {
  validateRole(role);
  if (!object(envelope) || Object.keys(envelope).some(key => !['action', 'expectedVersion', 'idempotencyKey', 'payload'].includes(key))
    || !Number.isSafeInteger(envelope.expectedVersion) || envelope.expectedVersion < 1
    || !nonempty(envelope.idempotencyKey) || envelope.idempotencyKey.length > 128) {
    throw new AppError(400, 'INVALID_PAYLOAD', 'Expected action, positive expectedVersion, idempotencyKey and closed payload.');
  }
  const spec = commands.find(item => item.action === envelope.action);
  if (!spec) throw new AppError(400, 'INVALID_PAYLOAD', 'Unknown command.');
  if (!spec.roles.includes(role)) throw new AppError(403, 'FORBIDDEN', 'Role cannot perform this exercise command.', spec.roles[0]);
  const payload = envelope.payload;
  if (!object(payload) || Object.keys(payload).length !== spec.fields.length ||
    Object.keys(payload).some(key => !spec.fields.some(item => item.key === key))) {
    throw new AppError(400, 'INVALID_PAYLOAD', 'Payload must contain exactly the configured fields.');
  }
  for (const item of spec.fields) {
    const value = payload[item.key];
    const valid = item.type === 'string' ? nonempty(value)
      : item.type === 'boolean' ? typeof value === 'boolean'
        : item.type === 'integer' ? Number.isSafeInteger(value) && value > 0
          : item.type === 'number' ? typeof value === 'number' && Number.isFinite(value) && value >= 0
            : item.type === 'datetime' ? nonempty(value) && /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(value) && Number.isFinite(Date.parse(value)) : false;
    if (!valid || (item.options && !item.options.includes(value))) {
      throw new AppError(400, 'INVALID_PAYLOAD', `Invalid ${item.key}.`);
    }
  }
  return spec;
}

export function allowedActions(home, role) {
  return commands.filter(item => {
    if (!item.roles.includes(role)) return false;
    if (item.action === 'send_handoff') return home.owner === role;
    if (['receive_handoff', 'accept_handoff', 'return_handoff'].includes(item.action)) return home.handoff?.destination === role;
    return true;
  }).map(item => item.action);
}

const blocker = (code, message, owner) => ({ code, message, owner });
export function blockers(home, destination = lifecycle[lifecycle.indexOf(home.stage) + 1]) {
  const f = home.facts;
  const required = lifecycle.indexOf(destination);
  const result = [];
  if (f.hazard.hold) result.push(blocker('SAFETY_HOLD', 'Linked hazard hold requires the separate safety response; this app cannot clear it.', 'safety_officer'));
  if (required >= 1) {
    if (!f.conflict.resolved) result.push(blocker('DATA_CONFLICT', 'Reconcile conflicting stock evidence.', 'data_owner'));
    if (!f.assessment.submitted) result.push(blocker('ASSESSMENT_MISSING', 'Assessment evidence has not been submitted.', 'assessor'));
    if (!f.assessment.approved) result.push(blocker('ASSESSMENT_APPROVAL', 'Separate coordinator assessment approval is required.', 'coordinator'));
  }
  if (required >= 2 && !f.design?.approved) result.push(blocker('DESIGN_APPROVAL', 'Current design requires coordinator approval.', 'coordinator'));
  if (required >= 3 && !(f.decision?.decision === 'accepted' && f.decision.designVersion === f.design?.version && f.decision.measure === f.measure)) {
    result.push(blocker('RESIDENT_DECISION', 'Accepted measure-specific resident decision against the current design is required.', 'resident_officer'));
  }
  if (required >= 4) {
    if (!(f.package.budgetApproved && f.package.fundingConfirmed && f.package.contractApproved)) {
      result.push(blocker('PACKAGE_APPROVAL', 'Finance budget, funding and contract approvals are required.', 'finance'));
    }
    if (!(f.capacity?.slots > 0 && f.capacity.packageVersion === f.package.version)) {
      result.push(blocker('CAPACITY_COMMITMENT', 'Committed capacity must match the current package version.', 'contract_manager'));
    }
    if (!(f.release?.approved && f.release.packageVersion === f.package.version && f.release.designVersion === f.design?.version)) {
      result.push(blocker('WORK_RELEASE', 'Explicit programme-manager release is required.', 'programme_manager'));
    }
  }
  if (required >= 5 && !(f.installation?.evidenceId && f.installation.designVersion === f.design?.version)) {
    result.push(blocker('INSTALLATION_EVIDENCE', 'Provider installation evidence must match the current design.', 'contractor'));
  }
  if (required >= 6 && !(f.quality?.outcome === 'accepted' && f.quality.designVersion === f.design?.version)) {
    result.push(blocker('QUALITY_ACCEPTANCE', 'Independent current-design quality acceptance and defect resolution are required.', 'quality_reviewer'));
  }
  if (required >= 7) {
    if (!f.handover?.accepted) result.push(blocker('HANDOVER_ACCEPTANCE', 'Separate handover acceptance is required.', 'quality_reviewer'));
    if (!f.invoice.matched) result.push(blocker('INVOICE_MATCH', 'Invoice reconciliation is required.', 'finance'));
    if (!home.residentUpdate.dueAt) result.push(blocker('UPDATE_COMMITMENT', 'Resident-update commitment needs a due date.', 'resident_officer'));
  }
  return result;
}
function requireGates(home, destination, excluded = []) {
  const failures = blockers(home, destination).filter(item => !excluded.includes(item.code));
  if (failures.length) throw new AppError(422, 'GATE_BLOCKED', 'Current lifecycle predicates are not satisfied.', failures[0].owner, failures);
}
function addTask(home, kind, owner, message, timestamp) {
  if (!home.tasks.some(task => task.kind === kind && task.status === 'open')) {
    home.tasks.push({ id: `EX-TASK-${randomUUID()}`, kind, owner, message, status: 'open', createdAt: timestamp });
  }
}
function evidence(home, id, kind, versionNumber, source) {
  if (home.evidence.some(item => item.id === id)) fail('New evidence identifier required; history is immutable.', 'coordinator');
  home.evidence.push({ id, kind, version: versionNumber, source });
}
const stageIndex = home => lifecycle.indexOf(home.stage);
function clearAfterDesign(home) {
  for (const key of ['decision', 'capacity', 'release', 'installation', 'quality', 'handover']) home.facts[key] = null;
}

export function mutate(home, action, payload, role, timestamp) {
  const f = home.facts;
  switch (action) {
    case 'resolve_conflict':
      f.conflict = { resolved: true, value: payload.value, source: payload.source };
      break;
    case 'submit_assessment':
      if (stageIndex(home) > 1) fail('Return case to assessed before replacing assessment.', 'coordinator');
      evidence(home, payload.evidenceId, 'assessment', home.version + 1, payload.source);
      f.design = null;
      clearAfterDesign(home);
      f.assessment = { submitted: true, approved: false, evidenceId: payload.evidenceId };
      break;
    case 'approve_assessment':
      if (stageIndex(home) > 1) fail('Return case to assessed before replacing assessment approval.', 'coordinator');
      if (!f.assessment.submitted || payload.evidenceId !== f.assessment.evidenceId) fail('Approval must reference submitted assessment evidence.', 'coordinator');
      f.assessment.approved = true;
      f.assessment.approvalSource = payload.source;
      break;
    case 'approve_design':
      if (stageIndex(home) > 2) fail('Return case to assessed before replacing dependent design.', 'coordinator');
      requireGates(home, 'assessed');
      if (home.evidence.some(item => item.kind === 'design' && item.version >= payload.designVersion)) fail('Design version must increase.', 'coordinator');
      clearAfterDesign(home);
      f.design = { version: payload.designVersion, approved: true };
      evidence(home, `EX-DESIGN-${home.id}-${payload.designVersion}`, 'design', payload.designVersion, payload.source);
      break;
    case 'record_decision':
      if (!f.design || payload.designVersion !== f.design.version || payload.measure !== f.measure) fail('Decision must reference current design and demo measure.', 'resident_officer');
      f.decision = { decision: payload.decision, measure: payload.measure, designVersion: payload.designVersion, source: payload.source };
      if (payload.decision !== 'accepted') {
        for (const key of ['release', 'quality', 'handover']) f[key] = null;
        if (stageIndex(home) > 2) home.stage = 'designed';
        addTask(home, 'resident_reassessment', 'resident_officer', 'Review resident choice before any renewed discretionary work release.', timestamp);
      }
      break;
    case 'approve_package':
      if (stageIndex(home) >= 4) fail('Return dependent case before changing the approved package.', 'coordinator');
      f.package = { version: f.package.version + (f.package.reviewed ? 1 : 0), reviewed: true,
        budgetApproved: payload.budgetApproved, fundingConfirmed: payload.fundingConfirmed, contractApproved: payload.contractApproved };
      f.capacity = null;
      f.release = null;
      break;
    case 'commit_capacity':
      if (stageIndex(home) >= 4) fail('Return dependent case before replacing committed capacity.', 'coordinator');
      if (payload.packageVersion !== f.package.version) fail('Capacity references a stale package.', 'contract_manager');
      requireGates(home, 'scheduled', ['CAPACITY_COMMITMENT', 'WORK_RELEASE']);
      f.capacity = { slots: payload.slots, packageVersion: payload.packageVersion };
      f.release = null;
      break;
    case 'release_work':
      if (payload.packageVersion !== f.package.version) fail('Release references a stale package.', 'programme_manager');
      requireGates(home, 'scheduled', ['WORK_RELEASE']);
      f.release = { approved: true, packageVersion: payload.packageVersion, designVersion: f.design.version };
      break;
    case 'record_installation':
      if (home.stage !== 'scheduled') fail('Installation evidence requires scheduled work.', 'contractor');
      requireGates(home, 'scheduled');
      if (payload.designVersion !== f.design.version) fail('Installation references a stale design.', 'contractor');
      evidence(home, payload.evidenceId, 'installation', payload.designVersion, payload.source);
      f.installation = { evidenceId: payload.evidenceId, designVersion: payload.designVersion };
      f.quality = null;
      f.handover = null;
      break;
    case 'record_quality':
      if (stageIndex(home) < 5) fail('Quality review requires installation.', 'quality_reviewer');
      requireGates(home, 'installed');
      if (payload.designVersion !== f.design.version) fail('Quality evidence references a stale design.', 'quality_reviewer');
      evidence(home, payload.evidenceId, 'quality', payload.designVersion, payload.source);
      f.quality = { outcome: payload.outcome, evidenceId: payload.evidenceId, designVersion: payload.designVersion };
      f.handover = null;
      if (payload.outcome === 'returned') {
        home.stage = 'installed';
        addTask(home, 'reinspection', 'quality_reviewer', 'New independent quality evidence is required for reinspection.', timestamp);
      } else {
        if (home.stage === 'handed_over') home.stage = 'quality_accepted';
        for (const task of home.tasks.filter(item => item.kind === 'reinspection')) task.status = 'resolved';
      }
      break;
    case 'accept_handover':
      if (home.stage !== 'quality_accepted') fail('Handover acceptance requires quality_accepted stage.', 'quality_reviewer');
      requireGates(home, 'quality_accepted');
      evidence(home, payload.evidenceId, 'handover', f.design.version, payload.source);
      f.handover = { accepted: true, evidenceId: payload.evidenceId };
      break;
    case 'match_invoice':
      f.invoice = { matched: payload.matched, source: payload.source };
      if (!payload.matched && home.stage === 'handed_over') {
        f.handover = null;
        home.stage = 'quality_accepted';
        addTask(home, 'invoice_review', 'finance', 'Reconcile the invoice before renewed handover.', timestamp);
      }
      break;
    case 'record_grant': {
      const states = ['opportunity', 'awarded', 'claimed', 'received'];
      const index = states.indexOf(payload.state);
      if (index > 0 && !f.grants[states[index - 1]]) fail('Grant stages require ordered prior evidence; opportunity is not an award or payment.', 'finance');
      if (index > 0 && payload.amount > f.grants[states[index - 1]].amount) fail('Amount cannot exceed the evidenced prior stage.', 'finance');
      if (states.slice(index + 1).some(state => f.grants[state])) fail('Cannot replace prior grant evidence after dependent ledger stages.', 'finance');
      f.grants[payload.state] = { amount: payload.amount, source: payload.source, simulated: true };
      break;
    }
    case 'send_handoff':
      if (home.owner !== role) throw new AppError(403, 'FORBIDDEN', 'Only current owner can send a handoff.', home.owner);
      if (payload.destination === role) fail('Handoff destination must differ from current owner.', home.owner);
      if (home.handoff && ['sent', 'received'].includes(home.handoff.status)) fail('An active handoff already exists.', home.owner);
      home.handoff = { id: `EX-HANDOFF-${randomUUID()}`, from: role, destination: payload.destination, status: 'sent', sentAt: timestamp, chaseOwner: role, reason: payload.reason, source: payload.source };
      break;
    case 'receive_handoff':
    case 'accept_handoff':
    case 'return_handoff': {
      const handoff = home.handoff;
      if (!handoff || handoff.destination !== role) throw new AppError(403, 'FORBIDDEN', 'Only handoff destination can act.', handoff?.destination ?? home.owner);
      if (handoff.id !== payload.handoffId) fail('Handoff ID is not the active handoff.', handoff.destination);
      const states = action === 'accept_handoff' ? ['received'] : action === 'receive_handoff' ? ['sent'] : ['sent', 'received'];
      if (!states.includes(handoff.status)) fail('Handoff state does not permit this action.', handoff.destination);
      handoff.status = action === 'receive_handoff' ? 'received' : action === 'accept_handoff' ? 'accepted' : 'returned';
      handoff[`${handoff.status}At`] = timestamp;
      if (action === 'accept_handoff') home.owner = role;
      break;
    }
    case 'set_update':
      home.residentUpdate = { owner: 'resident_officer', dueAt: payload.dueAt, source: payload.source, reason: payload.reason };
      break;
    case 'record_appointment':
      if (home.appointments.some(item => item.appointmentId === payload.appointmentId)) fail('Appointment has already been recorded.', 'resident_officer', 'APPOINTMENT_CONFLICT');
      home.appointments.push({ ...payload, recordedAt: timestamp });
      if (payload.confirmed && payload.verified && payload.outcome === 'resident_no_access') {
        f.noAccess.count++;
        if (f.noAccess.count > f.noAccess.threshold) addTask(home, 'no_access_investigation', 'resident_officer', 'Investigate repeated verified no-access; this is not refusal or case closure.', timestamp);
      }
      break;
    case 'acknowledge_referral':
      if (!f.hazard.referralId || payload.referralId !== f.hazard.referralId) fail('Referral must match the linked safety referral.', 'safety_officer');
      f.hazard.acknowledged = true;
      f.hazard.acknowledgedAt = timestamp;
      break;
    case 'return_case':
      if ((payload.target === 'assessed' && role !== 'coordinator') || (payload.target === 'installed' && role !== 'quality_reviewer')) throw new AppError(403, 'FORBIDDEN', 'Role cannot return to that target stage.');
      if (stageIndex(home) < lifecycle.indexOf(payload.target)) fail('Return cannot advance a case.', role);
      if (payload.target === 'assessed') {
        f.design = null;
        clearAfterDesign(home);
        addTask(home, 'design_reassessment', 'coordinator', 'Reapprove design and dependent evidence.', timestamp);
      } else {
        f.quality = null;
        f.handover = null;
        addTask(home, 'reinspection', 'quality_reviewer', 'New independent quality evidence is required.', timestamp);
      }
      home.stage = payload.target;
      break;
    case 'advance': {
      const destination = lifecycle[stageIndex(home) + 1];
      if (!destination) fail('No case closure or further lifecycle stage exists in this PoC.', 'programme_manager');
      requireGates(home, destination);
      home.stage = destination;
      break;
    }
    default: throw new AppError(400, 'INVALID_PAYLOAD', 'Unknown command.');
  }
  return home;
}

export function caseView(home, role, events = []) {
  return { ...home, blockers: blockers(home, home.stage === 'handed_over' ? 'handed_over' : undefined),
    allowedActions: allowedActions(home, role), events };
}
export function filterCases(cases, workflow = '', q = '') {
  if (workflow && workflow !== 'all' && !workflows.some(item => item.id === workflow)) throw new AppError(400, 'INVALID_FILTER', 'Unknown workflow filter.');
  const query = q.trim().toLowerCase();
  return cases.filter(home => (!workflow || workflow === 'all' || home.workflow === workflow)
    && [home.id, home.homeId, home.buildingId, home.owner].some(value => value.toLowerCase().includes(query)));
}
export function portfolio(cases, scope, asOf) {
  const groups = [
    ['homes', 'Homes in scope', cases],
    ['blocked', 'Homes with current blockers', cases.filter(home => home.blockers.length)],
    ['safety_holds', 'Linked safety holds', cases.filter(home => home.facts.hazard.hold)],
    ['handed_over', 'Synthetic accepted handovers', cases.filter(home => home.stage === 'handed_over')],
    ['update_due', 'Resident updates due', cases.filter(home => home.residentUpdate.dueAt && Date.parse(home.residentUpdate.dueAt) <= Date.parse(asOf))],
  ];
  return { scope, asOf, synthetic: true, cases: cases.map(home => home.id),
    metrics: groups.map(([id, label, members]) => ({ id, label, numerator: members.length, denominator: cases.length,
      value: members.length, caseIds: members.map(home => home.id) })) };
}
