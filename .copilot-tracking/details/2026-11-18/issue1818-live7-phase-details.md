<!-- markdownlint-disable-file -->
# Issue 1818 live round 7: phase details

* Phase 2 steps: assign Registry Contributor (IoT Hub) and Event Hubs Data Receiver (event hub) to `id-cutover-test-api`; create the manual job with the demo app environment plus `ZF_SIM_HUB_HOSTNAME`, `ZF_DEMO_HOMES`, `ZF_DEMO_SLOTS=3`, `ZF_DEMO_CLEANUP=1`, `ZF_DEMO_EH_NAMESPACE`, `ZF_DEMO_EH_NAME`; start; read the result from the execution status and Log Analytics; delete job and role assignments.
* Phase 3: Playwright scripts read credentials at runtime from the home-directory files and never print them.
* Stop conditions: any step needing a deletion of a non-throwaway resource, a push to the registry, or a cost beyond the cap.
