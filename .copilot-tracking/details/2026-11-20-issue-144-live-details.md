# Details: issue 144 guard fix

* capset: header {version 0x20080522, pid 0}; two `__user_cap_data_struct` (effective, permitted, inheritable as u32). Read with capget, set inheritable to 0 in both, keep effective and permitted, call capset. Non-zero return raises nothing itself; the later zero-mask check fails closed. An OSError from the libc lookup returns a failure code.
* Private dirs: `os.makedirs(path, mode=0o700, exist_ok=True)`, then `os.chmod(path, 0o700)` and verify `st_uid == os.getuid()` and not group/world-writable; otherwise raise ContainerHardeningError.
* Helper runs only when `ZF_CONTAINER_HARDENING` is `enforced`; base paths come from `/tmp` and `/state` (parameters for tests). TMPDIR is always repointed; ZF_STATE only if already set. `tempfile.tempdir` is reset when `os.environ` is the target.
* CapBnd stays non-zero: needs CAP_SETPCAP to drop; with NoNewPrivs=1 and empty permitted/ambient sets, execve cannot raise capabilities, so the bounding set only limits capabilities that cannot be gained (reviewer to confirm).
