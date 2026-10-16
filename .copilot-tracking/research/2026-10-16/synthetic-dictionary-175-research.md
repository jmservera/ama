<!-- markdownlint-disable-file -->
# Research: synthetic dictionary and provenance (Refs #175)

## Research Brief

Deliver the four issue acceptance criteria for maintainers: dataset coverage,
external-source provenance, automated personal-data/label rejection, and tested
public/private separation. Output mode: convergence preparing implementation.
Focused posture, selected for the bounded internal issue and offline constraint.
No Azure, private dataset reads, legacy-tree edits, identity setup edits or
operational approval. Read original case study, addendum, knowledge-base index
and owner memory at intake.

## Research Parameters and Direction Controls

Task identity: issue-175 / synthetic-dictionary-175. Reuse the clean existing
`docs/synthetic-dictionary-175` branch, tracking origin/main with no open PR.
User explicitly requests research, plan, implementation, review and PR delivery;
phase progression is authorized by that end-to-end request, not a claim of
interactive automatic-session consent.

## Extension Registry and Participation

Repository instructions, ADR 0006 and explicit user constraints selected.
RPI skills coordinate phase artifacts. No web work or legal interpretation.
Inline research: one continuous dataset/provenance trace does not benefit from
delegation. Independent final-plan critique will use a bounded reviewer.
No external retrieval permitted; recorded local evidence must not be presented
as freshly verified official-source content.

## Questions and Candidate Areas

1. Which generated outputs and runtime records lack current dictionary coverage?
2. Can locally recorded source provenance resolve the reopened metadata gaps?
3. Do existing rejection tests exercise real validation and all generated files?
4. Can separation be verified without accessing private working data?

Start with the dictionary/register, core synthetic generators/tests, agent chat
fixtures, source README metadata, project packaging and source CI.

## Research Cycle Log

Cycle 1 opening: Wider inventories generated surfaces and source metadata;
Deeper traces labels, output guards and scanner behavior; Contrarian challenges
absolute PII-free claims and distinguishing generated fixtures from live chat.

## Evidence Log

* C1: `docs/reference/research/retrofit-synthetic-data/data-dictionary.md:318`:
  sensor section incorrectly claims no generator; reopened issue explicitly
  identifies the contradiction.
* C2: `src/core/tests/test_synthetic_provenance.py:49`: test enforces obsolete
  not-generated sensor status and permits absent external retrieval dates.
* C3: `src/core/tests/test_synthetic_provenance.py:93`: tests read private stock
  working data, making the guard unsuitable for a clean offline checkout.
* C4: `docs/reference/research/retrofit-synthetic-data/provenance-register.json:20`:
  three external source entries contain provisional licences and null dates.

## Findings, Decisions and Readiness

* C5: `src/core/src/zava_forward/core/synthetic/sensor_backfill.py:36`:
  sensor register/readings use source_type=SYNTHETIC, not is_synthetic.
  Register mode also emits labelled stock-fabric.csv, and manifests bind hashes.
* C6: `src/core/src/zava_forward/core/synthetic/scale_fixture.py:112`:
  homes/events inherit the manifest label; households carry row labels.
* C7: `src/agents/tests/chat_fixture.py:231`: nine generated JSONL datasets
  and a synthetic manifest; live runtime chat is distinct from these templates.
* C8: `support/synthetic-data/retrofit-flow/zava-forward-year-one/stock-geography/README-private.txt:15`:
  source-only metadata confirms OSM date/licence, but no retrieval dates or
  verified licence terms for the other three sources. No private dataset read.
* C9: `src/agents/evals/registry.json:4`: existing eval registry inventories
  all eight public JSON files, including chat/regulatory and document fixtures.

Cycle 1 Wider: identified scale/fabric, sensor/register-backed outputs, nine
chat tables and public evals beyond the old register. Reflection: dictionary
needs dataset families, not an assertion that full-stock data was materialized.
Deeper: traced row labels, manifest labels/hashes, runtime/private paths and
existing tests. Reflection: preserve generator bytes and test explicit inherited
labels rather than alter established deterministic fixtures.
Contrarian: metadata-only file exemptions are legitimate, but arbitrary labels
or regexes do not prove a person is fictional. Live user chat and staff bindings
cannot be certified synthetic. Unknown retrieval dates cannot be reconstructed
from a Git commit date. Reflection: AC2 must remain unmet under offline scope.

Accepted: reusable typed validator and CLI; fresh tiny generated fixtures,
public-only scans and no private working-data dependency; current dictionary
and source register; explicit nonzero source-readiness audit.
Rejected: inventing dates/licences, scanning private stock, universal PII-free
claims, unnecessary generator/schema changes or new datasets.
Deferred: official metadata verification by exercise Legal/Compliance/DPO
owner Juan Manuel Servera; actual runtime/DPO approval remains separate.

Planning Readiness: Ready for bounded implementation with AC2 blocked.
Research disposition: executed. One complete cycle sufficient: all four
questions answered; unavailable external provenance cannot be recovered within
the caller's offline boundary. No second search cycle is justified.
