# Details
1. Patterns: private key block, AWS access key id, GitHub tokens, Azure storage AccountKey, SAS sig, JWT, SQL Password= in connection strings.
2. API: scan_text(path, text) -> findings; scan_repo(root) over `git ls-files`; main returns 1 on findings.
3. Tests: constructed positives per rule, allowlist exactness, clean text, live repo scan returns none.
