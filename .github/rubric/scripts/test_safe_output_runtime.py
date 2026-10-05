"""Runtime regression tests for the generated record_rubric_score safe output.

These tests run the real pinned gh-aw safe-outputs MCP runtime against the
config and tool schema extracted from the compiled rubric-score.lock.yml
(override with GH_AW_PROBE_LOCK). The tool has 20 required score choices
(A1_score..D3_score, options "1".."5") plus required details and summary
strings, kept within the compiler's 25-input limit for safe-output jobs. They
never reimplement the runtime validation. Point GH_AW_RUNTIME_DIR at the
`actions/setup/js` directory of github/gh-aw-actions at the pinned commit
(fetched outside the repository); the runtime tests skip when it is absent.
"""

from __future__ import annotations

import hashlib
import json
import os
import queue
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate  # noqa: E402

RUBRIC_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = RUBRIC_DIR.parent.parent
LOCK = Path(os.environ.get("GH_AW_PROBE_LOCK") or REPO_ROOT / ".github" / "workflows" / "rubric-score.lock.yml")
RUBRIC = json.loads((RUBRIC_DIR / "rubric.json").read_text(encoding="utf-8"))
IDS = [criterion["id"] for criterion in RUBRIC["criteria"]]
EXPECTED_IDS = [f"{group}{n}" for group, count in (("A", 7), ("B", 7), ("C", 3), ("D", 3)) for n in range(1, count + 1)]
CONFIG_KEY = "record-rubric-score"
TOOL = "record_rubric_score"
SCORE_OPTIONS = ["1", "2", "3", "4", "5"]

# gh-aw v0.89.21 (github/gh-aw c35393777e5604a63721d09512263b1383301d4f) pins
# github/gh-aw-actions 924af5fdc64061cfbf66fb584c8b07e2ac230c60. Git blob SHAs of
# the runtime files exercised here, taken from that pinned tree.
PINNED_BLOBS = {
    "mcp_server_core.cjs": "21dda2c06354d7c100350fca89f6143d6bf4e0d6",
    "safe_outputs_handlers.cjs": "ef2a42e3c1edc8c046219c47923b3d8fceb370a5",
    "safe_outputs_mcp_server.cjs": "efb24c34fec875ffcd9d997d93f043c78fe16f8b",
    "safe_outputs_mcp_server_http.cjs": "9e1f9338876b4645b0b899cfe7e0be27c7715a37",
    "safe_outputs_tools_loader.cjs": "dce6458a8f30198b9648e9968c9a04050ef5dff6",
    "generate_safe_outputs_tools.cjs": "ae09ab0a9d637035d4442f72475abcafe5e50ea4",
    "safe_outputs_config.cjs": "c5fef5e3799d56985de1057d7e99409d00bc8c82",
    "safe_outputs_append.cjs": "4a6fc13e3435173218f499342cc1cdf7dcb2348a",
    "mcp_http_transport.cjs": "556aaa1c5ace024885c40c1183ba7d4dbaa2a869",
    "safe_outputs_mcp_arguments.cjs": "cee914b8e9e009e00cfef7650deccb0feaf792ba",
}
TIMEOUT = 20


def lock_step_env(step_name: str) -> dict:
    lock = yaml.safe_load(LOCK.read_text(encoding="utf-8"))
    for step in lock["jobs"]["agent"]["steps"]:
        if step.get("name") == step_name:
            return step["env"]
    raise AssertionError(f"step {step_name!r} not found in {LOCK.name}")


def generated_config_text() -> str:
    return lock_step_env("Generate Safe Outputs Config")["GH_AW_SAFE_OUTPUTS_CONFIG"]


def generated_tools_env() -> dict:
    return lock_step_env("Generate Safe Outputs Tools")


