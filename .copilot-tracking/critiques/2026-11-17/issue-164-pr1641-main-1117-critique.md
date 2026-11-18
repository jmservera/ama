# Critique (one pass)
* Risk: rerere replays prior resolutions silently. Mitigation: compared every conflicted file with the prior reviewed tree and main; differences explained above.
* Risk: reintroducing safeguarding owner exposure in staff case detail (main redacts). Decision: reapply 69367b4f1 (compatible with settled review); do not reopen.
* Out of scope: consent-regrant defects, unrelated failures. Compatible; applied directly.
