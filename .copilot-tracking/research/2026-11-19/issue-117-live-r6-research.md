# Research: issue 117 live, sixth pass. Refs #117.
Goal: first unticked criterion ("Uploads are scanned before availability") on the synthetic demo.
Planning readiness: Ready (reused prior evidence plus new live probe, see docs/reference/research/issue-117-live-r6-2026-11-19.md).
Finding: Defender for Storage on stcutovertestrzsrg is isEnabled true (consistent with the r2 correction). Demo API still lacks ZF_SCANNER=defender. Direct tag probe from this host is refused by storage network rules.
