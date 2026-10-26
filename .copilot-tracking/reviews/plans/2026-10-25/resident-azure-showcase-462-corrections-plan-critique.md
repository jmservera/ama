# Critique: corrections plan (issue 462)

Run once on 2026-10-25 by an independent read-only agent before implementation. Original verdict: Revise (2 blocking, 4 non-blocking, 1 suggestion). Not repeated.

1. Blocking: the tool cannot promise swap or memory safety. Applied: claim removed; residual stated; run only on an owner-controlled machine.
2. Blocking: leak controls underspecified. Applied: `main(argv, stdin, stderr, prompt)` contract, argv rejected, tty required, generic errors with no traceback, subprocess tests for argv and piped stdin.
3. Non-blocking: "one client cannot lock another" overstated. Applied: precise wording and a test that the global cap lockout remains.
4. Non-blocking: XFF tests need multi-line, IPv6, malformed, port or bracket fallbacks, client-prefix cases. Applied.
5. Non-blocking: policy is easily satisfied by predictable patterns. Applied: repeat-unit, distinct-character and common-substring rejection; the tool advises a password-manager-generated random value and states that rules are not proof of strength.
6. Non-blocking: stale-email tests need old and new email. Applied.
7. Suggestion: keep scope narrow. Accepted.
