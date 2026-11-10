# Plan critique: issue 1288 E7

Independent critique by a rubber-duck agent (read-only), executed once, on the E7 research, plan and details at start `56d0bdc33`. Verdict: rework (4 blocking, 1 non-blocking). Ordinary flow: compatible findings applied directly; no finding conflicts with a confirmed user decision; no user decision needed. The critique is not repeated for this task.

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | A mutable capability flag set on real instances can be bypassed by a subclass or a delegating `store.ai` | Blocking | Accepted. The refusal is enforced at two boundaries: `Lane.request` and the real `Ai._request` sealed-simulation branch, before verifier, data hold, meter, token or socket. Production code never sets the capability; only scripted test plumbing sets it, and a source regression asserts that. Tests cover a subclass and a delegating replacement before any I/O. |
| 2 | A response proxy omits `code` and `msg` that `HTTPErrorProcessor` reads and may bypass cleanup via `__enter__` | Blocking | Accepted, design changed: no proxy. The connection sets `response_class` to an `HTTPResponse` subclass that receives the live socket at construction and owns the window, so the full urllib interface and context manager are unchanged. Tests cover success and non-2xx through `Ai.evidence`. |
| 3 | Pre-handoff failures (send, header read, urllib processing) leak the deadline operation once `close()` no longer cancels | Blocking | Accepted. `close()` finishes the window unless a response has adopted it; `ai.py` closes an `HTTPError` on the failure path. Tests assert no live timer and no open socket after send failure, malformed headers and an HTTP error. |
| 4 | Shutdown can yield a partial read that parses as valid JSON | Blocking | Accepted. The window keeps a sticky expired state under a lock; the response `read` raises `TimeoutError` when expired even if shutdown produced EOF. Test: a valid JSON prefix followed by a trickle past the deadline fails. |
| 5 | `Lane.state` reports ready and the UI still offers the request button | Non-blocking | Accepted as a residual, no web edit. The existing UI path renders the refusal (`Not sent (reason). manual route`). The residual is recorded in the handoff; a UI change would need the web guidelines and is outside this correction. |

Residual accepted by the critique: the ordinary `Assistants.execute` path still uses this transport and retains its post-fence suspension race; it is not claimed as a closed guarantee.
