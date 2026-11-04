# Signed-in walkthrough 462 and authenticated checks 810 research (2026-11-04)

Research disposition: satisfied-and-skipped (existing evidence: deploy-main-810-462 research and review, easy-auth note, resident demo source). Planning Readiness: Ready.

* Targets: `ca-resident-demo` (own app-level sign-in, no Easy Auth) and `ca-cutover-test-demo-api` (Easy Auth on; excluded paths /healthz, /readyz, /, /welcome.html, /style.css, /zava-logo.png, /sign-in), resource group `ama`. Ingress transport `Http` on both. API image `zava-forward-api:4d56cf609` (includes the HTTP/1.1 keep-alive fix).
* The resident test user is a demo-app account, not an Entra identity, so it cannot obtain an Easy Auth token for the API (staff token blocker recorded in deploy-main-810-462). The authenticated burst is therefore signed-in resident traffic, plus unauthenticated Easy Auth traffic to the API.
* `/demo/view` needs the `X-Resident-Session` header (value from `/demo/session`); the server bounds concurrency to 8 (`MAX_CONCURRENT`).
* Credentials were read only in code from the owner file. Scripts and evidence were scanned for the values (none present). Screenshots mask the email fields.
