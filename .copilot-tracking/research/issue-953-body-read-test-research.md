# Research: issue 953 slice 2

* Merged PR 924 (backend ConnectionError answers 500 and ERROR) and PR 990 (request-read disconnect logs WARNING) delivered the code. Research disposition: reused.
* Gap named in PR 990: the POST body-read branch (`_body_read_failed` in `server.py` `_body`) had no dedicated test.
* Planning Readiness: Ready. Test-only slice; no security, infrastructure, SQL or deployment change.
* Related #921 was not assessed by either PR and is not assessed here.
