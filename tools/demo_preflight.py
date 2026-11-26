"""Read-only demo preflight (issue 2206).

Checks container app revisions, job executions, /healthz and the cohort and consent counts, then
prints a Markdown table that doubles as the runbook preflight record. Only read-only az commands
and GET /healthz are used. Output carries names, states and counts, never tokens, connection
strings or environment values. Counts need a path to the private SQL server; when it is not
reachable they are reported as unavailable instead of failing silently.

Usage: python3 tools/demo_preflight.py [--resource-group ama] [--strict]
Exit code: 1 when any check fails; with --strict, also when a check is unavailable.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import subprocess
import sys
import urllib.request
from collections import Counter
from collections.abc import Callable
from datetime import UTC, datetime

APPS = ["ca-cutover-test-demo-api", "ca-resident-demo"]
JOBS = [
    "job-cutover-test-demo-load",
    "job-cutover-test-demo-audit",
    "job-cutover-test-demo-orch",
    "job-live-simulator",
    "job-live-receiver",
]
AGENTS_APP = "ca-cutover-test-demo-agents"
SQL_SERVER = "sql-cutover-test-rzsrg.database.windows.net"
SQL_DATABASE = "retrofit"
BUILD_COMMIT_LINE = re.compile(r"build: commit=([0-9a-f]{7,40}|unknown)")
READ_ONLY_VERBS = {"list", "show", "get-access-token"}

Runner = Callable[[list[str]], str]
Getter = Callable[..., tuple[int, str]]
CountReader = Callable[[], list[dict[str, object]]]


class Result:
    def __init__(self, name: str, status: str, detail: str) -> None:
        self.name, self.status, self.detail = name, status, detail


def run_az(argv: list[str]) -> str:
    if not any(part in READ_ONLY_VERBS for part in argv[:5]):
        raise ValueError("NOT_READ_ONLY")
    done = subprocess.run(["az", *argv], capture_output=True, text=True, timeout=60, check=False)
    if done.returncode:
        raise RuntimeError(f"az exit {done.returncode}")
    return done.stdout


def http_get(url: str, timeout: int = 15) -> tuple[int, str]:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.status, resp.read(2048).decode("utf-8", "replace")


def _json(runner: Runner, argv: list[str]) -> object:
    return json.loads(runner(argv) or "null")


def check_revisions(runner: Runner, group: str, app: str) -> Result:
    name = f"revisions {app}"
    try:
        rows = _json(
            runner,
            ["containerapp", "revision", "list", "-g", group, "-n", app, "-o", "json"],
        )
    except Exception as exc:  # noqa: BLE001 - any failure is reported
        return Result(name, "FAIL", str(exc))
    active = [r.get("properties", {}) for r in rows or [] if r.get("properties", {}).get("active")]
    if not active:
        return Result(name, "FAIL", "no active revision")
    traffic = sum(int(p.get("trafficWeight") or 0) for p in active)
    parts = [
        f"{r.get('name')} {p.get('healthState')}/{p.get('runningState')} {p.get('trafficWeight')}%"
        for r, p in zip([x for x in rows if x.get("properties", {}).get("active")], active)
    ]
    healthy = all(p.get("healthState") == "Healthy" for p in active)
    ok = healthy and traffic == 100
    return Result(name, "PASS" if ok else "FAIL", "; ".join(parts))


def check_deployment(runner: Runner, group: str, kind: str, name: str) -> Result:
    """Report the image digest and the hardening switch; no other environment value is read."""
    label = f"deployment {name}"
    argv = ["containerapp", "job", "show"] if kind == "job" else ["containerapp", "show"]
    query = (
        "{image: properties.template.containers[0].image, hardening: "
        "properties.template.containers[0].env[?name=='ZF_CONTAINER_HARDENING'].value | [0]}"
    )
    try:
        body = _json(runner, [*argv, "-g", group, "-n", name, "--query", query, "-o", "json"])
    except Exception as exc:  # noqa: BLE001 - any failure is reported
        return Result(label, "FAIL", str(exc))
    body = body if isinstance(body, dict) else {}
    image = str(body.get("image") or "")
    digest = image.partition("@sha256:")[2][:12]
    hardening = body.get("hardening")
    detail = f"digest {digest or 'none'}; ZF_CONTAINER_HARDENING={hardening}"
    return Result(label, "PASS" if hardening == "enforced" and digest else "FAIL", detail)


def check_build_commit(runner: Runner, group: str, app: str, expected: str | None = None) -> Result:
    """Read the source commit the running image reports at start-up; keep only that token."""
    label = f"build commit {app}"
    try:
        out = runner(
            [
                "containerapp",
                "logs",
                "show",
                "-g",
                group,
                "-n",
                app,
                "--tail",
                "300",
                "--type",
                "console",
            ]
        )
    except Exception as exc:  # noqa: BLE001 - any failure is reported
        return Result(label, "UNAVAILABLE", str(exc))
    found = BUILD_COMMIT_LINE.findall(out or "")
    if not found:
        return Result(label, "UNAVAILABLE", "no start-up build line in the recent log")
    commit = found[-1]
    if commit == "unknown":
        return Result(label, "FAIL", "commit=unknown: image built without ZF_BUILD_COMMIT")
    if expected and not (
        commit.startswith(expected.lower()) or expected.lower().startswith(commit)
    ):
        return Result(label, "FAIL", f"commit {commit[:12]} is not the expected {expected[:12]}")
    return Result(label, "PASS", f"commit {commit[:12]}")


def check_job(runner: Runner, group: str, job: str) -> Result:
    name = f"job {job}"
    try:
        rows = _json(
            runner,
            ["containerapp", "job", "execution", "list", "-g", group, "-n", job, "-o", "json"],
        )
    except Exception as exc:  # noqa: BLE001 - any failure is reported
        return Result(name, "FAIL", str(exc))
    if not rows:
        return Result(name, "UNAVAILABLE", "no executions")
    latest = max(rows, key=lambda r: r.get("properties", {}).get("startTime") or "")
    props = latest.get("properties", {})
    status = props.get("status")
    verdict = "FAIL" if status in ("Failed", "Degraded") else "PASS"
    return Result(name, verdict, f"latest {status} at {props.get('startTime')}")


def check_health(runner: Runner, getter: Getter, group: str, app: str) -> Result:
    name = f"health {app}"
    try:
        fqdn = runner(
            [
                "containerapp", "show", "-g", group, "-n", app,
                "--query", "properties.configuration.ingress.fqdn", "-o", "tsv",
            ]
        ).strip()  # fmt: skip
        url = f"https://{fqdn}/healthz"
        try:
            code, _ = getter(url)
            note = ""
        except TimeoutError:
            # A replica scaled to zero needs longer than the first timeout to start.
            code, _ = getter(url, 90)
            note = " (cold start, retried)"
    except Exception as exc:  # noqa: BLE001 - any failure is reported
        return Result(name, "FAIL", type(exc).__name__)
    return Result(name, "PASS" if code == 200 else "FAIL", f"GET /healthz {code}{note}")


def check_counts(reader: CountReader | None) -> Result:
    name = "cohort and consent counts"
    if reader is None:
        return Result(name, "UNAVAILABLE", "no reader")
    try:
        bodies = reader()
    except Exception as exc:  # noqa: BLE001 - any failure is reported
        return Result(name, "UNAVAILABLE", f"SQL not reachable ({type(exc).__name__})")
    homes = {str(b.get("home_id")) for b in bodies if b.get("home_id")}
    consent = Counter(str(b.get("consent", "unknown")) for b in bodies)
    detail = f"cohort homes {len(homes)}; " + ", ".join(
        f"{k} {consent[k]}" for k in sorted(consent)
    )
    return Result(name, "PASS" if homes else "FAIL", detail if consent else "no controls")


def sql_reader(runner: Runner) -> CountReader:
    def read() -> list[dict[str, object]]:
        import pyodbc

        raw = runner(
            [
                "account", "get-access-token", "--resource", "https://database.windows.net/",
                "--query", "accessToken", "-o", "tsv",
            ]
        ).strip().encode("utf-16-le")  # fmt: skip
        token = struct.pack(f"<I{len(raw)}s", len(raw), raw)
        conn = pyodbc.connect(
            f"Driver={{ODBC Driver 18 for SQL Server}};Server={SQL_SERVER};Database={SQL_DATABASE};",
            attrs_before={1256: token},
            timeout=15,
        )
        try:
            rows = conn.execute("SELECT body FROM sensor_consumer_control").fetchall()
        finally:
            conn.close()
        return [json.loads(r[0]) for r in rows]

    return read


def collect(
    runner: Runner,
    getter: Getter,
    reader: CountReader | None,
    group: str = "ama",
    apps: list[str] | None = None,
    jobs: list[str] | None = None,
    expected_commit: str | None = None,
) -> list[Result]:
    results: list[Result] = []
    for app in apps or APPS:
        results.append(check_revisions(runner, group, app))
        results.append(check_health(runner, getter, group, app))
    results.extend(
        check_deployment(runner, group, "app", app) for app in apps or [*APPS, AGENTS_APP]
    )
    results.extend(check_deployment(runner, group, "job", job) for job in jobs or JOBS)
    results.extend(check_job(runner, group, job) for job in jobs or JOBS)
    results.append(check_build_commit(runner, group, (apps or APPS)[0], expected_commit))
    results.append(check_counts(reader))
    return results


def render(results: list[Result], now: datetime, group: str) -> str:
    lines = [
        f"Demo preflight, resource group {group}, {now.strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "| Check | Result | Detail |",
        "| --- | --- | --- |",
    ]
    lines += [f"| {r.name} | {r.status} | {r.detail.replace('|', '/')} |" for r in results]
    fails = sum(r.status == "FAIL" for r in results)
    na = sum(r.status == "UNAVAILABLE" for r in results)
    lines += ["", f"Summary: {len(results) - fails - na} pass, {fails} fail, {na} unavailable."]
    return "\n".join(lines)


def exit_code(results: list[Result], strict: bool) -> int:
    if any(r.status == "FAIL" for r in results):
        return 1
    return 1 if strict and any(r.status == "UNAVAILABLE" for r in results) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--resource-group", default="ama")
    parser.add_argument("--expect-commit", help="source commit the API image must report")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    results = collect(
        run_az,
        http_get,
        sql_reader(run_az),
        args.resource_group,
        expected_commit=args.expect_commit,
    )
    print(render(results, datetime.now(UTC), args.resource_group))
    return exit_code(results, args.strict)


if __name__ == "__main__":
    sys.exit(main())