def generated_tool_schema() -> dict:
    meta = json.loads(generated_tools_env()["GH_AW_TOOLS_META_JSON"])
    tools = [tool for tool in meta.get("dynamic_tools", []) if tool.get("name") == TOOL]
    assert len(tools) == 1, f"expected one generated {TOOL} dynamic tool"
    return tools[0]


def expected_fields() -> list[str]:
    return [f"{cid}_score" for cid in EXPECTED_IDS] + ["details", "summary"]


def valid_card(**overrides: object) -> dict:
    card: dict = {f"{cid}_score": "3" for cid in EXPECTED_IDS}
    details = {cid: {"evidence": [f"docs/case_study_48_addendum.md:{n}"], "rationale": f"{cid} rationale", "change_reason": ""} for n, cid in enumerate(EXPECTED_IDS, 1)}
    card["details"] = json.dumps(details)
    card["summary"] = "Runtime regression scorecard"
    card.update(overrides)
    return card


# --- Generated config and schema --------------------------------------------


def test_rubric_ids_match_expected_groups():
    # Arrange / Act / Assert
    assert IDS == EXPECTED_IDS


def test_generated_config_declares_exact_required_inputs():
    # Arrange
    config = json.loads(generated_config_text())[CONFIG_KEY]

    # Act
    inputs = config["inputs"]

    # Assert
    assert len(inputs) == 22
    assert sorted(inputs) == sorted(expected_fields())
    for name, spec in inputs.items():
        assert spec.get("required") is True, name
        if name.endswith("_score"):
            assert spec["type"] == "choice", name
            assert spec["options"] == SCORE_OPTIONS, name
        else:
            assert spec["type"] == "string", name
            assert "options" not in spec, name


def test_generated_tool_schema_is_strict_with_score_enum():
    # Arrange
    schema = generated_tool_schema()["inputSchema"]

    # Act
    properties = schema["properties"]

    # Assert
    assert schema["type"] == "object"
    assert schema["additionalProperties"] is False
    assert sorted(schema["required"]) == sorted(expected_fields())
    assert sorted(properties) == sorted(expected_fields())
    for name, prop in properties.items():
        assert prop["type"] == "string", name
        if name.endswith("_score"):
            assert prop["enum"] == SCORE_OPTIONS, name
        else:
            assert "enum" not in prop, name


# --- Real runtime harness ---------------------------------------------------


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


@pytest.fixture(scope="module")
def runtime_dir() -> Path:
    value = os.environ.get("GH_AW_RUNTIME_DIR")
    if not value:
        pytest.skip("GH_AW_RUNTIME_DIR is not set; real gh-aw safe-outputs runtime unavailable")
    path = Path(value)
    if not (path / "mcp_server_core.cjs").is_file():
        pytest.skip(f"GH_AW_RUNTIME_DIR={value} does not contain mcp_server_core.cjs")
    if shutil.which("node") is None:
        pytest.skip("node is not available to execute the gh-aw runtime")
    return path


def test_runtime_matches_pinned_gh_aw_actions_blobs(runtime_dir):
    # Arrange / Act
    actual = {name: git_blob_sha(runtime_dir / name) for name in PINNED_BLOBS}

    # Assert
    assert actual == PINNED_BLOBS


