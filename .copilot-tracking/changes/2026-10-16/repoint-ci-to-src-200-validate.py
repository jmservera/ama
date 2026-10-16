"""Task-only synthetic runtime/image verification; no private input or cloud access."""

import json
import os
from pathlib import Path
import secrets
import subprocess
import tempfile
import time
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path.cwd()
DOCKER = ["sudo", "-n", "docker"]


def docker(*args):
    return subprocess.check_output([*DOCKER, *args], text=True).strip()


def wait_health(url, process=None):
    for _ in range(60):
        if process is not None and process.poll() is not None:
            raise AssertionError("Local API exited before becoming healthy")
        try:
            with urlopen(url + "/healthz", timeout=2) as response:
                assert response.status == 200
            return
        except (URLError, TimeoutError, ConnectionError):
            time.sleep(0.5)
    raise AssertionError("API health timeout")


with tempfile.TemporaryDirectory(prefix="zf200-") as tmp:
    base = Path(tmp)
    seed = base / "seed"
    seed.mkdir()
    (seed / "zavaforward.json").write_text('{"cases":[],"staff":[]}')
    env = {
        "PATH": os.environ["PATH"],
        "HOME": tmp,
        "ZF_DATA": str(seed / "zavaforward.json"),
        "ZF_STATE": str(base / "state"),
        "ZF_PASSWORD": secrets.token_urlsafe(24),
        "ZF_BIND": "127.0.0.1",
        "PORT": "18200",
    }
    process = subprocess.Popen(
        ["/tmp/zf200/bin/python", "-m", "zava_forward.api"],
        cwd=tmp, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
    )
    try:
        wait_health("http://127.0.0.1:18200", process)
        print("Installed local API module: /healthz 200")
    finally:
        process.terminate()
        _, errors = process.communicate(timeout=15)
        if process.returncode not in (-15, 0):
            raise AssertionError(errors.decode())

    base.chmod(0o755)
    seed.chmod(0o755)
    (seed / "zavaforward.json").chmod(0o644)
    version_probe = (
        "from zava_forward.api.version import __version__; "
        'print(f"zava-forward-api {__version__}")'
    )
    for project, dist in (
        ("api", "api"), ("agents", "agents"), ("orchestrator", "orchestrator"),
        ("importer", "import"),
    ):
        image = f"zava-forward-{project}:issue-200"
        assert docker("run", "--rm", "--entrypoint", "id", image, "-u") == "10001"
        docker(
            "run", "--rm", "--entrypoint", "sh", image, "-c",
            "test ! -e /app/data && test ! -e /data/zavaforward.json",
        )
        options = [
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--tmpfs", "/tmp", "--tmpfs", "/state:uid=10001,gid=10001",
            "-v", f"{seed}:/data:ro",
        ]
        command = ["python", "-c", version_probe] if project == "api" else []
        out = docker("run", "--rm", *options, image, *command)
        assert out == f"zava-forward-{dist} 0.1.0", (project, out)
        docker(
            "run", "--rm", *options, "--entrypoint", "sh", image, "-c",
            "touch /state/probe && ! touch /app/probe 2>/dev/null "
            "&& ! touch /probe 2>/dev/null "
            "&& grep -q '^CapEff:.0000000000000000$' /proc/1/status",
        )
        if project == "api":
            docker(
                "run", "--rm", "--entrypoint", "python", image, "-c",
                "import importlib.util as u; "
                "assert u.find_spec('zava_forward.orchestrator') is None",
            )
        if project == "orchestrator":
            docker(
                "run", "--rm", "--entrypoint", "python", image, "-c",
                "import zava_forward.orchestrator.token_store; "
                "import zava_forward.orchestrator.digest_blob",
            )
        if project == "agents":
            docker(
                "run", "--rm", "--entrypoint", "python", image, "-c",
                "import importlib.util as u; "
                "assert not any(u.find_spec(m) for m in ('mssql_python', 'azure'))",
            )
        print(f"{project}: non-root, no-data, read-only, no capabilities, version OK")
        if project == "api":
            container = docker(
                "run", "-d", *options, "-p", "127.0.0.1::8088",
                "-e", f"ZF_PASSWORD={secrets.token_urlsafe(24)}", image,
            )
            try:
                host_port = json.loads(docker("inspect", container))[0][
                    "NetworkSettings"
                ]["Ports"]["8088/tcp"][0]["HostPort"]
                url = f"http://127.0.0.1:{host_port}"
                wait_health(url)
                with urlopen(url + "/zava-logo.png", timeout=5) as response:
                    assert response.headers["Content-Type"] == "image/png"
                    assert response.read() == (
                        ROOT / "src/api/src/zava_forward/api/web/zava-logo.png"
                    ).read_bytes()
                print("Read-only API image: /healthz 200 and exact public logo OK")
            finally:
                docker("rm", "-f", container)
