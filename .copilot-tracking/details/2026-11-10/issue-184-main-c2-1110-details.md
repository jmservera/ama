<!-- markdownlint-disable-file -->
# Issue 184 correction C2: details (2026-11-10)

Append to the original changes record a section stating: parent PR 1417 merged to main as `583d4fbd` (Root-reported, whole #108 open); Root released target `main` (local reconciliation only); child now contains main via ordinary merge `a6c9ce7d`; the "Review not run" line and the C1 "holds remain" line are historical with this as the dated transition; remaining gates: Root independent exact-head review, hosted checks, publication, any live or Azure step; no whole #184 acceptance; five observations unchanged, two job 404s are exact names only, cost authority expired and not renewed, serving, runtime flow and image mapping unknown.

Validation: pre-append content is a byte prefix of the new file; links resolve; leak scan; diff scope only that append plus C2 files.

Critique PC-001 applied: the appended section also states the original chain stays QUALIFIED with verify exit 1, the C1 chain (verify 0) and its independent approval are separate and do not heal it, and the remaining holds are: Root independent exact-head review, hosted checks, publication and any live or Azure step.
