"""Execute rubric publication and baseline refresh steps locally, without scoring or GitHub writes."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
SHA = "a" * 40
OTHER_SHA = "c" * 40
BRANCH = "rubric/baseline-refresh"


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


def run_js(script, *, response=None, error=None, env=None, pr=True, decision=True, score_passed=True, gate_decision=None):
    payload = {
        "script": script,
        "response": response,
        "error": error,
        "pr": pr,
        "decision": decision,
        "score_passed": score_passed,
        "gate_decision": gate_decision,
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
  info: message => result.notices.push(message),
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
    JSON.stringify(input.gate_decision || {valid: true, passed: input.score_passed, total: input.score_passed ? 66 : 65, baseline_total: 66}) : 'report',
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
        **os.environ, "SCORED_SHA": SHA, "PR_NUMBER": "206" if pr else "",
        "MOVED": "", "VERIFY_OUTCOME": "success", "GATE_OUTCOME": "success",
        "HEAD_STATE": "eligible", "HEAD_OUTCOME": "success",
        **(env or {}),
    }
    result = subprocess.run(
        ["node", "-e", harness], input=json.dumps(payload), text=True,
        capture_output=True, env=environment, check=True,
    )
    return json.loads(result.stdout)


def script(steps, name):
    return step(steps, name)["with"]["script"]


def statuses(result):
    return [call["args"] for call in result["calls"] if call["name"] == "status"]


def reviews(result):
    return [call["args"] for call in result["calls"] if call["name"] == "review"]


@pytest.mark.parametrize("name", [
    "Check pull request lifecycle", "Recheck pull request before publishing",
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
    "Check pull request lifecycle", "Recheck pull request before publishing", "Publish verdict",
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
    "Check pull request lifecycle", "Recheck pull request before publishing", "Publish verdict",
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
    ({}, OTHER_SHA, False),
    ({"MOVED": "true"}, SHA, False),
    ({"HEAD_STATE": "moved"}, SHA, False),
    ({"HEAD_STATE": "", "HEAD_OUTCOME": "failure"}, SHA, False),
    ({"HEAD_STATE": "", "HEAD_OUTCOME": "success"}, SHA, False),
    ({"HEAD_OUTCOME": "skipped"}, SHA, False),
    ({"VERIFY_OUTCOME": "failure"}, SHA, False),
    ({"GATE_OUTCOME": "failure"}, SHA, False),
])
def test_publication_requires_valid_checks_and_unmoved_head(steps, env, head, passed):
    result = run_js(script(steps, "Publish verdict"), response={"state": "open", "head": {"sha": head}}, env=env)
    assert "error" not in result
    assert [status["sha"] for status in statuses(result)] == [SHA]
    assert statuses(result)[0]["context"] == "rubric/score"
    assert statuses(result)[0]["state"] == ("success" if passed else "failure")
    assert reviews(result)[0]["event"] == ("APPROVE" if passed else "REQUEST_CHANGES")
    assert reviews(result)[0]["commit_id"] == SHA
    assert len([call for call in result["calls"] if call["name"] == "get"]) == 1


def test_publication_posts_comment_status_and_review_without_branch_writes(steps):
    result = run_js(script(steps, "Publish verdict"), response={"state": "open", "head": {"sha": SHA}})
    assert sorted(call["name"] for call in result["calls"]) == ["comment", "get", "review", "status"]
    assert "66/100 vs baseline 66/100" in reviews(result)[0]["body"]


def test_regression_is_a_failing_status_and_change_request(steps):
    result = run_js(
        script(steps, "Publish verdict"), response={"state": "open", "head": {"sha": SHA}}, score_passed=False,
    )
    assert statuses(result)[0]["state"] == "failure"
    assert reviews(result)[0]["event"] == "REQUEST_CHANGES"
    assert "65/100 vs baseline 66/100" in reviews(result)[0]["body"]


@pytest.mark.parametrize("score", [2, 3])
def test_real_deterministic_comparison_drives_publication(steps, score):
    rubric = json.loads((ROOT / ".github/rubric/rubric.json").read_text())
    ids = [criterion["id"] for criterion in rubric["criteria"]]
    evidence = "docs/brds/agentic-retrofit-programme-brd.md"
    baseline = {"total": 60, "criteria": {
        cid: {"score": 3, "evidence": [], "rationale": "baseline"} for cid in ids
    }}
    proposed = {cid: {
        "score": score if cid == "A1" else 3,
        "evidence": [f"{evidence}:1"], "rationale": "fixture", "change_reason": "changed evidence",
    } for cid in ids}
    decision = gate.evaluate(
        rubric, baseline, False, ids, [evidence],
        [{"type": gate.TOOL_TYPE, "scorecard": {"criteria": proposed}}],
        "success", "success",
    )
    assert decision["valid"] and decision["passed"] == (score == 3)
    result = run_js(
        script(steps, "Publish verdict"),
        response={"state": "open", "head": {"sha": SHA}}, gate_decision=decision,
    )
    assert statuses(result)[0]["state"] == ("success" if score == 3 else "failure")


@pytest.mark.parametrize("env", [{}, {"HEAD_STATE": "obsolete"}])
def test_closed_at_publication_has_no_verdict_side_effects(steps, env):
    result = run_js(script(steps, "Publish verdict"), response={"state": "closed"}, env=env)
    assert "error" not in result
    assert result["notices"]
    assert all(call["name"] == "get" for call in result["calls"])


def test_non_pr_publication_preserves_no_write_behavior(steps):
    result = run_js(script(steps, "Publish verdict"), pr=False)
    assert result["calls"] == []


def test_non_pr_regression_opens_an_issue_without_review(steps):
    result = run_js(script(steps, "Publish verdict"), pr=False, score_passed=False)
    assert [call["name"] for call in result["calls"]] == ["issue"]


def test_missing_gate_decision_cannot_pass(steps):
    result = run_js(script(steps, "Publish verdict"), response={"state": "open", "head": {"sha": SHA}}, decision=False)
    assert statuses(result) and all(status["state"] == "failure" for status in statuses(result))
    assert all(review["event"] != "APPROVE" for review in reviews(result))


def test_conditions_wire_obsolete_and_error_outcomes(steps):
    checkout = next(item for item in steps if item.get("uses", "").startswith("actions/checkout@"))
    assert checkout["with"]["ref"] == "${{ github.event.pull_request.head.sha || github.sha }}"
    for name in ["Load trusted rubric tools", "Verify scored commit", "Run deterministic gate"]:
        assert step(steps, name)["if"] == "steps.lifecycle.outputs.state != 'obsolete'"
    assert checkout["if"] == "steps.lifecycle.outputs.state != 'obsolete'"
    publish = step(steps, "Publish verdict")
    assert "steps.lifecycle.outcome == 'success'" in publish["if"]
    assert "steps.lifecycle.outputs.state != 'obsolete'" in publish["if"]


def test_no_step_writes_scores_to_a_pull_request_branch(steps):
    names = [item.get("name") for item in steps]
    assert "Record score on the pull request branch" not in names
    assert "Recheck pull request before recording" not in names
    pushes = [item for item in steps if "git push" in item.get("run", "") or " push " in item.get("run", "")]
    assert [item["name"] for item in pushes] == ["Refresh baseline on main"]
    text = json.dumps(steps)
    assert "HEAD_REF" not in text and "github.head_ref" not in text
    assert "refs/heads/main" not in pushes[0]["run"].replace("github.ref == 'refs/heads/main'", "")
    assert "HEAD:refs/heads/${REFRESH_BRANCH}" in pushes[0]["run"]


def test_refresh_runs_only_for_main_pushes_and_unforced_dispatch_after_the_gate(steps):
    condition = step(steps, "Refresh baseline on main")["if"]
    assert "github.event_name == 'push'" in condition
    assert "github.event_name == 'workflow_dispatch' && github.event.inputs.force != 'true'" in condition
    assert "github.ref == 'refs/heads/main'" in condition
    assert "steps.gate.outcome == 'success'" in condition
    assert "pull_request" not in condition


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
    git(root, "config", "url." + str(remote) + ".insteadOf", "https://x-access-token:dummy@example.test/test/repo.git")
    out = tmp_path / "out"
    out.mkdir()
    (out / "latest.json").write_text('{"total": 66}\n')
    (out / "badge.svg").write_text("<svg/>\n")
    (out / "decision.json").write_text(json.dumps({"valid": True, "passed": True, "calibration": False}))
    return root, remote, out, base, scored


FAKE_GH = """#!/bin/bash
echo "$*" >> "$GH_LOG"
case "$1 $2" in
  "pr list")
    if [ -n "${GH_EXISTING_PR:-}" ] || [ -f "$GH_STATE/created" ]; then echo 7; fi ;;
  "pr create") touch "$GH_STATE/created" ;;
  "pr view")
    if [ -n "${GH_MAIN_AFTER_PUBLISH:-}" ]; then echo "$GH_MAIN_AFTER_PUBLISH" > "$GH_STATE/main_commit"; fi
    if [ -n "${GH_HEAD_MOVED:-}" ]; then printf 'd%.0s' $(seq 1 40); echo
    else git --git-dir "$GH_REMOTE" rev-parse refs/heads/rubric/baseline-refresh; fi ;;
  "pr merge") if [ -n "${GH_MERGE_FAIL:-}" ]; then exit 1; fi ;;
  "api repos/"*)
    case "$2" in
      */compare/*)
        range="${2##*/compare/}"; from="${range%%...*}"; to="${range##*...}"
        if [ "$from" = "$to" ]; then echo identical
        elif git --git-dir "$GH_REMOTE" merge-base --is-ancestor "$from" "$to"; then echo ahead
        elif git --git-dir "$GH_REMOTE" merge-base --is-ancestor "$to" "$from"; then echo behind
        else echo diverged; fi ;;
      */contents/*)
        main_commit="${GH_MAIN_COMMIT:-}"
        if [ -f "$GH_STATE/main_commit" ]; then main_commit="$(cat "$GH_STATE/main_commit")"; fi
        printf '{"commit": "%s"}' "$main_commit" | base64 -w0 ;;
      */commits/*)
        git --git-dir "$GH_REMOTE" log -1 --format=%B "${2##*/commits/}"
        if [ -n "${GH_BRANCH_ADVANCE:-}" ]; then
          git --git-dir "$GH_REMOTE" update-ref refs/heads/rubric/baseline-refresh "$GH_BRANCH_ADVANCE"
        fi ;;
    esac ;;
