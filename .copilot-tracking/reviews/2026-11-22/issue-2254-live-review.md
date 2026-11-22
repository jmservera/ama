# Issue 2254 review (single pass)

Executed once. Outcome: conformant for the local fix.

* Fix is one tuple member; Azure SQL bool handled by norm().
* Open: live confirmation after deploy; startup repair cost grows by one comparison per row.
