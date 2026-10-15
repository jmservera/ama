# Changes: #105

* Added `mvp/zavaforward_mvp/ai_registry.py`.
* Edited `ai_tasks.py` (envelope on records/results, registration gate), `assistants.py` (envelope binding), `server.py` (registry on `/api/ai/report`).
* Added `RegistryEnvelopeTests`. Validation: 474 tests OK (85 skipped).
* Open: priority path still calls `ai.run` directly without envelope; all authority items stay `unknown`.
