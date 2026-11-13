# Details

* `ROUTE_FLAG` is exported from `runtime`. Standby loop: `while not stop.wait(IDLE_SECONDS): beat(heartbeat)`, after an initial beat. Signal handlers installed first so SIGTERM exits 0 immediately.
* Message is plain language: "queue consumption is off (standby); no tasks will be processed."
