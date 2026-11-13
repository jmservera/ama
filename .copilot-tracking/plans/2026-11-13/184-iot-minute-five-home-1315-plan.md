# Plan: #184 port
* [ ] P1 Apply candidate patch (git apply) onto main.
* [ ] P2 RED test: sensor_handover_verify.main with empty reference and with run() returning None must exit non-zero and never print passed true.
* [ ] P3 Guard in main(): result must be a Mapping and result.get("passed") is True for exit 0.
* [ ] P4 ruff format; ruff check; mypy; targeted unittests in --system-site-packages venv.
* [ ] P5 Independent review, commit (Refs #184, #1288, #109).
* [ ] P2b RED uses passed=1 (truthy non-bool) and None result; literal True only exits 0.
* [ ] P6 attempt_permitted gets optional demo set; exact control cohort recheck per attempt; RED test sixth home mid-slot.
* [ ] P7 run loop cohort refusal propagates non-zero exit from main; test.
* [ ] P8 --max-homes conflicting with demo five refused (SIM_CONFIG_INVALID); test.
* [ ] P9 reword "hold"/"envelope" in added README text.
