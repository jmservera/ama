---
title: Details for #184 slice 2
ms.date: 2026-11-08
---

* Control document schema `live-sim-control-v1`: `version`, `enabled` bool, `expires_at` UTC `YYYY-MM-DDTHH:MM:SSZ`, `approval_reference` non-empty, `owner` named, `homes` list of 1..100 unique home ids. Unknown keys, duplicates, past or more than 14 day expiry (at start) refused with fixed codes.
* `decide(control, now)`: expired when `now >= expires_at`; stopped when not enabled; else send.
* Sender: `--control-file` (or `ZF_SIM_CONTROL_FILE`); required for `--sink iothub`; cohort is control homes present in the store; fixed 100 cap constant shared with the receiver binding limit.
* Receiver entry: `python -m zava_forward.api.live_receiver --control-file F --seconds N --events M`; Activation needs routing readiness attested by `ZF_SIM_ROUTING_READY=1`, an owner-verified fact.
* Retained interface frozen for the UI and AI slice: stored live envelope keeps `sensor_id`, `reading_id` `LIVE-<sensor>-<UTC slot>`, `home_id`, `observed_at`, `temperature_c` (C), `humidity_pct` (%), `sunlight_wm2` (W/m2), `source_type=SYNTHETIC`, `schema_version=live-sim-reading-v1`, `label`; never calibrated indoor evidence; missing pre/post retrofit context stays explicit.
