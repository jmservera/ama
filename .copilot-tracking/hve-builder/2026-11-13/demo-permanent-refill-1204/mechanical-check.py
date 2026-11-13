"""Exercise the documented launcher with an owned, harmless worker stand-in."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import uuid

ROOT = Path(__file__).parent
TARGET = Path("/home/azureuser/source/ama-demo-wt/demo-permanent-refill-1204-0914")
REV = "cbb5d01a40f0c8b812574510b0f805cf9889832a"
assert subprocess.check_output(["git", "-C", str(TARGET), "rev-parse", "HEAD"], text=True).strip() == REV
body = subprocess.check_output(
    ["git", "-C", str(TARGET), "show", f"{REV}:.github/agents/ama-backlog-delivery-coordinator.agent.md"],
    text=True,
)
lines = body.splitlines()
start = next(i for i, line in enumerate(lines) if line.strip() == "#!/usr/bin/env bash")
end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "```")
launcher = textwrap.dedent("\n".join(lines[start:end])) + "\n"
name = "rpi-mech-1204-" + uuid.uuid4().hex
log = Path("/tmp") / f"{name}.log"
payload = "literal $HOME $(printf EXPANDED) `printf BACKTICK` 'single' \"double\" \\\nsecond line"
results = []
with log.open("x") as stream:
    stream.write("historical-sentinel\n")
try:
    with tempfile.TemporaryDirectory(prefix="ama-refill-mech-") as directory:
        temp = Path(directory)
        script = temp / "launcher.sh"
        script.write_text(launcher)
        brief = temp / "brief with spaces.md"
        brief.write_text(payload)
        capture = temp / "args.json"
        stub = temp / "copilot"
        stub.write_text(
            "#!/usr/bin/env python3\n"
            "import json, os, sys\n"
            "with open(os.environ['STUB_CAPTURE'], 'w') as stream: json.dump(sys.argv[1:], stream)\n"
            "print('stub stdout'); print('stub stderr', file=sys.stderr)\n"
            "sys.exit(int(os.environ['STUB_EXIT']))\n"
        )
        stub.chmod(0o700)
        subprocess.run(["bash", "-n", str(script)], check=True)
        for attempt, expected in [("attempt-1", 17), ("attempt-2", 0)]:
            env = {
                "PATH": str(temp) + os.pathsep + os.environ["PATH"],
                "STUB_CAPTURE": str(capture),
                "STUB_EXIT": str(expected),
            }
            command = [
                "/bin/sh", "-c", 'exec bash "$1" "$2" "$3" "$4"',
                "contained-launch", str(script), name, attempt, str(brief),
            ]
            run = subprocess.run(command, env=env, text=True, capture_output=True, timeout=15)
            args = json.loads(capture.read_text())
            assert args[args.index("-p") + 1] == payload
            assert run.returncode == expected, (run.returncode, run.stdout, run.stderr)
            results.append({
                "attempt": attempt, "expected_exit": expected, "actual_exit": run.returncode,
                "literal_brief_preserved": True, "stdout": run.stdout, "stderr": run.stderr,
            })
        content = log.read_text()
        assert content.startswith("historical-sentinel\n")
        for marker in ["--- launch attempt-1", "exit=17", "--- launch attempt-2", "exit=0"]:
            assert marker in content
        report = {
            "target_revision": REV, "outer_shell": "/bin/sh", "explicit_launcher_shell": "bash",
            "bash_syntax_exit": 0, "attempts": results, "append_only_log": content,
            "scope": "Extracted script and explicitly quoted shell arguments; full tmux command interpolation not exercised.",
            "real_copilot_model_calls": 0,
        }
        with (ROOT / "mechanical-result.json").open("x") as stream:
            json.dump(report, stream, indent=2)
            stream.write("\n")
        print(json.dumps(report, indent=2))
finally:
    log.unlink()
