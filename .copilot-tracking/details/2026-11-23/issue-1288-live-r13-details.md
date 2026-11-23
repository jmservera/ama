# Issue 1288 r13 plan details

Phase 1: in src/api/src/zava_forward/api/server.py add a module-level helper logging `sensor-unavailable GET <path> exc=<ClassName> at=<file:line:func>` at WARNING via `logging.getLogger(__name__)`. Call it inside `except Exception as exc:` for `/sensors` and `/sensor-drafts`.

Phase 2: test patches `self.service.sensors` to raise RuntimeError("secret-host") and asserts 503, unchanged body, `assertLogs("zava_forward.api.server")` contains `RuntimeError` and not `secret-host`.
