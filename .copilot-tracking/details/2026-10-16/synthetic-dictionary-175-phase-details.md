# Phase Details: issue-175 / synthetic-dictionary-175

## P01-T01: Validator

Reuse generator label conventions: sensor source_type, chat is_synthetic,
scale households is_synthetic and homes/events manifest inheritance bound by
file_sha256. Read only public files or caller-supplied fresh temporary snapshots.
Explicit expected file inventories prevent silently skipping added payloads.
Manifest and CSV/JSON parse failures fail loudly; findings contain paths/reasons,
not sensitive matched values. Real-looking postcodes are rejected except the
scale generator's exact fictional TE[0-8] 1ST field values.

Public contract: operating CSV rows require is_synthetic=true except the named
evidence-gap-register.csv metadata exemption. Pack/scenario manifests require
root is_synthetic=true. Document controls require labels on cases, forms on
families and already-labelled nested documents. Constructed AI/chat scenario
collections inherit their existing root note, regulatory cases/results inherit
their root label, and eval registry entries require contains_real_data=false.
All exempt/inherited content is still pattern-scanned; no fixture bytes change.

## P01-T02: Tests

Core tests cover all registered public files and source-readiness failures,
mutated positive fixtures, all label alternatives, separation using git check-ignore
without private-file reads, sensor/register-backed/scale snapshots and CLI exit.
One agents module generates the nine chat payloads and mutates them through the
same checker. Do not weaken source metadata assertions into a blanket pass.
For each pattern and missing/false row label, refresh hashes and assert the
specific checker diagnostic independently of integrity/source failure. CLI
mutations disable source checks; clean CLI exit zero is the control. Stale
hashes and missing manifest labels have separate tests. Allocate fresh scratch
under the owning project using explicit output paths and clean up afterwards.
Exception: the existing register-backed generator refuses all repository paths;
its regression uses an explicitly allocated outside-repository temporary
directory and cleans it up. Do not weaken or mock that guard. All-excluded
monitoring fixtures retain their valid explicitly empty sensor output.

## P01-T03: Documentation

Register generated status separately from visibility. Include scale/fabric,
document controls, current chat/regulatory evals and runtime chat/memory.
Record runtime user content as potentially personal, not guaranteed fictional.
Preserve source null dates and provisional licences with explicit readiness.
Add exact acceptance table and bounded detection statement to dictionary.
Update core/agents and knowledge-base READMEs and append log entry.

## P02-T01: Validation

Use src/core/.venv installed editable core/agents/api (missing dependencies were
confirmed first). Set absolute PYTHONPATH for each project's test helpers.
Run affected suites and project ruff/mypy; local checker CLI succeeds for public
data and rejects source audit; launch API only with fresh synthetic test data.
No Azure or model calls.
Set ZF_DATA and ZF_STORE explicitly for local startup, omit model configuration
and use fresh DATA from the committed test helper, not any private seed.

## P02-T02: Review and delivery

One RPI Review after implementation; route new material findings as follow-up.
Audit AC1/3/4 on measured evidence, AC2 unmet. Configure authenticated privacy-safe
repo-local author/committer and required trailer; push current branch and create
PR targeting main with Refs #175, explicit unmet criterion and validation.
