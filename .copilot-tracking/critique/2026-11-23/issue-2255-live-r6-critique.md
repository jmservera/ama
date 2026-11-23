---
title: Critique, issue 2255 run 6
ms.date: 2026-11-23
---

Executed once. Verdict: proceed. Risk: distinguishing "key absent" from "value null" in the marker. The marker is only written by the running branch, which always stores `noticed_was`, so key presence is a sound discriminator; legacy markers without the key keep the old behaviour. The edit is private infra tooling, not deployed code: focused tier, classified by impact (no permission, image, secret or gate change).
