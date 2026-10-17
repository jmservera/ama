"""Execute rubric recording steps locally, without scoring or GitHub writes."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[3]
SHA = "a" * 40
NEW_SHA = "b" * 40
OTHER_SHA = "c" * 40


@pytest.fixture(params=["source", "lock"])
def steps(request):
    path = ROOT / ".github/workflows" / f"rubric-score.{'md' if request.param == 'source' else 'lock.yml'}"
    text = path.read_text(encoding="utf-8")
    if request.param == "source":
        config = yaml.safe_load(text.split("---", 2)[1])
        return config["safe-outputs"]["jobs"]["record-rubric-score"]["steps"]
    return yaml.safe_load(text)["jobs"]["record_rubric_score"]["steps"]


def step(steps, name):
    return next(item for item in steps if item.get("name") == name)


def run_js(script, *, response=None, error=None, env=None, pr=True, decision=True):
    payload = {
        "script": script,
        "response": response,
        "error": error,
        "pr": pr,
        "decision": decision,
    }
    harness = r"""
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const result = {outputs: {}, calls: [], notices: []};
const context = {
  repo: {owner: 'test', repo: 'test'}, payload: input.pr ? {pull_request: {number: 206}} : {},
  serverUrl: 'https://example.test', runId: 1, ref: process.env.TEST_REF || 'refs/heads/main',
};
const core = {
  setOutput: (key, value) => {result.outputs[key] = value;},
  notice: message => result.notices.push(message),
  warning: message => result.notices.push(message),
};
const endpoint = name => async args => {result.calls.push({name, args}); return {data: {}};};
const github = {rest: {
  pulls: {
    get: async args => {
      result.calls.push({name: 'get', args});
      if (input.error) throw new Error(input.error);
      return {data: input.response};
    },
    createReview: endpoint('review'),
  },
  repos: {createCommitStatus: endpoint('status')},
  issues: {createComment: endpoint('comment'), updateComment: endpoint('comment'),
    listComments: endpoint('listComments'), create: endpoint('issue')},
}, paginate: async () => []};
const fakeFs = {
  existsSync: () => input.decision,
  readFileSync: path => path.endsWith('decision.json') ?
    JSON.stringify({valid: true, passed: true, total: 66, baseline_total: 66}) : 'report',
};
const customRequire = name => name === 'fs' ? fakeFs : require(name);
(async () => {
  try {
    await new (Object.getPrototypeOf(async function(){}).constructor)(
      'github', 'context', 'core', 'require', input.script
    )(github, context, core, customRequire);
  } catch (error) {result.error = error.message;}
  console.log(JSON.stringify(result));
})();
"""
    environment = {
        **os.environ, "SCORED_SHA": SHA, "NEW_SHA": "", "PR_NUMBER": "206" if pr else "",
        "MOVED": "", "PUSH_FAILED": "", "RECORD_OUTCOME": "success",
        "VERIFY_OUTCOME": "success", "GATE_OUTCOME": "success",
        "RECORD_HEAD_STATE": "eligible", "RECORD_HEAD_OUTCOME": "success",
        **(env or {}),
    }
    result = subprocess.run(
        ["node", "-e", harness], input=json.dumps(payload), text=True,
        capture_output=True, env=environment, check=True,
    )
    return json.loads(result.stdout)


def script(steps, name):
    return step(steps, name)["with"]["script"]


@pytest.mark.parametrize("name", [
    "Check pull request lifecycle", "Recheck pull request before recording",
])
@pytest.mark.parametrize(("response", "state"), [
    ({"state": "closed", "head": None}, "obsolete"),
    ({"state": "open", "head": {"sha": SHA}}, "eligible"),
    ({"state": "open", "head": {"sha": OTHER_SHA}}, "moved"),
])
def test_lifecycle_classifies_explicit_state(steps, name, response, state):
    result = run_js(script(steps, name), response=response)
    assert "error" not in result
    assert result["outputs"] == {"state": state}
    assert [call["name"] for call in result["calls"]] == ["get"]
    assert bool(result["notices"]) == (state == "obsolete")


@pytest.mark.parametrize("name", [
    "Check pull request lifecycle", "Recheck pull request before recording", "Publish verdict",
])
@pytest.mark.parametrize("response", [
    None, {}, {"state": "unknown"}, {"state": "open"}, {"state": "open", "head": None},
    {"state": "open", "head": {}}, {"state": "open", "head": {"sha": "short"}},
    {"state": "open", "head": {"sha": [SHA]}},
])
def test_malformed_api_success_fails_closed(steps, name, response):
    result = run_js(script(steps, name), response=response)
    assert result["error"] == "Could not verify the current pull request head"
    assert result["outputs"] == {}
    assert [call["name"] for call in result["calls"]] == ["get"]


@pytest.mark.parametrize("name", [
    "Check pull request lifecycle", "Recheck pull request before recording", "Publish verdict",
])
@pytest.mark.parametrize("error", ["404 Not Found", "403 Forbidden", "500 API unavailable"])
def test_api_failure_is_not_obsolete_or_success(steps, name, error):
    result = run_js(script(steps, name), error=error)
    assert result["error"] == error
    assert result["outputs"] == {}
    assert result["notices"] == []
    assert [call["name"] for call in result["calls"]] == ["get"]


def test_non_pr_preflight_needs_no_api(steps):
    result = run_js(script(steps, "Check pull request lifecycle"), pr=False)
    assert result["outputs"] == {"state": "eligible"}
    assert result["calls"] == []


@pytest.mark.parametrize(("env", "head", "passed"), [
    ({}, SHA, True),
    ({"NEW_SHA": NEW_SHA}, NEW_SHA, True),
    ({"NEW_SHA": NEW_SHA}, SHA, False),
    ({"NEW_SHA": NEW_SHA}, OTHER_SHA, False),
    ({}, OTHER_SHA, False),
    ({"MOVED": "true"}, SHA, False),
    ({"RECORD_HEAD_STATE": "moved", "RECORD_OUTCOME": "skipped"}, SHA, False),
    ({"RECORD_HEAD_STATE": "", "RECORD_HEAD_OUTCOME": "failure", "RECORD_OUTCOME": "skipped"}, SHA, False),
    ({"RECORD_HEAD_STATE": "", "RECORD_HEAD_OUTCOME": "success", "RECORD_OUTCOME": "skipped"}, SHA, False),
    ({"RECORD_HEAD_OUTCOME": "skipped", "RECORD_OUTCOME": "skipped"}, SHA, False),
    ({"RECORD_OUTCOME": "failure"}, SHA, False),
    ({"RECORD_OUTCOME": "skipped"}, SHA, False),
    ({"PUSH_FAILED": "true"}, SHA, False),
    ({"VERIFY_OUTCOME": "failure"}, SHA, False),
    ({"GATE_OUTCOME": "failure"}, SHA, False),
])
def test_publication_requires_valid_checks_and_exact_resulting_head(steps, env, head, passed):
    result = run_js(script(steps, "Publish verdict"), response={"state": "open", "head": {"sha": head}}, env=env)
    assert "error" not in result
    statuses = [call["args"] for call in result["calls"] if call["name"] == "status"]
    assert [status["sha"] for status in statuses] == [SHA] + ([env["NEW_SHA"]] if env.get("NEW_SHA") else [])
    assert all(status["state"] == ("success" if passed else "failure") for status in statuses)
    reviews = [call["args"] for call in result["calls"] if call["name"] == "review"]
    assert reviews[0]["event"] == ("APPROVE" if passed else "REQUEST_CHANGES")
    assert reviews[0]["commit_id"] == env.get("NEW_SHA", SHA)


@pytest.mark.parametrize("env", [{}, {"NEW_SHA": NEW_SHA}, {"RECORD_HEAD_STATE": "obsolete"}])
def test_closed_at_publication_has_no_verdict_side_effects(steps, env):
    result = run_js(script(steps, "Publish verdict"), response={"state": "closed"}, env=env)
    assert "error" not in result
    assert result["notices"]
    assert all(call["name"] == "get" for call in result["calls"])


def test_non_pr_publication_preserves_no_write_behavior(steps):
    result = run_js(script(steps, "Publish verdict"), pr=False)
    assert result["calls"] == []


def test_missing_gate_decision_cannot_pass(steps):
    result = run_js(script(steps, "Publish verdict"), response={"state": "open", "head": {"sha": SHA}}, decision=False)
    statuses = [call["args"] for call in result["calls"] if call["name"] == "status"]
    assert statuses and all(status["state"] == "failure" for status in statuses)
    assert all(call["args"]["event"] != "APPROVE" for call in result["calls"] if call["name"] == "review")


def test_conditions_wire_obsolete_and_error_outcomes(steps):
    checkout = next(item for item in steps if item.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"]["ref"] == "${{ github.event.pull_request.head.sha || github.sha }}"
    for name in ["Load trusted rubric tools", "Verify scored commit", "Run deterministic gate"]:
        assert step(steps, name)["if"] == "steps.lifecycle.outputs.state != 'obsolete'"
    assert checkout["if"] == "steps.lifecycle.outputs.state != 'obsolete'"
    record = step(steps, "Record score on the pull request branch")
    assert "steps.record_head.outputs.state == 'eligible'" in record["if"]
    assert "steps.verify.outputs.moved != 'true'" in record["if"]
    publish = step(steps, "Publish verdict")
    assert "steps.lifecycle.outcome == 'success'" in publish["if"]
    assert "steps.lifecycle.outputs.state != 'obsolete'" in publish["if"]
    assert "always()" not in record["if"]  # Implicit success() must retain earlier failures.


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, check=True, text=True, capture_output=True).stdout.strip()


def recording_repo(tmp_path):
    root, remote = tmp_path / "work", tmp_path / "remote.git"
    root.mkdir()
    git(root, "init", "-b", "main")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "test")
    scores = root / ".github/rubric/scores"
    scores.mkdir(parents=True)
    (scores / "latest.json").write_text('{"total": 60}\n')
    git(root, "add", ".")
    git(root, "commit", "-m", "base")
    base = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "-b", "topic")
    (root / "evidence.txt").write_text("scored evidence\n")
    git(root, "add", ".")
    git(root, "commit", "-m", "scored")
    scored = git(root, "rev-parse", "HEAD")
    git(root, "init", "--bare", str(remote))
    git(root, "-c", "core.hooksPath=/dev/null", "push", str(remote), "main", "topic")
    git(root, "config", f"url.{remote}.insteadOf", "https://x-access-token:dummy@example.test/test/repo.git")
    out = tmp_path / "out"
    out.mkdir()
    (out / "latest.json").write_text('{"total": 66}\n')
    return root, remote, out, base, scored


@pytest.mark.parametrize("timing", ["before", "after"])
@pytest.mark.parametrize("movement", ["unchanged", "deleted", "backward", "forward"])
def test_real_record_push_never_recreates_or_overwrites_moved_head(steps, tmp_path, timing, movement):
    root, remote, out, base, scored = recording_repo(tmp_path)
    forward = git(root, "commit-tree", f"{scored}^{{tree}}", "-p", scored, "-m", "concurrent")
    git(root, "--git-dir", str(remote), "fetch", str(root), forward)
    destination = {"unchanged": scored, "deleted": "", "backward": base, "forward": forward}[movement]
    update = ["update-ref", "refs/heads/topic", destination, scored] if destination else ["update-ref", "-d", "refs/heads/topic", scored]
    record = step(steps, "Record score on the pull request branch")["run"].replace("/tmp/rubric-out", str(out))
    if timing == "before":
        git(root, "--git-dir", str(remote), *update)
    elif movement != "unchanged":
        command = 'git --git-dir="$TEST_REMOTE" ' + " ".join(update)
        record = record.replace('chmod 700 "$HOOK_DIR/pre-push"', f'cat >> "$HOOK_DIR/pre-push" <<\'RACE\'\n{command}\nRACE\nchmod 700 "$HOOK_DIR/pre-push"')
    output = tmp_path / "outputs"
    env = {
        **os.environ, "HEAD_REF": "topic", "SCORED_SHA": scored,
        "PUSH_TOKEN": "dummy", "GITHUB_SERVER_URL": "https://example.test",
        "GITHUB_REPOSITORY": "test/repo", "RUNNER_TEMP": str(tmp_path),
        "GITHUB_OUTPUT": str(output), "TEST_REMOTE": str(remote),
    }
    result = subprocess.run(["bash", "-e", "-c", record], cwd=root, env=env, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    outputs = output.read_text()
    assert git(root, "--git-dir", str(remote), "rev-parse", "refs/heads/main") == base
    if movement == "unchanged":
        new = git(root, "rev-parse", "HEAD")
        assert outputs == f"new_sha={new}\n"
        assert git(root, "--git-dir", str(remote), "rev-parse", "refs/heads/topic") == new
        assert git(root, "rev-parse", "HEAD^") == scored
    else:
        assert outputs == "push_failed=true\n"
        if destination:
            assert git(root, "--git-dir", str(remote), "rev-parse", "refs/heads/topic") == destination
        else:
            assert subprocess.run(["git", "--git-dir", str(remote), "show-ref", "--verify", "refs/heads/topic"], capture_output=True).returncode != 0


@pytest.mark.parametrize("has_decision", [False, True])
def test_successful_no_commit_record_keeps_scored_head(steps, tmp_path, has_decision):
    root, remote, out, _, scored = recording_repo(tmp_path)
    latest = out / "latest.json"
    if has_decision:
        latest.write_text((root / ".github/rubric/scores/latest.json").read_text())
    else:
        latest.unlink()
    output = tmp_path / "outputs"
    record = step(steps, "Record score on the pull request branch")["run"].replace("/tmp/rubric-out", str(out))
    result = subprocess.run(
        ["bash", "-e", "-c", record], cwd=root, text=True, capture_output=True,
        env={**os.environ, "GITHUB_OUTPUT": str(output)},
    )
    assert result.returncode == 0, result.stderr
    assert not output.exists()
    assert git(root, "--git-dir", str(remote), "rev-parse", "refs/heads/topic") == scored


@pytest.mark.parametrize(("state", "wrong_checkout", "moved"), [
    ("eligible", False, False), ("moved", False, True), ("eligible", True, True),
])
def test_verification_retains_initial_moved_signal_and_exact_checkout(steps, tmp_path, state, wrong_checkout, moved):
    root, _, _, base, scored = recording_repo(tmp_path)
    if wrong_checkout:
        git(root, "checkout", "--detach", base)
    output = tmp_path / "outputs"
    result = subprocess.run(
        ["bash", "-e", "-c", step(steps, "Verify scored commit")["run"]],
        cwd=root, text=True, capture_output=True,
        env={**os.environ, "EXPECTED_SHA": scored, "HEAD_STATE": state, "GITHUB_OUTPUT": str(output)},
    )
    assert result.returncode == 0, result.stderr
    assert output.exists() == moved
    if moved:
        assert output.read_text() == "moved=true\n"
    assert git(root, "rev-parse", "HEAD") == scored


@pytest.mark.parametrize("line", [
    "", f"HEAD {NEW_SHA} refs/heads/topic {'0' * 40}\n",
    f"HEAD {NEW_SHA} refs/heads/other {SHA}\n",
    f"HEAD {OTHER_SHA} refs/heads/topic {SHA}\n",
    f"HEAD {NEW_SHA} refs/heads/topic {SHA}\nextra\n",
])
def test_isolated_hook_rejects_missing_or_unexpected_updates(steps, tmp_path, line):
    body = step(steps, "Record score on the pull request branch")["run"].split("<<'HOOK'\n", 1)[1].split("\nHOOK", 1)[0]
    result = subprocess.run(
        ["sh", "-c", body], input=line, text=True, capture_output=True,
        env={**os.environ, "RECORD_SHA": NEW_SHA, "SCORED_SHA": SHA, "HEAD_REF": "topic"},
    )
    assert result.returncode != 0
    assert "::error::" in result.stderr


def test_canonical_and_generated_recording_code_match():
    directory = ROOT / ".github/workflows"
    source = yaml.safe_load((directory / "rubric-score.md").read_text().split("---", 2)[1])
    lock = yaml.safe_load((directory / "rubric-score.lock.yml").read_text())
    canonical = source["safe-outputs"]["jobs"]["record-rubric-score"]
    generated = lock["jobs"]["record_rubric_score"]
    assert canonical["permissions"] == generated["permissions"]
    for item in canonical["steps"]:
        target = step(generated["steps"], item["name"]) if "name" in item else next(
            candidate for candidate in generated["steps"] if candidate.get("uses", "").startswith("actions/checkout@")
        )
        for field in ("id", "if", "run", "with"):
            if field in item:
                assert target[field] == item[field]
        for key, value in item.get("env", {}).items():
            assert target["env"][key] == value
