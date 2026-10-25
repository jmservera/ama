# Reconciled exact resident requirement map

**Unsigned review proposal only; current independent PRD FAIL / Validate
BLOCKED / Finalize NOT_EVALUATED.** Completed PRD v0.19.1 SHA-256:
`7fb40549ba4975c2feb8d8a2a3de882e06677875c02e4a43c4b3a94ddf218343`.
All 30 resident criterion texts, PRD parents and Not-run statuses are exactly
unchanged from the pinned canonical PRD. Source line numbers and whole-file
hash are updated in a new map; the original map is not overwritten.

The [JSON companion](requirement-map-reconciled.json) preserves exact criterion
text, original and completed source references, original BRD parents and
completed qualified FR-trace supplements. C1–C9 refer to the
[one recommended candidate](../../resident-service-unregistered-proposal.md).
Structural coverage is not singularity, feasibility, approval or test evidence.

| PRD AC | PRD parent | BRD design parents / criteria | Contracts | Exact delta / execution |
| --- | --- | --- | --- | --- |
| AC-111 | FR-062 | FR-053, AC-104, AC-105 | C2 | Unchanged / Not run |
| AC-112 | FR-062 | FR-053, AC-104, AC-105 | C2 | Unchanged / Not run |
| AC-113 | FR-062 | FR-053, AC-104, AC-105 | C2 | Unchanged / Not run |
| AC-114 | FR-063 | FR-054, AC-106, AC-107 | C2, C3, C4 | Unchanged / Not run |
| AC-115 | FR-063 | FR-054, AC-106, AC-107 | C2, C3, C4 | Unchanged / Not run |
| AC-116 | FR-064 | FR-055, AC-108, AC-109 | C3, C5 | Unchanged / Not run |
| AC-117 | FR-064 | FR-055, AC-108, AC-109 | C3, C5 | Unchanged / Not run |
| AC-118 | FR-065 | FR-056, AC-110, AC-111 | C3, C8 | Unchanged / Not run |
| AC-119 | FR-065 | FR-056, AC-110, AC-111 | C3, C8 | Unchanged / Not run |
| AC-120 | FR-066 | FR-057, AC-112 | C3, C8 | Unchanged / Not run |
| AC-121 | FR-067 | FR-058, AC-113, AC-114 | C2, C6, C7, C8 | Unchanged / Not run |
| AC-122 | FR-067 | FR-058, AC-113, AC-114 | C2, C6, C7, C8 | Unchanged / Not run |
| AC-123 | FR-067 | FR-058, AC-113, AC-114 | C2, C6, C7, C8 | Unchanged / Not run |
| AC-124 | FR-068 | FR-059, AC-115, AC-125 | C5, C8 | Unchanged / Not run |
| AC-125 | FR-068 | FR-059, AC-115, AC-125 | C5, C8 | Unchanged / Not run |
| AC-126 | FR-069 | FR-060, AC-116, AC-117 | C1, C2, C5 | Unchanged / Not run |
| AC-127 | FR-069 | FR-060, AC-116, AC-117 | C1, C2, C5 | Unchanged / Not run |
| AC-128 | FR-069 | FR-060, AC-116, AC-117 | C1, C2, C5 | Unchanged / Not run |
| AC-129 | FR-070 | FR-061, AC-118, AC-119, AC-126, AC-084 | C2, C6, C7, C8 | Unchanged / Not run |
| AC-130 | FR-070 | FR-061, AC-118, AC-119, AC-126, AC-084 | C2, C6, C7, C8 | Unchanged / Not run |
| AC-131 | FR-070 | FR-061, AC-118, AC-119, AC-126, AC-084 | C2, C6, C7, C8 | Unchanged / Not run |
| AC-132 | FR-071 | FR-062, AC-123, AC-124 | C9 | Unchanged / Not run |
| AC-133 | FR-071 | FR-062, AC-123, AC-124 | C9 | Unchanged / Not run |
| AC-134 | NFR-018 | NFR-013, AC-120 | C1, C4, C5, C6, C8 | Unchanged / Not run |
| AC-135 | NFR-019 | NFR-014, AC-121, AC-122 | C1, C2, C4, C6, C9 | Unchanged / Not run |
| AC-136 | NFR-019 | NFR-014, AC-121, AC-122 | C1, C2, C4, C6, C9 | Unchanged / Not run |
| AC-137 | NFR-020 | NFR-014, AC-111, AC-112, AC-119, AC-122 | C1, C3, C4, C7, C8 | Unchanged / Not run |
| AC-138 | NFR-020 | NFR-014, AC-111, AC-112, AC-119, AC-122 | C1, C3, C4, C7, C8 | Unchanged / Not run |
| AC-139 | NFR-021 | OD-55 | C9 | Unchanged / Not run |
| AC-140 | GOAL-005 | FR-053–FR-062, AC-104–AC-126 | C1, C2, C3, C4, C5, C6, C7, C8, C9 | Unchanged / Not run |

## Qualified trace supplements and retained debt

Completed PRD FR-064 explicitly traces to BRD FR-055 **and FR-046** (scheduling);
FR-067 to BRD FR-058 **and FR-003/RULE-003** (independent hazard referral);
FR-068 to BRD FR-059 **and RULE-027** (optionality); FR-069 to BRD FR-060
**and FR-045** (representative authority); FR-070 to BRD FR-061
**and RULE-028/FR-044** (bounded policy and actual disposition). These are
compatible elaborations already covered by original ADR contracts and
cross-cutting controls, not new superseding business decisions. Exact qualified
FR source arrays are copied from the completed trace JSON into the new map.

The original ADR’s broader BRD AC lists remain proposed design obligations;
a shared parent reference does not mean each listed AC is exercised by each
PRD criterion. Do not join PRD/BRD by number alone, allocate new IDs or call
71/71 whole-PRD FR-link coverage full reciprocal fidelity. PRD FR-059’s
GOAL-004 definition versus GOAL-002 retained matrix overlink is still open.
Inherited PRD FR-044/060 and AC-104–106 bundles remain the singularity blocker;
this 30-row resident map does not atomize or approve those unrelated obligations.

NFR-018–021 and GOAL-005 continue through AC-134–140. NFR-021’s proposed
numerical sizing is linked to BRD OD-55, not a signed BRD latency target.
Generic/resident NFR response/file-size precedence remains OPEN
(pr442-qual-041); no pass is asserted for overlapping operations without
requirements-owner applicability clarification. All execution remains Not run.
OD-52–55 ↔ OQ-028–031, live resident authority gates and independent staff/
regulatory boundaries remain unchanged. No task, policy or ADR registration
is supplied by this reconciliation.
