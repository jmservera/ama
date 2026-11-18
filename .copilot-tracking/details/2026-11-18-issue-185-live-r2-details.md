---
title: Details for issue 185 live plan
date: 2026-11-18
---

Driver lives in /tmp only. Keys are held in process memory; the driver prints device ids, status codes and a boolean for key leakage. Teardown order: devices, job, role assignment. Abort if any device remains.
