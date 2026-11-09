# Details: issue 144 queue-slice recovery (2026-11-09)

Tier: owner-selected demo-targeted (replaces full local gate for this demo push).

* Environment: venv outside the repo with `pip install -e src/core -e src/agents ruff mypy`.
* From `src/agents`: `python -m unittest discover -s tests -p test_queue_azure.py` (and test_worker, test_dispatch, test_dependency_rule); full agents suite with `PYTHONPATH=../core/tests`.
* `ruff check` and `ruff format --check` on queue_azure.py and test_queue_azure.py; `mypy` on queue_azure.py and worker.py.