@pytest.fixture
def runtime(runtime_dir, tmp_path) -> dict:
    """Write the generated config and build tools.json with the real generator."""
    safe = tmp_path / "safeoutputs"
    safe.mkdir()
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    config_path = safe / "config.json"
    config_path.write_text(generated_config_text(), encoding="utf-8")
    tools_path = safe / "tools.json"
    tools_env = generated_tools_env()
    env = {
        **os.environ,
        "RUNNER_TEMP": str(tmp_path),
        "GITHUB_WORKSPACE": str(workspace),
        "GH_AW_MCP_LOG_DIR": str(tmp_path / "logs"),
        "GH_AW_SAFE_OUTPUTS": str(safe / "outputs.jsonl"),
        "GH_AW_SAFE_OUTPUTS_CONFIG_PATH": str(config_path),
        "GH_AW_SAFE_OUTPUTS_TOOLS_PATH": str(tools_path),
        "GH_AW_SAFE_OUTPUTS_TOOLS_SOURCE_PATH": str(runtime_dir / "safe_outputs_tools.json"),
        "GH_AW_TOOLS_META_JSON": tools_env["GH_AW_TOOLS_META_JSON"],
        "GH_AW_VALIDATION_JSON": tools_env["GH_AW_VALIDATION_JSON"],
    }
    env.pop("GH_AW_POLICY_ALLOW_CREATE_PULL_REQUEST", None)
    script = "require(process.argv[1]).main()"
    generator = subprocess.run(
        ["node", "-e", script, str(runtime_dir / "generate_safe_outputs_tools.cjs")],
        cwd=runtime_dir, env=env, capture_output=True, text=True, timeout=TIMEOUT,
    )
    assert generator.returncode == 0, generator.stderr
    tools = json.loads(tools_path.read_text(encoding="utf-8"))
    generated = [tool for tool in tools if tool["name"] == TOOL]
    assert len(generated) == 1
    assert generated[0]["inputSchema"] == generated_tool_schema()["inputSchema"]
    return {"dir": runtime_dir, "env": env, "config": config_path, "outputs": safe / "outputs.jsonl", "tmp": tmp_path}


class StdioClient:
    def __init__(self, runtime: dict):
        self.stderr = open(runtime["tmp"] / "stdio.stderr.log", "w", encoding="utf-8")
        self.proc = subprocess.Popen(
            ["node", str(runtime["dir"] / "safe_outputs_mcp_server.cjs")],
            cwd=runtime["dir"], env=runtime["env"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.stderr, text=True, encoding="utf-8", bufsize=1,
        )
        self.lines: queue.Queue = queue.Queue()
        threading.Thread(target=self._read, daemon=True).start()
        self.next_id = 0

    def _read(self) -> None:
        for line in self.proc.stdout:
            self.lines.put(line)

    def call(self, method: str, params: dict) -> dict:
        self.next_id += 1
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params}) + "\n")
        self.proc.stdin.flush()
        deadline = time.monotonic() + TIMEOUT
        while True:
            try:
                message = json.loads(self.lines.get(timeout=max(0.1, deadline - time.monotonic())))
            except queue.Empty as exc:
                raise AssertionError(f"stdio server did not answer {method}") from exc
            if message.get("id") == self.next_id:
                return message

    def close(self) -> None:
        self.proc.stdin.close()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        self.stderr.close()


class HttpClient:
    def __init__(self, runtime: dict):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            self.port = sock.getsockname()[1]
        self.stderr = open(runtime["tmp"] / "http.stderr.log", "w", encoding="utf-8")
        self.proc = subprocess.Popen(
            ["node", str(runtime["dir"] / "safe_outputs_mcp_server_http.cjs"), "--port", str(self.port)],
            cwd=runtime["dir"], env=runtime["env"], stdout=self.stderr, stderr=subprocess.STDOUT,
        )
        self.next_id = 0
        deadline = time.monotonic() + TIMEOUT
        while True:
            if self.proc.poll() is not None:
                raise AssertionError(f"HTTP server exited with {self.proc.returncode}")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/health", timeout=2) as response:
                    if response.status == 200:
                        break
            except (urllib.error.URLError, ConnectionError):
                if time.monotonic() > deadline:
                    raise AssertionError("HTTP server did not become healthy")
                time.sleep(0.2)

    def call(self, method: str, params: dict) -> dict:
        self.next_id += 1
        body = json.dumps({"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params}).encode()
        request = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/", data=body, method="POST",
            headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        )
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            return {"http_status": exc.code, **json.loads(exc.read() or b"{}")}

    def close(self) -> None:
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        self.stderr.close()


def output_lines(runtime: dict) -> list[dict]:
    path = runtime["outputs"]
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def without(card: dict, *keys: str) -> dict:
    return {key: value for key, value in card.items() if key not in keys}


INVALID_CARDS = {
    "missing_A2": (without(valid_card(), "A2_score"), "A2_score"),
    "missing_details": (without(valid_card(), "details"), "details"),
    "blank_summary": (valid_card(summary="   "), "summary"),
    "extra_key": (valid_card(A1_evidence="[]"), "A1_evidence"),
    "null_score": (valid_card(A1_score=None), "A1_score"),
    "number_score": (valid_card(A1_score=3), "A1_score"),
    "object_details": (valid_card(details={"A1": {}}), "details"),
    "invalid_choice": (valid_card(B3_score="6"), "B3_score"),
}


@pytest.fixture(params=["stdio", "http"])
def client(request, runtime):
    instance = (StdioClient if request.param == "stdio" else HttpClient)(runtime)
    yield instance
    instance.close()


def start(client) -> None:
    init = client.call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "pytest", "version": "1"}})
    assert "result" in init, init
    listed = client.call("tools/list", {})
    tools = {tool["name"]: tool for tool in listed["result"]["tools"]}
    assert tools[TOOL]["inputSchema"] == generated_tool_schema()["inputSchema"]


