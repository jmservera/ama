<!-- markdownlint-disable-file -->
# Critique: issue 1288 H1 restart-context plan

Single critique (rubber-duck, independent, read-only), executed before any observation; readback `date -u` 2026-11-09T23:37Z. Verdict: Revise, 3 blocking, 0 non-blocking. Timestamp note: the research, plan and details files state 23:36Z and 23:37Z; a readback at 23:36:43Z shows the 23:37Z stamps in plan and details were rounded about 20 seconds early. No observation preceded any of them.

## Findings and dispositions (all applied, see plan amendment)

1. `release_support.install` deletes and recreates the `fx-*` release rows, so variant B would mutate the durable evidence under test. Applied: B must not touch the database; it only sets in-memory provider context.
2. The confirmation criterion could pass vacuously. Applied: require the baseline `review-suggested`, A `not-current`, non-empty citations, unchanged persisted rows and a context-specific guard explanation (denial reason, constructed-versus-live, release reference mismatch).
3. Reusing the first provider shares state and installation mutates its release callback. Applied: B uses an independent equivalent `CapturingProvider()`; durable state is snapshotted around each variant; suspension, denial reason, stored and current release reference and `runtime_binding` digest are recorded.
