---
title: Issue 153 exact button names details
ms.date: 2026-11-13
---

## Details

* Briefing: `const retry = !content.childElementCount;` then `ownedNotice(..., retry ? "use Try loading briefing again, then contact application support if it continues." : "use Refresh briefing, then contact application support if it continues.")`.
* Startup: `error.reloadWorkspace ? "choose Reload workspace, ..." : "choose Try again, ..."`.
* Tests: source-level assertions that each message names exactly one button in its branch, plus node evaluation of the branch expressions against the extracted `ownedNotice` helper for both states. Browser rendering is covered by existing browser checks, not run here.
