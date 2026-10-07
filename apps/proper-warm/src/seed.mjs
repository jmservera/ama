import { workflows } from './domain.mjs';

export const schemaVersion = 'poc-1';
export const fixtureVersion = 'constructed-nine-v1';
const source = id => `EX-SOURCE-${id}`;
function createCase(number, workflow, threshold) {
  const id = `EX-HOME-${number}`;
  return {
    id, homeId: id, buildingId: [208, 317].includes(number) ? 'EX-BUILDING-PAIR' : `EX-BUILDING-${number}`,
    schemeId: 'EX-SCHEME-LOCAL', workflow, stage: 'candidate', version: 1, owner: 'programme_manager',
    evidence: [{ id: `EX-STOCK-${number}`, kind: 'stock', version: 1, source: source(number) }],
    facts: {
      synthetic: true, measure: 'insulation', packageId: [208, 317].includes(number) ? 'EX-PACKAGE-PAIR' : `EX-PACKAGE-${number}`,
      conflict: { resolved: true, value: 'constructed stock record', compared: [] },
      assessment: { submitted: false, approved: false }, design: null, decision: null,
      package: { version: 1, reviewed: false, budgetApproved: false, fundingConfirmed: false, contractApproved: false },
      capacity: null, release: null, installation: null, quality: null, handover: null,
      invoice: { matched: false }, grants: { opportunity: null, awarded: null, claimed: null, received: null },
      hazard: { hold: false, referralId: null, acknowledged: false, externalClock: 'not simulated' },
      noAccess: { count: 0, threshold, ruleVersion: 'exercise-no-access-v1' },
    },
    handoff: null, residentUpdate: { owner: 'resident_officer', dueAt: null, source: null },
    tasks: [], appointments: [],
  };
}
function prepare(home, stage) {
  const f = home.facts;
  const suffix = home.id.replace('EX-HOME-', '');
  const add = (kind, id) => home.evidence.push({ id, kind, version: 1, source: source(suffix) });
  f.assessment = { submitted: true, approved: true, evidenceId: `EX-ASSESSMENT-${suffix}`, approvalSource: source(suffix) };
  add('assessment', f.assessment.evidenceId);
  f.design = { version: 1, approved: true };
  add('design', `EX-DESIGN-${home.id}-1`);
  if (['resident_ready', 'scheduled', 'installed', 'quality_accepted'].includes(stage)) {
    f.decision = { decision: 'accepted', measure: 'insulation', designVersion: 1, source: source(suffix) };
  }
  if (['scheduled', 'installed', 'quality_accepted'].includes(stage)) {
    f.package = { version: 1, reviewed: true, budgetApproved: true, fundingConfirmed: true, contractApproved: true };
    f.capacity = { slots: 1, packageVersion: 1 };
    f.release = { approved: true, packageVersion: 1, designVersion: 1 };
  }
  if (['installed', 'quality_accepted'].includes(stage)) {
    f.installation = { evidenceId: `EX-INSTALLATION-${suffix}`, designVersion: 1 };
    add('installation', f.installation.evidenceId);
  }
  if (stage === 'quality_accepted') {
    f.quality = { outcome: 'accepted', evidenceId: `EX-QUALITY-${suffix}`, designVersion: 1 };
    add('quality', f.quality.evidenceId);
  }
  home.stage = stage;
  home.residentUpdate = { owner: 'resident_officer', dueAt: '2026-10-08T12:00:00Z', source: source(suffix) };
}
export function seedCases(threshold = 5) {
  const mapping = { prioritisation: 646, technical_readiness: 104, resident_service: 208,
    capacity: 317, hazards: 531, quality: 422, finance_grants: 752, handoffs: 863, portfolio: 900 };
  const cases = workflows.map(workflow => createCase(mapping[workflow.id], workflow.id, threshold));
  const by = number => cases.find(home => home.id === `EX-HOME-${number}`);
  by(104).owner = 'coordinator';
  prepare(by(208), 'designed');
  by(208).owner = 'resident_officer';
  prepare(by(317), 'resident_ready');
  by(317).owner = 'contract_manager';
  by(317).facts.package = { version: 1, reviewed: true, budgetApproved: true, fundingConfirmed: true, contractApproved: true };
  prepare(by(422), 'installed');
  by(422).owner = 'quality_reviewer';
  by(422).facts.quality = { outcome: 'returned', evidenceId: 'EX-QUALITY-422-RETURNED', designVersion: 1 };
  by(422).evidence.push({ id: 'EX-QUALITY-422-RETURNED', kind: 'quality', version: 1, source: source(422) });
  by(422).tasks.push({ id: 'EX-TASK-422-REINSPECT', kind: 'reinspection', owner: 'quality_reviewer', status: 'open', message: 'Constructed defect requires new reinspection evidence.', createdAt: '2026-10-07T00:00:00Z' });
  by(531).owner = 'safety_officer';
  by(531).facts.hazard = { hold: true, referralId: 'EX-REFERRAL-531', acknowledged: false, externalClock: 'not simulated' };
  by(531).evidence.push({ id: 'EX-HAZARD-531', kind: 'hazard', version: 1, source: source(531) });
  by(646).owner = 'data_owner';
  by(646).facts.conflict = { resolved: false, value: null, compared: [
    { value: 'EX-EPC-D', source: 'EX-SOURCE-646-STOCK', version: 1 },
    { value: 'EX-EPC-E', source: 'EX-SOURCE-646-SURVEY', version: 1 },
  ] };
  prepare(by(752), 'quality_accepted');
  by(752).owner = 'finance';
  by(752).facts.grants.opportunity = { amount: 7500, source: source(752), simulated: true };
  by(863).owner = 'coordinator';
  by(863).handoff = { id: 'EX-HANDOFF-863', from: 'coordinator', destination: 'resident_officer',
    status: 'sent', chaseOwner: 'coordinator', sentAt: '2026-10-07T00:00:00Z', source: source(863), reason: 'Constructed ownership transfer' };
  return cases;
}
