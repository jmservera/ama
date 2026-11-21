# Review: issue 2190 (executed once)

Outcome: conformant for local scope. Gate tests 120 OK, api218 5 OK, mypy clean, ruff clean on changed src files, 6 of 6 loaded browser runs pass; no check relaxed.
Open: hosted CI and complete gate for this head (coordinator); flake 2 lacks a deterministic test. Witness note: implement-start recorded with source already edited, because the regression tests were ported first to reproduce the flake on unfixed code.
