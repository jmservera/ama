<!-- markdownlint-disable-file -->
# Corrected model-ID sidecar for run 002 (added 2026-11-06; original run-index.md unchanged)

* Original defect: run-index.md model column was truncated (for example "GPT-6" for runs whose share transcript says "GPT-6.1 Sol"). Not new execution and not an upgraded tier. autoTier remains unknown.
* Method: for each run, the share transcript in /tmp/h1204-r3/run was read and the text "Auto selected <model> since" extracted (either "since" or "to" phrasing); hashes computed from the same files.

| copy | scenario | share model (actual) | original index model | share sha256 |
|---|---|---|---|---|
| m1 (p4w) | F-13 | GPT-6.1 Sol | GPT-6 | d115a588231b38b877a4d225186225bbd4e58c6eeb40576d2f624777091fe49d |
| m2 (r9d) | F-10 | GPT-6.1 Sol | GPT-6 | 9429a66b42597e5db49f5fedb2766dc812fe4ea7833a6ae2390445bf6f3762ca |
| m2 (r9d) | F-P2b | GPT-6.1 Sol | GPT-6 | de75f997ab30f819732fc10ba3dfbc07fefd100da792405be508ee43ad097c7a |
| m3 (t2x) | F-09 | GPT-6.1 Sol | GPT-6 | c1f86fd36dbd50a69981564bf4c4f3bdfc87ba72641dab73688b0a369410ea89 |
| real (k7q) | F-01 | GPT-6.1 Sol | GPT-6 | 28caec3cbcaf68d28a80ac4f6c6c9bbee26fbc497c890af3c328613233874c7f |
| real (k7q) | F-02 | GPT-6.1 Sol | GPT-6 | 7e2049362b07bc35937e26a8d1f91a12bd674716e44af344361929b7f137a0f8 |
| real (k7q) | F-03 | GPT-6.1 Sol | GPT-6 | a47374234faa465ebd2795dab901c6e21b75e49754f95cca3e6a6b1413de4ab0 |
| real (k7q) | F-04 | GPT-6.1 Sol | GPT-6 | 92a8f91f251ef92861c4df7fffe3591e90f2b3d229b53d6c9d0ecb6ede1b98de |
| real (k7q) | F-05 | GPT-6.1 Sol | GPT-6 | 9f0c880e2a491f352a81083c1bb585677e2d73696d9cbd5c453af7bec9597113 |
| real (k7q) | F-06 | GPT-6.1 Sol | GPT-6 | 93baad5fc9f3cf97f1ad0465e43a56386d9ae36dd665c602b1eb2534e2a378be |
| real (k7q) | F-07 | GPT-6.1 Sol | GPT-6 | a5f690347308f53c3dd692eceff2c644ca5c8b778618c6feecf38da65c0a5ed7 |
| real (k7q) | F-08 | GPT-6.1 Sol | GPT-6 | 951d0c1a18835b0aebe917eb39265c3b3f118ab9bc5d8078aa44ecb162d98924 |
| real (k7q) | F-09 | GPT-6.1 Sol | GPT-6 | da71a77c80382452bc987d529b7dec9fd3b3863666c685358c25067c397a966f |
| real (k7q) | F-10 | GPT-6.1 Sol | GPT-6 | 83f6267f9ef1fe9fb31692f1cbfabadf8634d7f05ffb57c7a2be5a4deeb83aad |
| real (k7q) | F-11 | GPT-6.1 Sol | GPT-6 | 0f6c6681cd54e14b7cff8f765b8349b4d8e6ce65c918ca4a7804f7b3d5030b36 |
| real (k7q) | F-12 | GPT-6 Luna | GPT-6 Luna since the task has medium complexity | 077cbfacb66d08f1428b35597b287f552df627bdf228ee0f9ca517404341e82a |
| real (k7q) | F-13 | GPT-6.1 Sol | GPT-6 | 5d6890eeb63957291415e85b571ca2dfc49118b724310fcdbf99b06e5cc3cad9 |
| real (k7q) | F-14 | GPT-6 Luna | GPT-6 Luna since the task has medium complexity | 4dd16e42175bf37f27400a0b2f30f75a28f17e79ecd9a82bec64ce00becf7bda |
| real (k7q) | F-15 | GPT-6.1 Sol | GPT-6 | 441988b2d74c5138c99e9b54d3053bb89453531a3257de6beeb76c03f536346d |
| real (k7q) | F-16 | GPT-6.1 Sol | GPT-6 | e68169ce326a1763049237dd8fafb07300a626bd03b9864a6f0ed20df0351799 |
| real (k7q) | F-17 | GPT-6.1 Sol | GPT-6 | f7f62757cf6ad94c3260f958052713b36c5c42ddd4a56194cc0213b669f9adf9 |
| real (k7q) | F-P2b | GPT-6.1 Sol | GPT-6 | 6be010f9bbf8c12fd3fa73bd166ba1c2238cac11821129aed11618965dd1e942 |
