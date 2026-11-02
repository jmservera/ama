# Plan

* In fetchReadRetrying keep cold-start retries; remember the status text replaced by the retry message and restore it in `finally` (success, failure or abort) only if the message is still shown.
* Validate: design_system_browser_check x5, employee_acceptance_check, test_workspace_scripts.
