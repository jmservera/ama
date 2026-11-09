# Changes: pinned Ruff 0.17.1 qualification (Refs #136, #1258)

Head under test `deb1f1e405826cc6092352720b885a78919e5c2f`, source unchanged. Tool `/tmp/v136ruff/v/bin/ruff`, `ruff 0.17.1` (own venv, removed after). cwd repo root, `--isolated`.

| Command | Exit |
| --- | --- |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_deploy.py infra/scripts/deploy.py` | 0 (All checks passed) |
| `ruff format --isolated --line-length 100 --check` same three files | 0 (3 files already formatted) |

sha256: test_bicep_policy.py `672b18699c69626f1291203446816d1a4514057c1efb3474bc7f9e4d0cd2e253`; test_deploy.py `e82dca61e0b017398bfceb08c08648974b468a7490781336c1e434782e1f0d6e`; deploy.py `4d99d4991d66e10757d050dfce659f6be285993930fdfe0f9421cc49e9df69f4`. The test_bicep_policy.py hash equals the blob qualified in the C6 changes record. Earlier 0.17.3 results remain as recorded. Nothing else rerun.
