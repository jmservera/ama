# Details: issue 954 C3 strict mypy on the photo-flag checker (2026-11-09)

Plan `.copilot-tracking/plans/2026-11-09-issue-954-c3-types-plan.md`.

## Step 1: merge

`git fetch origin main`; record the resolved SHA; `git merge --no-ff origin/main` with a Conventional message. Resolve any tracking or log conflict by keeping both intents (appended entries from both sides); a source conflict is reported, not shortcut. Afterwards confirm `git diff origin/main --name-only` is the checker plus tracking only.

## Step 2: reproduce

From `src/api`, in the existing owned venv `/home/azureuser/.venvs/ama462` (pip restore only for missing chosen-profile dependencies, never global): `mypy --version` (2.4.0), `mypy`. Expect exactly the five hosted errors on the checker; keep the raw output. If the venv cannot resolve imports, restore only what is missing with pip inside that venv and record it.

## Step 3: checker (`src/api/checks/photo_flag_stale_browser_check.py` only)

* Imports: `Callable` and `Mapping` from `collections.abc`; `Dialog` from `playwright.sync_api`.
* Module aliases after the constants: `principal_header: Callable[..., str] = principal`; `make_provider: Callable[[Store, Mapping[str, str]], auth.TrustedProxyProvider] = auth.TrustedProxyProvider`; `make_app: Callable[..., App] = App` (adjust parameter types to what mypy accepts, never `Any`).
* `detector_self_test.case()`: `count = int(page.evaluate("window.__zfDisruptive.length"))`.
* `observe()`: `principal_header(oid=OID_SAM)`; replace the dialog lambda with `def on_dialog(dialog: Dialog) -> None` that appends `dialog.message` then calls `dialog.dismiss()`, registered with `page.on("dialog", on_dialog)`.
* `main()`: `make_app(store, provider=make_provider(store, ENV))`.

## Step 4: validation and record

mypy (whole project command), Ruff check and `ruff format --check` over the project, unit selections, holder check, one nonqueued admission. Evidence in a session-owned directory (`evidence-954-c3`) with commands, stdout, stderr, exits, tool versions, import and checker SHA before and after, admission time and raw manifest. Then changes, review, state and handoff.
