# Critique: issue 1840 live2 (single pass)

Verdict: proceed. Risk: sys.path handed to the worker widens self-test import path; acceptable because the self-test is labelled lower fidelity and the image path is unchanged. Alternative (env var read inside the worker) rejected: it would alter the file shipped into the old image. Src change means FULL-tier classification applies in principle; the owner brief forbids `rpi-checks.py --all`, so this is recorded as unmet.
