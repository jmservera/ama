# Proper Warm local demonstrator

This is a local viability demonstrator for the Proper Warm retrofit programme. It uses fictional evidence, a local Python server and SQLite. It is not an operational case-management system, and its outputs are not evidence that a legal, safety, funding or company requirement has been met.

## Safety boundaries

* Use synthetic data only. Do not enter resident, staff, address, contact, health, support or other personal information.
* Local startup binds to `127.0.0.1` by default. The container image also defaults to loopback; only the Bicep internal-ingress configuration selects the container listener. Never expose that listener publicly.
* It has no M365, Dataverse, Dynamics 365, external AI or other live-system integration.
* The private `support/synthetic-data/retrofit-flow/proper-warm-year-one/stock-geography/` overlay is excluded.
* The missed-appointment threshold is a provisional synthetic test rule, not an approved operational control. Only a confirmed appointment with verified resident no-access counts; escalation is strictly greater than the configured threshold.
* Stage gates, safety holds, reviews and threshold changes demonstrate workflow behavior only. Human review remains necessary, and company ratification is outstanding.
* Local SQLite data is stored in `prototype/.data/` by default. It is disposable demo state, not a backup or production data store.
* In the Azure Container Apps example, SQLite is on the container's ephemeral filesystem. A restart or revision replacement can lose its state; the example has one replica and no Azure Files or production persistence.

## Requirements

* Python 3.12 or newer.
* The dependency in `requirements.txt` (`openpyxl`).
* The repository's published fictional evidence pack at `docs/reference/research/retrofit-synthetic-data/`.

## Run locally

From the repository root, create an environment and install the one dependency:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r prototype/requirements.txt
```

Start the server in PowerShell:

```powershell
$env:PYTHONPATH = "prototype"
python -m properwarm.server
```

On macOS or Linux, use `PYTHONPATH=prototype python -m properwarm.server`. Open <http://127.0.0.1:8765> in a browser. The server accepts `--port`, `--data-dir` and `--source-dir` options for local testing. Stop it with `Ctrl+C`.

The first start seeds local SQLite state from the synthetic `candidate-lifecycle.csv` and `safety-holds.csv` files. The app reads selected synthetic fields only. It fails if either required source or its required columns are missing. Demo database and journal files remain under `prototype/.data/` unless `--data-dir` is set.

## Container and compile-only Azure example

The container package includes a separate sanitized seed directory, not the full source CSVs. Generate it from the approved synthetic pack and build the image from the repository root:

```powershell
python prototype/scripts/build_container_seed.py
docker build -f prototype/Dockerfile -t properwarm-demo:local .
```

The Docker image defaults to loopback. The Azure Container Apps template sets `APP_INTERNAL_INGRESS=true` together with internal-only environment and app ingress; the server maps that explicit mode to the container interface. Do not set this mode outside an internal-ingress environment.

The compile-only template is [deploy/main.bicep](deploy/main.bicep). It requires an existing Azure Container Apps infrastructure subnet and a container image available to Azure; it creates a Log Analytics workspace, an internal managed environment, and a single-replica app. It is not deployment-tested, does not provision a virtual network or image registry, and is not production guidance. Compile without deploying:

```powershell
az bicep build --file prototype/deploy/main.bicep --stdout
```

## Test and regenerate the sample workbook

Run the regression suite from the repository root:

```powershell
python -m unittest discover -s prototype/tests -v
python -m compileall -q prototype/properwarm
```

Rebuild the fictional three-row workbook:

```powershell
python prototype/scripts/build_demo_workbook.py
```

In the workbench, select `prototype/seed/demo-import.xlsx`, preview every row disposition, then commit the preview. Import accepts only the declared nine-column synthetic schema, rejects invalid rows, preserves source-row lineage and rechecks conflicts at commit. It does not modify the workbook or overwrite an existing case.

## Workbench flow

* Search and filter fictional cases, then inspect current stage, gates, holds and history.
* Change synthetic gate controls and advance only when required gates pass and no active hold blocks progression.
* Record confirmed appointment outcomes, review events, closure and reopening. Closure starts a new active episode while retaining prior history.
* Configure the synthetic missed-appointment threshold and inspect the audit history. The default is 5; five eligible events do not escalate and the sixth does.
* Download the JSON evidence export to inspect cases, source lineage, events, audit entries and current configuration.

All actions remain within the running demonstrator and do not contact residents or alter source evidence. In the container example, access is restricted to the configured internal network.

## Architecture

The editable local architecture diagram is [architecture/proper-warm-local-prototype.excalidraw](architecture/proper-warm-local-prototype.excalidraw). It describes the implemented local flow; the compile-only Azure example does not represent an approved production architecture.

## Limitations

This prototype demonstrates deterministic workflow and data-handling behavior against one fictional evidence pack. It does not prove company process fit, rule validity, resident acceptance, accessibility conformance, security for operational data, delivery outcomes or regulatory compliance. Threshold ratification, operational configuration governance, hosting, identity, integrations and production persistence require separate evidence and approval.
