# Details

_SECRET = re.compile(r"(?<![A-Za-z0-9])sk-|^(?:gh[pousr]_|github_pat_|AKIA[0-9A-Z]{12,}|eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,})|[0-9a-fA-F]{32,}|[A-Za-z0-9_]{32,}") with IGNORECASE only on sk- (inline `(?i:sk-)`).
Oversize: `len(value) > limit` for str -> UNVERIFIED_IDENTITY; non-str -> None.
The previous 'abcsk-...' secret case is no longer a secret shape (F4 requires boundary); removed from SECRETS.
Existing callers: ai.py passes 120 for deployment; becomes 80 constant via IDENTITY_CHARS.