def call(client, arguments: dict) -> dict:
    return client.call("tools/call", {"name": TOOL, "arguments": arguments})


def test_runtime_rejects_invalid_cards_before_append_then_accepts_corrected_retry(runtime, client):
    # Arrange
    start(client)

    # Act / Assert: each invalid card is rejected with -32602 and appends nothing
    for case, (arguments, field) in INVALID_CARDS.items():
        response = call(client, arguments)
        assert "error" in response, (case, response)
        assert response["error"]["code"] == -32602, (case, response)
        assert field in response["error"]["message"], (case, response["error"]["message"])
        assert output_lines(runtime) == [], case

    # Act / Assert: corrected retry is accepted and appended once
    card = valid_card()
    accepted = call(client, card)
    assert "error" not in accepted, accepted
    assert json.loads(accepted["result"]["content"][0]["text"]) == {"result": "success"}
    assert output_lines(runtime) == [{**card, "type": TOOL}]


def test_runtime_appends_second_valid_card_but_gate_rejects_multiple_items(runtime, client):
    # Arrange
    start(client)
    card = valid_card()
    assert "error" not in call(client, card)

    # Act
    second = call(client, valid_card(summary="second"))

    # Assert: MCP has no custom-job one-call limit; the deterministic gate refuses two.
    assert "error" not in second, second
    items = output_lines(runtime)
    assert items == [{**card, "type": TOOL}, {**valid_card(summary="second"), "type": TOOL}]
    parsed, error = gate.parse_scorecard(items, EXPECTED_IDS)
    assert parsed is None
    assert error == "expected exactly one record_rubric_score call, found 2"


def test_runtime_accepts_malformed_details_json_but_gate_rejects_attempt_pair(runtime, client):
    """Characterises the runtime boundary: details content is validated downstream only.

    The runtime checks only that details is a non-blank string, so a malformed
    card is appended; the adapter rejects it when the gate reads one item.
    """
    # Arrange
    start(client)
    card = valid_card(details="{not valid json")

    # Act
    response = call(client, card)
    retry_card = valid_card()
    retry = call(client, retry_card)

    # Assert
    assert "error" not in response, response
    assert "error" not in retry, retry
    items = output_lines(runtime)
    assert items == [{**card, "type": TOOL}, {**retry_card, "type": TOOL}]
    parsed, error = gate.parse_scorecard(items, EXPECTED_IDS)
    assert parsed is None
    assert error == "expected exactly one record_rubric_score call, found 2"
    parsed, error = gate.parse_scorecard([items[0]], EXPECTED_IDS)
    assert parsed is None and "details is not valid JSON" in error