esac
"""


def run_refresh(steps, tmp_path, root, remote, out, scored, **extra):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    for name, body in {"gh": FAKE_GH, "sleep": "#!/bin/sh\nexit 0\n"}.items():
        (bin_dir / name).write_text(body)
        (bin_dir / name).chmod(stat.S_IRWXU)
    state = tmp_path / "state"
    state.mkdir(exist_ok=True)
    log = tmp_path / "gh.log"
    log.touch()
    record = step(steps, "Refresh baseline on main")["run"].replace("/tmp/rubric-out", str(out))
    env = {
        **os.environ, "PATH": f"{bin_dir}:{os.environ['PATH']}", "GH_TOKEN": "dummy", "SCORED_SHA": scored,
        "REFRESH_BRANCH": BRANCH, "GITHUB_SERVER_URL": "https://example.test",
        "GITHUB_REPOSITORY": "test/repo", "GH_LOG": str(log), "GH_STATE": str(state),
        "GH_REMOTE": str(remote),
    }
    env.update({key: value for key, value in extra.items() if value is not None})
    result = subprocess.run(["bash", "-e", "-c", record], cwd=root, env=env, text=True, capture_output=True)
    return result, log.read_text().splitlines()


def remote_ref(remote, ref):
    result = subprocess.run(["git", "--git-dir", str(remote), "rev-parse", "--verify", ref], capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else None


def test_refresh_pushes_a_bot_branch_and_opens_then_merges_a_pull_request(steps, tmp_path):
    root, remote, out, base, scored = recording_repo(tmp_path)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored)
    assert result.returncode == 0, result.stderr
    refreshed = remote_ref(remote, f"refs/heads/{BRANCH}")
    assert refreshed and refreshed != scored
    assert git(root, "--git-dir", str(remote), "rev-parse", f"{refreshed}^") == scored
    changed = git(root, "--git-dir", str(remote), "diff", "--name-only", scored, refreshed).splitlines()
    assert sorted(changed) == [".github/rubric/scores/badge.svg", ".github/rubric/scores/latest.json"]
    assert remote_ref(remote, "refs/heads/main") == base
    assert remote_ref(remote, "refs/heads/topic") == scored
    assert git(root, "--git-dir", str(remote), "log", "-1", "--format=%s", refreshed) == "chore(rubric): record score 66/100"
    assert any(call.startswith("pr create ") and "--base main" in call and f"--head {BRANCH}" in call for call in calls)
    merge = [call for call in calls if call.startswith("pr merge ")]
    assert len(merge) == 1 and f"--match-head-commit {refreshed}" in merge[0] and "--squash" in merge[0]


def test_refresh_updates_an_existing_pull_request_and_replaces_a_stale_branch(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    stale = git(root, "commit-tree", f"{scored}^{{tree}}", "-p", scored, "-m", "stale refresh")
    git(root, "-c", "core.hooksPath=/dev/null", "push", str(remote), f"{stale}:refs/heads/{BRANCH}")
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_EXISTING_PR="1")
    assert result.returncode == 0, result.stderr
    refreshed = remote_ref(remote, f"refs/heads/{BRANCH}")
    assert refreshed not in (None, stale)
    assert git(root, "--git-dir", str(remote), "rev-parse", f"{refreshed}^") == scored
    assert any(call.startswith("pr edit 7 ") for call in calls)
    assert not any(call.startswith("pr create ") for call in calls)


@pytest.mark.parametrize("decision", [
    {"valid": True, "passed": False, "calibration": False},
    {"valid": False, "passed": False},
    {"valid": True, "passed": True, "calibration": True},
    None,
])
def test_refresh_never_records_a_failed_or_calibration_score(steps, tmp_path, decision):
    root, remote, out, _, scored = recording_repo(tmp_path)
    if decision is None:
        (out / "decision.json").unlink()
    else:
        (out / "decision.json").write_text(json.dumps(decision))
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored)
    assert result.returncode == 0, result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") is None
    assert calls == []


def test_refresh_without_a_scorecard_changes_nothing(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    (out / "latest.json").unlink()
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored)
    assert result.returncode == 0, result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") is None and calls == []


def test_refresh_skips_when_the_baseline_already_matches(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    (out / "latest.json").write_text((root / ".github/rubric/scores/latest.json").read_text())
    (out / "badge.svg").unlink()
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored)
    assert result.returncode == 0, result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") is None and calls == []


def test_refresh_refuses_a_checkout_that_is_not_the_scored_commit(steps, tmp_path):
    root, remote, out, base, scored = recording_repo(tmp_path)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, base)
    assert result.returncode != 0
    assert "not the scored commit" in result.stdout + result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") is None and calls == []


def test_refresh_does_not_merge_a_head_that_another_run_replaced(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_HEAD_MOVED="1")
    assert result.returncode == 0, result.stderr
    assert not any(call.startswith("pr merge ") for call in calls)
    assert "newer run owns" in result.stdout


def test_refresh_leaves_the_pull_request_open_when_merge_is_blocked(steps, tmp_path):
    root, remote, out, base, scored = recording_repo(tmp_path)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_MERGE_FAIL="1")
    assert result.returncode == 0, result.stderr
    assert len([call for call in calls if call.startswith("pr merge ")]) == 5
    assert "::warning::" in result.stdout and "could not be merged" in result.stdout
    assert remote_ref(remote, f"refs/heads/{BRANCH}")
    assert remote_ref(remote, "refs/heads/main") == base


def test_refresh_server_push_rejection_fails_the_step(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    hook = remote / "hooks/pre-receive"
    hook.write_text("#!/bin/sh\nexit 1\n")
    hook.chmod(0o700)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored)
    assert result.returncode != 0
    assert not any(call.startswith(("pr create", "pr merge")) for call in calls)


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


def newer_commit(root, remote, parent, message="newer main"):
    commit = git(root, "commit-tree", f"{parent}^{{tree}}", "-p", parent, "-m", message)
    git(root, "-c", "core.hooksPath=/dev/null", "push", str(remote), f"{commit}:refs/heads/newer-{commit[:8]}")
    return commit


def test_refresh_replaces_an_older_baseline_on_main(steps, tmp_path):
    root, remote, out, base, scored = recording_repo(tmp_path)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_MAIN_COMMIT=base)
    assert result.returncode == 0, result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") not in (None, scored)
    assert any(call.startswith("pr merge ") for call in calls)


def test_older_dispatch_cannot_replace_a_newer_baseline_on_main(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    newer = newer_commit(root, remote, scored)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_MAIN_COMMIT=newer)
    assert result.returncode == 0, result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") is None
    assert not any(call.startswith(("pr create ", "pr edit ", "pr merge ")) for call in calls)


def test_older_dispatch_cannot_replace_a_newer_pending_refresh(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    newer = newer_commit(root, remote, scored)
    pending = git(root, "commit-tree", f"{scored}^{{tree}}", "-p", scored, "-m", "pending", "-m", f"Scored commit: {newer}")
    git(root, "-c", "core.hooksPath=/dev/null", "push", str(remote), f"{pending}:refs/heads/{BRANCH}")
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_EXISTING_PR="1")
    assert result.returncode == 0, result.stderr
    assert remote_ref(remote, f"refs/heads/{BRANCH}") == pending
    assert not any(call.startswith(("pr create ", "pr edit ", "pr merge ")) for call in calls)


def test_newer_pending_refresh_pushed_after_the_check_is_not_overwritten(steps, tmp_path):
    root, remote, out, _, scored = recording_repo(tmp_path)
    old_pending = git(root, "commit-tree", f"{scored}^{{tree}}", "-p", scored, "-m", "pending", "-m", f"Scored commit: {scored}")
    git(root, "-c", "core.hooksPath=/dev/null", "push", str(remote), f"{old_pending}:refs/heads/{BRANCH}")
    newer = newer_commit(root, remote, scored)
    raced = git(root, "commit-tree", f"{newer}^{{tree}}", "-p", newer, "-m", "pending", "-m", f"Scored commit: {newer}")
    git(root, "-c", "core.hooksPath=/dev/null", "push", str(remote), f"{raced}:refs/heads/raced")
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_EXISTING_PR="1", GH_BRANCH_ADVANCE=raced)
    assert result.returncode != 0
    assert remote_ref(remote, f"refs/heads/{BRANCH}") == raced
    assert not any(call.startswith("pr merge ") for call in calls)


def test_refresh_does_not_merge_when_a_newer_baseline_lands_before_the_merge(steps, tmp_path):
    root, remote, out, base, scored = recording_repo(tmp_path)
    newer = newer_commit(root, remote, scored)
    result, calls = run_refresh(steps, tmp_path, root, remote, out, scored, GH_MAIN_COMMIT=base, GH_MAIN_AFTER_PUBLISH=newer)
    assert result.returncode == 0, result.stderr
    assert not any(call.startswith("pr merge ") for call in calls)
