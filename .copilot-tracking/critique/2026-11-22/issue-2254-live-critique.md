# Issue 2254 critique (single pass)

Verdict: proceed.

* Adding hazard to the repair comparison is the smallest change that gives one definition; both sides already share taskqueues.has_open_safety.
* Considered adding support, days and rkey: rejected, days/rkey drift with the clock and would rewrite every row at startup. Out of scope.
* Risk: Azure SQL returns bits as bool; the existing norm() handles it.
* Live proof of the fix needs a deploy, which is out of scope (no push); mark unproven.
