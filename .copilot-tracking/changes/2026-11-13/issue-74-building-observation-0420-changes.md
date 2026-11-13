<!-- markdownlint-disable-file -->
# Changes: #74 buildingView operational observation (issue-74-building-observation-0420)

Date 2026-11-13. Head e8dec941d567653c02163f551874ca26f2b527fa. No product, check, test or config change; only tracking files added. This is the narrower alternative to the V2-proposed check edit, which root did not admit; no added source budget or history is used.

Outputs (retained, not committed) in `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/74-building-observation-0420/`: `observe_final.py`, `run.sh`, `run.log`, `observation.json`, `preflight.txt` (SHA-256 prefixes e1bfc369, 87b3a528, adc1b079, 604be20e, 9233a9e8). `observe.py` there is an earlier draft superseded by critique and never run.

## Preflight and isolation

Lock `/tmp/ama-rpi-heavy.lock` non-blocking, regular non-symlink, owner azureuser, inode 77057; MemAvailable 4.87 GiB; no prior server or Chromium process; window 04:17:28Z to 04:17:32Z. Frozen b0e venv interpreter, `env -i`, owned HOME and scratch, no private ZF_DATA (the harness wrote its own temp fixture). The harness module imported from this checkout (`checks_module_under_checkout` true). Chromium 156.0.8078.4 from the read-only cache. No install, download, SQL or cloud.

## Observed (one run, exit 0; harness server PASS printed, then OBSERVATION RECORDED)

* Journey: Programme Manager login `pam@example.test`; `#/case-home/ZF-2`; the existing link `Open full building context`; route `#/building/SYN-B1`; `/api/buildings` response status 200 (one).
* One h1 and six h2 sections, each exactly once and visible: Shared systems, Dependencies, Work stopped pending review, Shared works, Shared building costs, Linked home cases.
* Per-section markers: SYS-1 only in Shared systems; DEP-1 only in Dependencies; HOLD-1 only in Work stopped pending review; WORK-1 in Shared works and as the work reference in Shared building costs; COST-1 and GBP 12000.00 only in Shared building costs; ZF-2 and ZF-3 both in Linked home cases; "Affected homes" shown on Dependencies, holds and works (ZF-2 listed), not on systems.
* Home-only sentinels (own document, own quality, decision, allocation source) were first seen on the ZF-2 home view, and none appeared anywhere in the building main. GBP 6000.00 home allocation did not appear on the building screen. Sentinels from the sibling home were absent from the ZF-2 home view by design, so their absence on the building screen shows nothing.
* Zero controls in `main`; zero non-safe requests after sign-in (guard would have aborted and counted any; count 0); zero non-loopback requests (guard count 0); zero page JavaScript errors.

## Cleanup

Harness terminated its exact server and the driver closed the browser. The runner's exact process group (PID 1125857) had 0 members afterwards; no server or Chromium remained; owned scratch empty. No name-based kill; nothing else removed. Lock held through cleanup, then released.

## Not shown

Not AT, WCAG, whole criterion 2 or outcome acceptance; not permanent regression coverage; one synthetic fixture, one role, one building. Finance-restricted and non-finance cost views, ZF-3 origin and unknown (null) items were not observed. Residual: harness port-release race (PC-008) unchanged. G5 applicability on the home panel, CR-002 unknown funding and author chronology limits unchanged.
