# Details: issue 100 r1

* role-screens.js: `usageCount`, `usageTotal` and `assetUsage(report)`. Integer fields render as numbers, anything else as Unknown. Denominators: proposals with a call = measured + missing; accepted proposals sit beside it. Alerts table lists owner, reason and route (25 rows max, with the existing truncation notice). Other cost components show Unknown or the supplied amount with currency. Total Cost of AI stays Unknown unless the report supplies it.
* Report missing: blocked panel stating Unknown is not zero, owner and next action.
* test_asset_board_screen.py: two new tests.
* Docs: atlas-screen-trace.md row and log.md entry.
