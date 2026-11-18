# Critique (executed once): issue #107 third pass

Verdict: proceed.
* Risk: claiming restart persistence proves "old images cannot restore revocation". Applied: the note states it shows a same-image restart keeping a suspension, not an old-image test.
* Risk: SUS-1 attribution rests on repository log and prior raw output, not a fresh `/api/continuity` read. Applied: note labels it as inferred from retained evidence.
* Risk: duplicate of r2. Applied: note scopes itself to the delta and reuses r2 test results by reference.
