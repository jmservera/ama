<!-- markdownlint-disable-file -->
# Critique: keyboard probe correction C2 (2026-11-10)

Execution: one rubber-duck critique of the final candidate plan. Both findings are compatible with the admitted scope and were applied directly.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Shape regex accepts a far-offset shadow as visible focus | Applied: supported ring requires zero x and y offsets and zero blur, spread of at least 2px; offset-shadow helper regression added |
| 2 | Transparent-shadow negative could pass if the shadow were merely absent | Applied: the mutation script reads the computed style after editing and throws unless the transparent non-black shadow and no outline are present, so the negative cannot pass on an absent shadow |
