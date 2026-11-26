# Details: issue 2301 live

Phase 1: parse the "Remaining epic criteria as exact gaps" table (3 cells) from the checkpoint section; assert each epic cell is "All nine" or an epic in EPICS, and each gap cell names an owner. Factor a helper `non_continue_rows_cite_gap_issue(rows, body)` so synthetic input proves the rule fails.
