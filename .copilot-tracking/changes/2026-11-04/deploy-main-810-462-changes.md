# Changes (live, resource group ama only)

* Failed attempt: two `az acr build` runs (`dbm`, `dbn`) failed at hosted-agent registry login 403; no image produced. Registry restored each time.
* Pushed `zava-forward-api:main-b0080d4e1` and `zava-resident-demo:main-b0080d4e1`; registry readback Disabled, Deny, no rules, exports disabled.
* `ca-cutover-test-demo-api` -> revision `--0000014` (100 percent, Healthy, transport Http). `ca-resident-demo` -> `--0000009` (100 percent, Healthy).
* No SQL, role, network, secret or Bicep change. Repo change: docs only.
