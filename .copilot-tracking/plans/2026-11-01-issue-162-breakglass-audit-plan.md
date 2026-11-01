# Plan: issue 162 break-glass audit with purpose (2026-11-01)

* [ ] Edit `src/core/src/zava_forward/core/chat_isolation.py`: include redacted purpose in the refused audit detail.
* [ ] Extend `test_break_glass_is_default_deny_audited_and_metadata_only` for purpose, target, policy ref on each entry and no content keys.
* [ ] Add OD-46 proposed policy options and recommendation to `docs/reference/research/chat-memory-dpia.md`; append `docs/reference/log.md`; adjust `src/core/README.md` open items.
* [ ] Validate: chat isolation tests, ruff check, ruff format --check, mypy for `src/core` and `src/api`.
* [ ] Commit, push, PR with `Refs #162` naming AC6 policy decision as unmet.

Critique (single pass, self-applied): do not tick AC6 or state the policy as decided; options are a proposal for owner and DPO; do not enable content access.
