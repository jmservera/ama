# Issue 86 formal-complaints typing correction: critique

Scope: jmservera/ama#86 only. One independent critique pass (rubber-duck sub-agent, read-only), run before any source or test edit. Not repeated for this task. Verdict: proceed with changes.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocker | `parse_acknowledgement(value: object)` fails strict mypy 2.4.0 at `value.get("received_at")`; the earlier conditional does not narrow. | Accepted. Parameter typed `Any`: the value is an untrusted receiver reply already validated at runtime; no body change. |
| 2 | Blocker | A `complaints_receiver: ... = None` class default makes `hasattr(store, ...)` true and changes sentinel `getattr` and patching behaviour. | Accepted. Annotation-only declaration under `TYPE_CHECKING`; no runtime attribute. |
| 3 | Significant | Plan claimed whole-core-suite equality from focused tests. | Accepted. Plan now states whole-suite comparison is pending the FULL gate. |

Critique also reported that mypy accepted `NoReturn`, `SyntheticReceiver` structural compatibility, `os.environ` and test dict literals as `Mapping[str, str]`, and Any assigned to annotated locals; no import cycle; Store persistence serialises `self.data`, not the instance. These are the critic's probe results, to be confirmed by the real mypy run.
