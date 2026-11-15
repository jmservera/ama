# Details: unified pack 1905

* Use `git cherry-pick -x`-free picks (preserve messages); on conflict, union both sides.
* Inventory regeneration only if test_cutover_audit fails or reference lines shifted.
* Final commit amends nothing from picks; tracking files of this run committed in a separate commit.
* Tier: Focused; no push, no issue edits, pip only.
