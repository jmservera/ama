# Plan critique: 521 Azure sync preflight

Executed once by `rubber-duck` before further probes. Verdict: Revise. Findings (numbered by the critic):

1. Probe output could expose ids; use allowlisted `--query` and withhold ids.
2. Workflow target is `workload=forward` (`pipeline.py`), not the observed `cutover-test` apps.
3. USD 5 gate not enforced by `chat_eval.py`; a pricing-aware hard-cap runner is required.
4. Go/no-go must derive from fresh probe results.
5. Dry-run check must test the exact value and exit status on Python 3.12.

Dispositions: all five applied directly in the research, plan and changes files. No user decision required.
