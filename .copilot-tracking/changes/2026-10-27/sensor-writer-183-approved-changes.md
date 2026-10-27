---
title: Canonical stock sensor identity implementation
ms.date: 2026-10-27
---

## Scope and Owner Decision

Refs #183, parent #177, child PR #485. Whole P02 identity phase of
177-approved-integration-2026-10-27. Owner decision
owner-approvals-2026-10-27-b adopts existing stock home IDs as canonical.
Original blocked evidence remains unchanged; no private stock file was opened.

## Implementation

Preserve canonical stock keys exactly, including case and Unicode, up to 128
UTF-16 units. New stock-sensor-v2 keys are S plus ten Base32 SHA-256 characters
(50 digest bits); derive from the complete UTF-8 home key, never its tail.
Selection detects duplicate derived sensor keys and fails explicitly instead
of reassigning home IDs. Eleven-character keys leave nine characters for the
existing UNMAPPED- fault prefix inside the consumer's 20-character limit.
Reading IDs remain <=40 using the unchanged timestamp suffix.

The consumer now validates home keys with the canonical stock contract, while
sensor/reading/scenario identities retain their previous strict rules.
Availability, mapping, consent, calibration, units, clock, range, ordering and
replay remain independent. Home IDs over 64 UTF-16 units return HOME_UNAVAILABLE
on both stores: the shared SQL cases.id schema remains NVARCHAR(64), not silently
expanded. Export supports the full 128-unit stock domain; store availability is
not manufactured by observations or the writer.

Fresh SQL reading home keys use binary-collated NVARCHAR(128). Existing legacy
reading schemas remain supported for their representable keys; insufficient
width or non-Unicode storage for a canonical key fails SENSOR_SCHEMA_UNSUPPORTED
before insertion. No truncation, alias, identity migration or live data mutation.
Generator revision fingerprint includes the identity helper.

## Validation

Executed from src/core with external focused venv, pip-editable installation of
this child only, never uv or PYTHONPATH=mvp:

```bash
python -m unittest discover -s tests -p test_sensor_consumer.py -q
python -m unittest discover -s tests -p test_sensor_stock.py -q
ruff check src/zava_forward/core/synthetic/sensor_identity.py \
  src/zava_forward/core/synthetic/sensor_stock.py \
  src/zava_forward/core/sensor_consumer.py \
  tests/test_sensor_consumer.py tests/test_sensor_stock.py
mypy src/zava_forward/core/synthetic/sensor_identity.py \
  src/zava_forward/core/synthetic/sensor_stock.py \
  src/zava_forward/core/sensor_consumer.py \
  tests/test_sensor_consumer.py tests/test_sensor_stock.py
```

35 actual SQLite consumer tests and 16 stock tests passed; targeted Ruff,
format and mypy passed. Seven new methods, no removals. Fixtures prove canonical
23/64-unit and non-ASCII exact admission/replay, unchanged canonical export at
64/65/128 units, explicit missing/oversized home refusal, consent/calibration
rejection, malformed keys, collision refusal, and actual UNMAPPED (not IDENTITY)
for a maximum-length transformed stock sensor key.

SQL Server execution is pending the one aggregate parent gate, not inferred
from SQLite. Synthetic fixture case keys are explicitly prepared by tests;
the production writer does not create cases or grant controls. Full source and
writer integration, full-stock output and parent Review/gate remain separate.
