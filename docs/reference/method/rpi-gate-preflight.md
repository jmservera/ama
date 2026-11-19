---
title: RPI gate preflight and timing method
description: Non-receipt change-specific preflight, full-gate timing analysis and benchmark protocol for the local RPI gate
ms.date: 2026-11-18
ms.topic: reference
---

## Purpose and boundary

This method gives developers a repeatable way to run the specific checks that
matter for a change before committing and before starting a full gate, and a
read-only way to analyse where a full gate spends its time. It implements the
standalone part of issue #1830.

* A preflight result is development feedback. It is not a receipt, does not
  satisfy the full tier, independent review or hosted CI, and carries
  `"receipt": false`, a fixed non-receipt label and none of the receipt fields.
* Nothing here removes, skips or loosens a required full-gate group, the real
  SQL and browser controls, scanners, fresh images, receipt scope or the
  `--changed`, `--jobs` and `--resume` policy in the
  [local RPI gate](../../../src/README.md#local-rpi-gate). The full gate and
  its verified receipt remain required for big features, releases,
  infrastructure, deployment, SQL and security-sensitive changes.
* The tools are standalone and are not wired into the gate or the `src-ci`
  workflow. Their tests are direct local checks: hosted CI does not run them.

## Preflight: `tools/rpi-preflight.py`

Current state (correction 5, issue #1830): every request that would import or run
repository-controlled code is refused with exit 5 before the first subprocess,
including `git`, and including `--dry-run`. That covers `--test`,
`--browser-test`, `--browser-check` and `--sql-test`. Nothing is imported,
discovered or run, so the rules below describe retained mechanics that the
command line cannot reach; only test fixtures reach them. Reason: an independent
pre-gate security diagnostic found that a selected new or changed browser
wrapper or test could import the existing SQL harness (`checks.sensor_sql_check`)
through module code, a test method, a `load_tests` hook or discovery, and that a
selector can name any zero-argument callable. Both are conditional attack paths
(a selected unsafe wrapper plus the harness prerequisites); no unsafe wrapper
exists in the candidate and no host exploit was shown. The boundary options were
evaluated and none holds: a textual or syntax denylist cannot prove Python free
of a capability; a positive import allowlist rejects nearly every real test
because `subprocess` and `socket` are also what ordinary tests and product code
use; environment scrubbing and rechecks do not bound code that synthesizes its
own settings; and runtime isolation (user, network and mount namespaces) is
unavailable without privileges (unprivileged user namespaces are blocked by
policy on the development host and no sandbox tool is installed). Arbitrary test
code is not a sandbox. Unmet criteria of #1830: change-specific unit, browser
and SQL preflight feedback is not delivered, the preflight runtime benefit cannot
be measured, and the live SQL criterion stays unmet. Follow-ups: a human-owned,
digest-pinned admission manifest with a per-entry capability review, a trusted
isolation helper on hosts that allow it, and the trusted SQL broker below. Use
the full gate for these checks.

Prerequisite: a Python environment with the `src/<project>` distributions
installed editable from the checkout under test. Every `zava_forward.<project>`
package (core, agents, api, orchestrator, importer) must resolve inside this
checkout's `src/<project>/src`; a mixed checkout exits 5. The helper never
installs, creates an environment, starts Docker or edits a file.

```text
python3 tools/rpi-preflight.py --python VENV/bin/python \
  --file src/api/src/zava_forward/api/store.py \
  --covers src/api/src/zava_forward/api/store.py=api:test_example \
  --test api:test_example
```

Rules, all fail closed:

* Selectors are exactly `PROJECT:test_module[.Class[.method]]`, the grammar
  the gate accepts for `--extra-test`. The module must exist under
  `src/PROJECT/tests/`, tracked or intended. Option-like values, `..`, absolute
  paths and symlink escapes exit 2.
* Each selector is loaded in the target interpreter first. Zero tests, an
  import failure or an unknown class or method exits 2 without running
  anything. After the run the count must equal the listed count and the output
  must end in a plain `OK`; any skip, such as a browser test without
  `ZF_BROWSER_TESTS=1`, exits 1. Use `--browser-test` for opt-in browser tests.
* Coverage is declared, not inferred. Each `--file` needs `--covers FILE=TARGET`
  naming a supplied selector or check, and a reviewed table adds required areas:
  `src/core` needs every consumer project, `src/agents` needs agents and api,
  `src/api` web or checks paths need a browser target, and store, schema, SQL,
  assistants or core sensor files need a SQL selector. Documentation paths are
  inert. Dockerfiles, requirements, `pyproject.toml`, workflows, `infra/` and
  every unmapped path, including new `tools/` files, are reported uncovered and
  exit 3. `--allow-uncovered` still runs the tests, prints a warning and exits 3,
  so it never yields a pass.
* The output states that coverage is declared and relevance is not verified,
  and that images, scanners, hosted CI and the receipt are gate-only.
* Browser checks (`--browser-check NAME`) run `python -m checks.NAME` from
  `src/api` for a tracked `src/api/checks/NAME.py`, with scratch directories
  redirected as in the gate. A check that takes `--axe` needs the pinned
  axe 4.10.3 file (sha256 `880970c0...a68bb`) and `--out`, outside the repository
  and at most 58 bytes. Browser and SQL paths take
  `/tmp/ama-rpi-heavy.lock` without queueing and exit 5 when it is busy, so they
  never run beside a gate. Missing Chromium exits 5.
* SQL (`--sql-test`) is refused (exit 5) and SQL execution is disabled (correction 4, issue #1830).
  Since correction 5 the refusal follows only the check that a selector was named and precedes
  every other validation (including coverage, so exit 3 is unreachable from the command line),
  `git`, interpreter probing, the heavy lock, Docker, `/proc`, socket, discovery and test
  contact, and it also applies to `--dry-run` because discovery imports test code. The
  correction 4 textual browser heuristic was removed in correction 5: it could not see imported
  helpers, and every browser check and unit selector is now refused (see above). Reason: an independent pre-gate
  security diagnostic found two High issues that no unprivileged design here resolves. First,
  `SO_PEERCRED` identifies who created the Docker socket, not who accepts on it, so metadata and
  a genuine unrelated root `dockerd` and `docker-proxy` cannot bind the actual acceptor and the
  SQL listener to the inspected container. This applies only if a root-created socket is handed
  to an unprivileged acceptor selected by the victim's Docker context; that host configuration
  is conditional and was not shown to exist on the development host. Second, verification
  happened before discovery and before separate SQL connections, so a port released by container
  lifecycle activity could be rebound before or between connections; a post-run recheck is too
  late. A future mechanism must prove acceptor identity, disposable-target ownership and
  endpoint pinning through discovery and every connection (for example a trusted host-side
  broker or an independently provisioned, pinned end-to-end SQL identity); no bounded
  unprivileged design was found, which is not a proof that none can exist. The live SQL
  criterion of issue #1830 is unmet. The paragraph below describes the retained, unreachable
  metadata and listener correlation checks, kept unchanged under their tests as necessary but
  insufficient preconditions; it no longer describes behaviour.
* Retained SQL precondition checks (`--sql-container ID --sql-owner TOKEN`, no longer reachable):
  loopback alone does not prove a
  disposable database, because the store tests drop tables. The helper refuses unless
  `DOCKER_HOST`, `DOCKER_CONTEXT` and the TLS variables are unset and the current Docker context
  is a local `unix://` socket (a remote daemon is never accepted). It then inspects the container
  read-only and requires it to be running, to use the `mcr.microsoft.com/mssql/server` image,
  to carry the `ama.rpi.owner` label equal to your `--sql-owner` token, to publish
  1433 only on `127.0.0.1` at `ZF_SQL_PORT` with a local listener on that port, and to hold a
  `MSSQL_SA_PASSWORD` equal to your `ZF_SQL_PASSWORD` (so the connection authenticates against that
  container; the value is never printed). Because a persistent data volume would let the
  destructive fixtures change real data, it also requires disposable provenance from daemon
  metadata: no mount of any kind (named or anonymous volume, bind or tmpfs), no `Binds`,
  `Mounts` or `VolumesFrom` in the host configuration, no restart policy, creation and start
  times that parse with a zone, are not in the future (60 s skew) and fall within the last 6
  hours, and an image, looked up by its id, whose repo digests all start with
  `mcr.microsoft.com/mssql/server@sha256:` (a locally built or retagged image is refused). Any
  missing or unparseable field refuses. The caller supplies `ZF_TEST_MSSQL=1`,
  `ZF_SQL_SERVER=127.0.0.1`, password authentication as `sa`, a database named `rpi_*`, the port
  and the password. The container is inspected again once the heavy lock is held, before the SQL
  group and after it. The caller starts the container with the gate's flags
  (`--label ama.rpi.owner=TOKEN --publish=127.0.0.1::1433`, a generated password
  passed by environment and `--memory=3g --cpus=2`), with no volume or mount, and removes it
  afterwards.
  Credentials are masked in output. Provenance of the daemon and the listener comes only from
  kernel-side evidence, never from the Docker endpoint, because a proxy to a remote daemon can
  return consistent fabricated metadata and neither labels nor `ZF_SQL_PASSWORD` bind the inspected
  container to the loopback listener. Before any request is sent to the endpoint the helper
  requires the process to be in the initial user namespace (identity `/proc/self/uid_map`, so
  uids are not remapped), the context socket to be a real socket owned by root in directories
  that only root can write, and `SO_PEERCRED` of a bare connect to report uid 0 (an `ssh -L`,
  `socat` or other user-created forwarder reports its own uid). Every later `docker` call pins
  that verified path with `--host`. After the metadata checks it requires exactly one root
  `dockerd`, exactly one TCP listener on the port (no wildcard, IPv6 or second listener) that is
  on `127.0.0.1`, owned by uid 0 and has an inode, and exactly one root `docker-proxy` process,
  a child of that `dockerd`, whose command line is `-proto tcp -host-ip 127.0.0.1 -host-port P
  -container-port 1433` with `-container-ip` equal to an address of the inspected container. A
  process vanishing or unreadable in `/proc` is skipped unless it is a Docker process; Docker
  process identities (pid, parent, start time, owner, command line) must not change during the
  check. These evidence checks run at every inspection. Residuals and unmet criteria: the
  listener socket inode cannot be mapped to a process without root, so the binding is by uid,
  port, address and parentage and does not defeat a root or root-equivalent actor (including a
  root-configured socket-activated forwarder) or a swap by the daemon itself; the check is a
  point-in-time proof bracketed by re-checks, and the database driver connects by address, so no
  verified connection or mediator pins the endpoint for the run; a rootless daemon or
  `userland-proxy` disabled has no root `docker-proxy` and is refused (fail closed); freshness and
  absence of storage are still inferred from daemon metadata and ownership is not a
  helper-created trusted manifest, which needs a runner change. The controls are tested with
  isolated fixtures, mutation checks and one real unprivileged unix-socket proxy only; no
  container, SQL server or live listener was contacted, so a live exercise, the full receipt and
  independent exact-head review remain unmet and the SQL part of the preflight criterion of
  issue #1830 is not claimed complete. The gate, not the preflight, proves ownership and cleanup.
* Execution uses argument lists, no shell, no stdin, a new process group killed
  at `--timeout`, and a scrubbed environment.
* A content digest of every tracked, untracked and ignored file, plus
  `git status --ignored`, is taken before and after. Any change exits 4 and
  names the paths. The `--out` directory must be outside the repository and must
  not contain `receipt.json`; `preflight-result.json` is written there.

Exit codes: 0 pass, 1 test or check failure or unexpected skip, 2 invalid input
or zero tests, 3 uncovered (also when `--allow-uncovered` lets tests run), 4
source mutation (reported even when a selector then fails to import), 5 prerequisite or lock, 6 `--dry-run` validated and listed
tests but ran nothing. Only exit 0 is a pass.

## Worked cases

These are recipes for the retained mechanics and are refused by the current
command line (correction 5). They have not been replayed on the real heads, because the
shared heavy lock was owned by another gate when this method was written. Do not
treat them as run until the commands, exits and logs are recorded on a final
head under a free lock.

* #1828 map check at the #1829 head
  (`3a7c655603eeae861c476eca1268a0188efde9bc`), in a new detached worktree
  with an editable environment: `--file src/api/checks/map_fullscreen_browser_check.py
  --covers ...=map_fullscreen_browser_check --test api:test_map_sensors
  --browser-check map_fullscreen_browser_check --axe AXE --out OUT`. The check is
  local-only: neither `src-ci` nor the gate browser group runs it. PR #1829
  reports 330 PASS, 0 FAIL and 14 axe scans without violations; the helper does
  not re-derive these.
* #1297 320 px: run `--browser-check design_system_browser_check` and
  `--browser-check case_journey_browser_check` with the changed `src/api` path
  declared against both. The 320 px assertions are in
  `design_system_browser_check.py` and `case_journey_browser_check.py`. The claim
  that the regression is caught before a full gate needs a failing run on the
  regressing head and a passing run after the fix.
* Negative cases that need no lock: `--test api:../x` exits 2;
  `--test api:test_does_not_exist.Nope.method` exits 2; an uncovered
  `tools/` path exits 3 only when the retained mechanics are reachable (fixtures); from the
  command line any selector, check or `--sql-test` exits 5 before git or Docker contact.

## Timing: `tools/rpi-gate-timing.py`

Read-only and standard library only.

* `report RECEIPT [--log RUNLOG]` accepts only a regular file whose sibling
  `receipt.sha256` matches and whose schema is 4, status `passed` and scope
  `full`. The digest is an integrity check, not gate verification
  (`rpi-checks.py --verify-receipt` is separate). It reports the command span,
  per-group start, end, wall time and summed command time, idle gaps inside a
  group, a concurrency histogram, the ten longest commands, setup command time,
  queue wait and lock-to-seal time from the log, and an observational critical
  chain. The chain walks back from the last finisher through the latest command
  that ended before each start, so a group holding a worker slot appears as a
  step; it is not causal. Group durations overlap and must not be added.
* `host-manifest` prints CPU model, vCPU count, memory, Docker server version and
  load. The receipt records none of these.
* `compare --before R R ... --after R R ...` needs at least two distinct receipts per
  arm (none shared between arms, all with identical selection, jobs, image mode,
  tool digests, executed group set and a per-group scrubbed command contract: argv, working
  directory, environment and the timeout, suite, integration, probe and attempts flags), a complete host manifest (nonblank CPU model and Docker version, positive vCPUs and memory) and an operator-supplied verification record per arm
  (the `--verify-receipt` command, exit 0 and checkout, asserted and not
  re-verified). It refuses with `NONCOMPARABLE` (exit 3) when selection, jobs,
  image mode, tool digests, executed groups, command contracts or host differ, or when the heads differ other than
  by `tools/rpi-checks.py` and its test with `--allow-tree-delta RUNNER_ONLY
  --repo CHECKOUT`. Only per-run values are masked: the container operand of
  `docker inspect`, `rm`, `logs`, `stop` and `kill` when it is a bare 64-hex id, the
  `ama.rpi.owner` label token and the `ZF_SQL_PORT` value. Image ids such as
  `docker image inspect sha256:<id>` stay literal, so image drift is refused. Receipt `images`
  identity is also compared: every executed image group (`mssql`, `image-*`, `logo-0600`)
  needs a well-formed `sha256:` id, the image sets must match and the pulled `mssql` base id
  must be equal across receipts. Qualification: ids of images built by the gate legitimately
  differ per build and are recorded but not compared, and the receipt does not record the base
  images of the built images, so base drift behind a built image cannot be detected. It reports medians, minimum and maximum, and no significance
  statistic.

Reading the retained receipt `/tmp/rpi-1297-pyc-full-20261116T1530Z` (head
`132f0b1ca1a229556f7c48a5b9e64f63a556f5de`, `--jobs 2`, 217 commands, one
verified receipt on one unrecorded host) gave a 2732.9 s command span, 0.001 s
queue wait, 2748.4 s from lock to seal and 377.0 s of setup commands within
5838.3 s of overlapping command time. Concurrency was 0 or 1 for 1167 s,
2 for 765 s, 3 for 60 s and 4 for 740 s. This is one observation. Two
verified receipts per arm on a recorded host are needed before any comparison,
so the multi-receipt criterion of issue #1830 stays open.

## Benchmark protocol for a later optimization

No optimization is implemented here, so there is no before and after
measurement. The scheduling hypotheses in the
[research record](../../../.copilot-tracking/research/2026-11-16/issue-1830-gate-audit-research.md)
(queue wait for the browser group, late API start, the setup prelude and shard
balance) are unproven upper bounds from one receipt. A runner change needs its
own reviewed, owner-approved full RPI.

* Arms: A is merged-main `tools/rpi-checks.py`, B the same tree plus the change.
* Controls: one host with a recorded manifest, idle, heavy lock held, same
  `--jobs`, `image_cache: fresh`, new output directories, same pinned tools,
  two verified full receipts per arm in ABBA order and the scanner database
  date recorded.
* Acceptance: every receipt verifies at full scope, the required group set and
  per-group command contracts are identical, no mandatory group is skipped,
  reordered away or weakened, and differences are reported descriptively with
  host qualifiers. Otherwise the result is unproven.
* SQL and fresh-image work (about 36 percent of the span in the observed
  receipt) are required controls, not optimization candidates.
