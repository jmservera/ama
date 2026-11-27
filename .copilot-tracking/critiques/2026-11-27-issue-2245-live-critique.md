# Critique: issue 2245 live (executed once, 2026-11-27)

Verdict: proceed with changes applied.

* Retry only the single-transaction message write; retrying audit writes or the whole ask could duplicate a committed step or a model call. Applied (audit untouched).
* Do not return an unsaved answer: the thread record and audit are governance evidence. Applied (a persistent lock-busy still raises, giving the existing 500/503 path).
* Keep the retry count small (2) so total wait stays under the 240 s ingress limit (15 s lock wait x 3 plus the model call). Applied.
* A fix cannot be proven live without a deploy; deploy is not authorised by the goal. Recorded as unproven.
