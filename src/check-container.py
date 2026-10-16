"""Exercise a built source image, including unsafe-launch rejection and API health."""

import argparse
import json
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.error import URLError
from urllib.request import urlopen

CONTROLS = [
    "--read-only",
    "--cap-drop=ALL",
    "--security-opt=no-new-privileges",
]
PROBE = """
import errno, os
from pathlib import Path
assert os.getuid() == os.getgid() == 10001
assert os.statvfs('/').f_flag & os.ST_RDONLY
status = dict(line.split(':', 1) for line in Path('/proc/1/status').read_text().splitlines())
assert all(int(status[k].strip(), 16) == 0 for k in
           ('CapInh', 'CapPrm', 'CapEff', 'CapBnd', 'CapAmb'))
assert status['NoNewPrivs'].strip() == '1'
try:
    Path('/app/security-probe').write_text('must fail')
except OSError as error:
    assert error.errno == errno.EROFS, error
else:
    raise AssertionError('root filesystem accepted a write')
Path('/state/security-probe').write_text('writable state')
assert not Path('/app/data').exists()
assert not Path('/data/zavaforward.json').exists()
"""


def docker(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["docker", *args], check=False, capture_output=True, text=True)
    if check and result.returncode:
        raise RuntimeError(f"docker {args}: {result.stdout}\n{result.stderr}")
    return result


def check_image(image: str, project: str) -> None:
    metadata = json.loads(docker("image", "inspect", image).stdout)[0]["Config"]
    assert metadata["User"] == "10001:10001", metadata["User"]
    assert metadata["Entrypoint"] == ["python", "/usr/local/bin/container-entrypoint.py"]
    writable = [
        "--tmpfs=/tmp:rw,nosuid,nodev",
        "--tmpfs=/state:rw,nosuid,nodev,uid=10001,gid=10001",
    ]
    docker("run", "--rm", *CONTROLS, *writable, image, "python", "-c", PROBE)
    for flags, expected in (
        (CONTROLS[1:], "root filesystem must be read-only"),
        ([CONTROLS[0], CONTROLS[2]], "must be zero"),
        (CONTROLS[:2], "NoNewPrivs must be enabled"),
        ([*CONTROLS, "--user=0:0"], "UID and GID must both be 10001"),
        ([*CONTROLS, "--user=10001:0"], "UID and GID must both be 10001"),
    ):
        result = docker(
            "run", "--rm", *flags, image, "python", "-c", "print('UNSAFE')", check=False
        )
        assert result.returncode == 78, (flags, result.returncode, result.stderr)
        assert expected in result.stderr and "UNSAFE" not in result.stdout, result
    if project == "agents":
        docker(
            "run",
            "--rm",
            *CONTROLS,
            image,
            "python",
            "-c",
            "import importlib.util as u; "
            "assert not any(u.find_spec(m) for m in ('mssql_python', 'azure'))",
        )
    if project != "api":
        result = docker("run", "--rm", *CONTROLS, *writable, image)
        dist = "import" if project == "importer" else project
        assert result.stdout.strip() == f"zava-forward-{dist} 0.1.0", result.stdout
        return
    with TemporaryDirectory(prefix="zf-container-") as directory:
        seed = Path(directory)
        seed.chmod(0o755)
        (seed / "zavaforward.json").write_text('{"cases":[],"staff":[]}', encoding="utf-8")
        (seed / "zavaforward.json").chmod(0o644)
        container = docker(
            "run",
            "-d",
            *CONTROLS,
            *writable,
            "--publish=127.0.0.1::8088",
            "--env=ZF_AI=off",
            "--mount",
            f"type=bind,source={seed},target=/data,readonly",
            image,
        ).stdout.strip()
        try:
            port = docker("port", container, "8088").stdout.strip().rsplit(":", 1)[1]
            url = f"http://127.0.0.1:{port}"
            for _ in range(60):
                try:
                    with urlopen(f"{url}/healthz", timeout=2) as response:
                        assert response.status == 200
                    break
                except (URLError, ConnectionError, TimeoutError) as error:
                    if (
                        docker("inspect", "--format={{.State.Running}}", container).stdout
                        != "true\n"
                    ):
                        logs = docker("logs", container)
                        raise AssertionError(f"{logs.stdout}\n{logs.stderr}") from error
                    time.sleep(0.5)
            else:
                raise AssertionError(f"API health timeout: {docker('logs', container).stdout}")
            with urlopen(f"{url}/zava-logo.png", timeout=3) as response:
                assert response.headers["Content-Type"] == "image/png"
                assert (
                    response.read()
                    == (
                        Path(__file__).parent / "api/src/zava_forward/api/web/zava-logo.png"
                    ).read_bytes()
                )
            docker(
                "exec",
                container,
                "python",
                "-c",
                "from pathlib import Path; Path('/state/api-probe').write_text('ok')",
            )
        finally:
            docker("rm", "-f", container)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", choices=("api", "agents", "orchestrator", "importer"))
    parser.add_argument("image")
    arguments = parser.parse_args()
    check_image(arguments.image, arguments.project)
    print(f"{arguments.project}: hardened runtime, negative launches and application check PASS")
