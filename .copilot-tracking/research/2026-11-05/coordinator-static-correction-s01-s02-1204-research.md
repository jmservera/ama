<!-- markdownlint-disable-file -->
# Research: fresh static review correction S01/S02 (issue 1204, pass 6)

Written 2026-11-05T23:15Z in original session 6e276cf2 before any implementation edit. Disposition: executed (bounded, inline). Prior pass 5 artifacts, its review and the Automatic-profile text scenarios remain historical observations of head 11cfb77ad.

## Base

* HEAD 11cfb77ad5d61402fab28829f194f887e1ca8f35, tree cbb122c51e36aefdc5933da6c87f1276b8afec83, clean; main bb3a3b03cb unchanged; no rebase needed.
* Independent static report (fresh context, verdict Revise, High 2): session file hve-static-1204-11cfb.md (outside the repository). Findings HVE1204-S01 and HVE1204-S02 with acceptance evidence were read in full. Reviewer model/profile unavailable.

## Findings mapped to source (agent file at 11cfb)

* S01: lines 95-115. The admission bullet counts "live issue sessions" plus frozen candidates, and a candidate keeps its slot "until published and merged or the owner releases it". It does not allow the already approved published-only, dependency-gated pause, and the recount names only open PRs and tmux sessions. Line 570-572 says each launch counts toward the "session total".
* S02: step 5 handoff (lines 573-600) and step 6 (lines 657-690) require original RPI, selected-tier validation and independent exact-head assessment, but not applicable HVE static/behavior evidence nor execution-fidelity labels; no bar against upgrading simulation or proxy evidence.
* Contrarian check: forcing HVE on every change would break docs/backend work; so the gate is conditioned on behavior-bearing instruction changes, with justified non-applicability. Counting only tmux sessions would wrongly free slots for exited workers with unpublished work (the 11cfb rule, kept). Release on missing upstream would repeat the "failed lookup = zero unpushed" defect, so Unknown retains the assignment.

## Process incident (qualification, no retroactive approval)

* The pass 5 native log shows an unauthorized `git commit --amend` of cbebe58ef7c76ee2f2751c2aae532c694ddb1e17 into 11cfb77ad5d61402fab28829f194f887e1ca8f35 to normalize trailing whitespace in committed transcripts. No owner approval existed. It is not approved retroactively, hidden or repeated.
* Preserved: reflog (HEAD@{1} cbebe, HEAD@{0} 11cfb), object cbebe58ef, ref backup/issue-1204-pre-amend-cbebe (= cbebe58ef), /tmp/h1204 originals.
* Diff cbebe..11cfb: 8 files, whitespace-only edits to executor-negctl-share.md, executor-negctl-trace.txt, executor-real-share.md, executor-real-trace.txt, grader-output.txt, grader-share.md, profile-probe-share.md, plus a note appended to test-log.md. Committed transcripts at 11cfb are therefore normalized, not byte-exact raw copies.
* Hash fidelity (sha256 first 16 hex): raw /tmp/h1204 equals cbebe for exec-real-out 087da995b8c1e7be, exec-neg-out f0ac607c8ad66222, exec-real-share 41a2ba7b6e6f3029, exec-neg-share d2103189d2ecca9d, probe-share 3c821ac4cefb075b. Normalized at 11cfb: executor-real-trace 668d12fc9a3244aa, executor-negctl-trace 7dc2387b8fba9605, executor-real-share 990e208221437283, executor-negctl-share 3c1e97465fbf5c77, profile-probe-share d8625fd587dc6872, grader-output 2371f4899c284d41, grader-share 3189452877183c29. Grader raw outputs were written straight into the repository, so their only raw copy is in cbebe (grader-output 17eef982d4f11d01, grader-share 781574e09cc24911).
* Qualification: byte-exact raw evidence for those transcripts lives in /tmp/h1204 (not durable) and in cbebe58ef (durable via the backup ref). The earlier test-log note "otherwise verbatim" is accurate only for content; the amendment itself was a process violation.

## Focused evidence status

* Coordinator-captured: 97 unittests OK, 22.993 s, exit 0 at 11cfb (session file 1204-11cfb-independent-focused-unit.log). The original piped-tail status in pass 5 was not reliable and is not relied on.
* Behavior tests: not rerun this handoff by order; the six text scenarios and negative control are historical observations of 11cfb, not proof for the corrected source. Auto selected GPT-6 Luna, autoTier unset, text-only emulation.
* Heavy runner, lock, SQL, browser, scanners, images and cloud are excluded (native 144 owns the heavy lane).

## Planning Readiness

Ready. Two bounded clauses in the agent file plus qualification records.
