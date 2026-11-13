# Review: #107 identity-field sanitisation (1440)

Execution: complete (code-review agent, one pass). Outcome: Conformant after one fix.

* Finding (Medium): `sk-` substring rejection mangled legitimate names such as `task-fast`, quarantining releases. Fixed: reject only at a token start or when followed by 16+ key characters; tests added. Rechecked: ruff, format, mypy, identity, consumption and API assistants suites pass.
* Routed: no open findings. Not run: MSSQL suites, the monolithic core discover (over 900 s).
