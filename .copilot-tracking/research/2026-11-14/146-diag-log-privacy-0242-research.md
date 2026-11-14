# Research: diagnostic log privacy (Refs #146 criterion 4)

* Bicep: 13 diagnosticSettings, all workspaceId-only; IoT Hub allLogs disabled; storage/token stores audit group only; SQL server SQLSecurityAuditEvents only; Front Door access and WAF logs only. No content-bearing category enabled.
* Runtime logging: core diagnostic_logging.install_diagnostic_redaction covers every Logger record (args, extras, exception text); entrypoints install it. Resident demo and server error prints emit exception class names only.
* Finding: live_simulator StdoutSink dry run printed the full raw reading body to stdout, which reaches ContainerAppConsoleLogs under allLogs. print bypasses logging redaction.
* Not leaks: auth._deny prints tenant ids and role names (no names or emails); StreamError and ConsumerError carry fixed codes.
* Planning readiness: Ready.
