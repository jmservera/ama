"""Run the rendered public simulation startup recipe in the actual API image (Refs #136, #1288).

Needs Docker and a prebuilt image supplied as ZF_API_IMAGE (built with
`docker build -f src/api/Dockerfile src`). Uses only disposable containers and volumes.
"""

import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
import uuid
from urllib.error import URLError
from urllib.request import urlopen

from test_bicep_policy import compile_bicep, render_api_container

IMAGE = os.environ.get("ZF_API_IMAGE", "")
CONTROLS = [
    "--user=10001:10001",
    "--read-only",
    "--cap-drop=ALL",
    "--security-opt=no-new-privileges",
    "--tmpfs=/tmp:rw,nosuid,nodev",
]
INSPECT = """
import hashlib, json, os, stat
out = {}
for name in ("store.sqlite", "hmac.key"):
    path = "/state/public-simulation/" + name
    if os.path.lexists(path):
        data = open(path, "rb").read()
        out[name] = [stat.S_IMODE(os.stat(path).st_mode), hashlib.sha256(data).hexdigest()]
out["dir"] = stat.S_IMODE(os.stat("/state/public-simulation").st_mode)
print(json.dumps(out))
"""
LANE = """
import json, os
from zava_forward.core import simulation_lane as lane
opened = lane.Lane.open(os.environ)
added = opened.observe()
view = opened.view()
opened.close()
print(json.dumps({"added": added, "keys": sorted(view)}))
"""


def docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["docker", *args], check=False, capture_output=True, text=True)
    if check and result.returncode:
        raise AssertionError(f"docker {args[:2]}: {result.stdout}\n{result.stderr}")
    return result


@unittest.skipUnless(
    shutil.which("docker") and shutil.which("az") and IMAGE,
    "Docker, Azure CLI with Bicep and ZF_API_IMAGE are needed to execute the recipe",
)
class PublicSimulationStartupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        container = render_api_container(
            compile_bicep("main.bicep"), enablePublicSimulationLane=True
        )["containers"][0]
        cls.command = container["command"]
        cls.env = [
            f"--env={e['name']}={e['value']}"
            for e in container["env"]
            if e["name"].startswith("ZF_SIM_")
        ]
        cls.run_id = uuid.uuid4().hex[:8]
        cls.created: list[str] = []
        cls.data = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.data.cleanup)
        dataset = os.path.join(cls.data.name, "zavaforward.json")
        with open(dataset, "w", encoding="utf-8") as handle:
            handle.write('{"cases":[],"staff":[]}')
        os.chmod(dataset, 0o644)
        os.chmod(cls.data.name, 0o755)

    def setUp(self) -> None:
        self.volume = f"zf-sim-test-{self.run_id}-{len(self.created)}"
        docker("volume", "create", self.volume)
        self.created.append(self.volume)
        self.addCleanup(docker, "volume", "rm", "-f", self.volume, check=False)

    def seed(self, script: str) -> None:
        docker(
            "run", "--rm", *CONTROLS, f"--volume={self.volume}:/state", IMAGE, "python", "-c", script
        )

    def start(self) -> str:
        """Start the rendered command with no entrypoint override and wait for the ordinary API."""
        name = f"{self.volume}-api"
        docker(
            "run", "-d", "--name", name, *CONTROLS, f"--volume={self.volume}:/state",
            "--env=ZF_AI=off", "--publish=127.0.0.1::8088",
            f"--mount=type=bind,source={self.data.name},target=/data,readonly", *self.env, IMAGE, *self.command,
        )  # fmt: skip
        self.addCleanup(docker, "rm", "-f", name, check=False)
        port = docker("port", name, "8088").stdout.strip().rsplit(":", 1)[1]
        for _ in range(80):
            try:
                with urlopen(f"http://127.0.0.1:{port}/healthz", timeout=2) as response:
                    self.assertEqual(response.status, 200)
                return name
            except (URLError, ConnectionError, TimeoutError):
                if docker("inspect", "--format={{.State.Running}}", name).stdout != "true\n":
                    break
                time.sleep(0.5)
        raise AssertionError(docker("logs", name).stdout + docker("logs", name).stderr)

    def stop(self, name: str) -> str:
        logs = docker("logs", name).stderr
        docker("rm", "-f", name)
        return logs

    def inspect(self, name: str) -> dict:
        return json.loads(docker("exec", name, "python", "-c", INSPECT).stdout)

    def test_fresh_start_initialises_then_reuses_without_reset(self) -> None:
        name = self.start()
        state = self.inspect(name)
        self.assertEqual(state["hmac.key"][0], 0o600)
        self.assertEqual(state["store.sqlite"][0], 0o600)
        self.assertEqual(state["dir"], 0o700)
        user = docker("exec", name, "python", "-c", "import os; print(os.getuid(), os.getgid())")
        self.assertEqual(user.stdout.strip(), "10001 10001")
        first = json.loads(docker("exec", name, *["env", *[e[6:] for e in self.env]],
                                  "python", "-c", LANE).stdout)  # fmt: skip
        self.assertEqual(first["added"], 12)
        self.assertEqual(self.stop(name), "")

        again = self.start()
        self.assertEqual(self.inspect(again)["hmac.key"], state["hmac.key"])
        second = json.loads(docker("exec", again, *["env", *[e[6:] for e in self.env]],
                                   "python", "-c", LANE).stdout)  # fmt: skip
        self.assertEqual(second["added"], 0)
        self.assertEqual(self.stop(again), "")

    def test_partial_and_corrupt_state_are_untouched_and_the_api_still_starts(self) -> None:
        cases = {
            "key-only": "import os; os.makedirs('/state/public-simulation', mode=0o700, exist_ok=True);"
            "open('/state/public-simulation/hmac.key','wb').write(b'k'*32)",
            "corrupt-store": "import os; os.makedirs('/state/public-simulation', mode=0o700, exist_ok=True);"
            "open('/state/public-simulation/store.sqlite','wb').write(b'not sqlite');"
            "open('/state/public-simulation/hmac.key','wb').write(b'k'*32)",
        }
        for label, script in cases.items():
            with self.subTest(label):
                docker("volume", "rm", "-f", self.volume, check=False)
                docker("volume", "create", self.volume)
                self.seed(script + ";os.chmod('/state/public-simulation/hmac.key',0o600)")
                before = json.loads(
                    docker(
                        "run", "--rm", *CONTROLS, f"--volume={self.volume}:/state",
                        IMAGE, "python", "-c", INSPECT,
                    ).stdout
                )  # fmt: skip
                api = self.start()
                self.assertEqual(self.inspect(api), before)
                logs = self.stop(api)
                self.assertIn("public simulation lane unavailable", logs)
                self.assertNotIn("kkkk", logs)
