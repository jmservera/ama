# Review (single pass): issue 144 guard fix

Execution: self-review by the worker against the diff; independent exact-head review is the coordinator's.
Outcome: conformant for the stated scope, with open items routed below.

* No check relaxed: sticky-bit and zero-mask logic unchanged; a failed or lying drop still fails closed (tests cover both).
* `capset` keeps effective and permitted unchanged, so it cannot widen privileges; version 3 header with two structs matches the kernel ABI (verified by a real call and by the local simulation).
* Private directory check verifies ownership and forces mode 0700; a foreign-owned `zf` directory is refused. A pre-existing symlink at `zf` is followed by `stat`/`chmod`; the parent is a platform mount, so the residual risk is low (open item).
* Entry points that pass an immutable mapping skip repointing and rely on the guard failing closed.
* CapBnd inertness is an engineering argument; needs reviewer confirmation.
* Unverified: baseline comparison of unrelated host-dependency test failures; live receipt.

## Routed follow-ups

1. Owner-authorised revision deploy with `enforced` and capture of the receipt.
2. Use `os.lstat`/`O_NOFOLLOW` semantics for the private directory if the parent mount is ever shared.
