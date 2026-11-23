"""Measure the anonymous edge behaviour for protected API paths (Refs #350, criterion 1).

Sends anonymous GET requests only, with no credentials, and does not follow
redirects. Protected API paths must answer 401 for native and browser-style
requests; protected pages may redirect to sign-in. This measures behaviour; it
is not trusted-platform-principal proof and never justifies an API exemption.

Exit codes: 0 all pass, 1 at least one fail, 2 a request could not be made.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

API_PATHS = ("/api/me", "/api/cases", "/api/staff")
PAGE_PATHS = ("/app",)
CHROME = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36"
STYLES = {
    "native": {"User-Agent": "curl/8.5.0"},
    "browser-json": {"User-Agent": CHROME, "Accept": "application/json", "Sec-Fetch-Mode": "cors"},
    "browser-html": {"User-Agent": CHROME, "Accept": "text/html"},
}


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def classify(path: str, status: int | None) -> str:
    if status is None:
        return "blocked"
    if path in API_PATHS:
        return "pass" if status == 401 else "fail"
    return "pass" if status in (302, 401) else "fail"


def fetch(base: str, path: str, headers: dict) -> int | None:
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(urllib.request.Request(base + path, headers=headers), timeout=20) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code
    except (urllib.error.URLError, OSError):
        return None


def run(base: str, fetcher=fetch) -> dict:
    rows = []
    for path in API_PATHS + PAGE_PATHS:
        for style, headers in STYLES.items():
            status = fetcher(base, path, headers)
            rows.append({"path": path, "style": style, "status": status, "result": classify(path, status)})
    results = {row["result"] for row in rows}
    verdict = "blocked" if "blocked" in results else "fail" if "fail" in results else "pass"
    return {"verdict": verdict, "rows": rows}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("base_url", help="https origin of the deployed API, without a trailing slash")
    report = run(parser.parse_args(argv).base_url.rstrip("/"))
    print(json.dumps(report, indent=2))
    return {"pass": 0, "fail": 1, "blocked": 2}[report["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
