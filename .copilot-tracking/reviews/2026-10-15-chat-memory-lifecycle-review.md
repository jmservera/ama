# Review: per-user memory lifecycle (#161)

Execution: once, after implementation. Outcome: conformant with open items.

| Criterion | Evidence |
| --- | --- |
| Off by default, informed opt-in | `test_off_by_default_and_needs_informed_opt_in` |
| Content, source, dates, expiry; edit, delete, clear | `test_items_are_inspectable_editable_deletable_and_clearable` |
| Excludes special-category data | `test_special_category_and_unknown_class_refused` |
| Never overrides rules or cited as evidence | `test_prompt_memory_is_non_authoritative_and_never_evidence` |
| Retention per class Unknown until DPO | `test_retention_unknown_per_class_until_dpo_approves` |
| Global and per-task disable | `test_global_and_task_switches_need_an_administrator` |

Open items (routed, not done): administrator app role decision; DPO retention approval; UI and endpoint wiring; SQL Server run (`ZF_TEST_MSSQL`) not executed here.
