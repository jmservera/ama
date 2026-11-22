# Details: issue 2245 and 2243

* Files: `src/agents/.../chat.py`, `src/core/.../chat_panel.py`, `src/api/.../server.py`, `src/api/.../resident_demo/assistant.py`, `aoai.py`, two test files.
* Tier: FULL classification (src code changes) with the owner D6 gate economy: no `rpi-checks.py --all` by the worker; the coordinator runs gates. Targeted tests, mypy and ruff run locally.
* Live changes allowed: image roll of `ca-resident-demo` only (az, never Bicep). Registry is reopened for the push window and restored by the trap in `/tmp/acr-push.sh`.
