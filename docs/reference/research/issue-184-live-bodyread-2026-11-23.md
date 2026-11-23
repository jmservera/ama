---
title: Issue 184 live message-body read attempt (demo, 2026-11-23)
description: Attempt to prove secret absence in live Event Hubs message bodies, and why the network blocks it
ms.date: 2026-11-23
ms.topic: reference
---

Scope: synthetic demo, resource group `ama`. This follows the [live re-check](issue-184-live-recheck-2026-11-23.md), which left one element unproven: secret absence in live message bodies. Refs #184. No credential was printed.

## What was done

* A temporary Azure Event Hubs Data Receiver role was assigned to the CLI user on `eh-iot-cutover-test-rzsrg/sensor-readings` and deleted afterwards; a check shows 0 user assignments remain. The pre-existing service principal assignment was left alone.
* A bounded read (events from the last 2 hours, body scan for `SharedAccessKey=`, `SharedAccessSignature sr=`, a device connection string, private key blocks, `AccountKey=`, JWT-like tokens and secret-named JSON keys) was run once load-balanced and once per partition. Only counts would have been recorded.
* Both runs received 0 events: the AMQP connection failed with `CBS Token authentication failed`.

## Why it cannot be proven for the demo

`eh-network.json` shows `publicNetworkAccess` Disabled and `disableLocalAuth` true. Only in-network readers can open the namespace. Enabling public access, adding a firewall rule or exec into a production container would change the estate, which the goal does not authorise. The scan script, `eventhub-body-scan.json` (0 events) and the job listings are under `.copilot-tracking/evidence/2026-11-23/issue-184-live-b/`.

## Current state

Simulator job `job-live-simulator-29924055` Succeeded at 14:15 UTC, running every 7 to 8 minutes; the receiver job runs every 30 minutes (`sim-executions.txt`, `receiver-executions.txt`).

## Outcome

No code gap and no source change. Secret absence in live message bodies stays unproven; the constructed fake-SDK test remains the only evidence for it. A future proof needs an in-network reader, such as a one-off job in the Container Apps environment, which is an owner decision.
