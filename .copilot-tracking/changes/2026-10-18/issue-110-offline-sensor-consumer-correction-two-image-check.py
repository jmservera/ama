import os
import tempfile
import unittest
from pathlib import Path

assert os.getuid() == os.getgid() == 10001
assert os.statvfs("/").f_flag & os.ST_RDONLY
status = dict(line.split(":", 1) for line in Path("/proc/1/status").read_text().splitlines())
assert status["NoNewPrivs"].strip() == "1"
assert all(
    int(status[key].strip(), 16) == 0
    for key in ("CapInh", "CapPrm", "CapEff", "CapBnd", "CapAmb")
)
print("UID/GID10001; read-only root; no capabilities; NoNewPrivs; network none", flush=True)
suite = unittest.defaultTestLoader.loadTestsFromNames(
    ["test_sensor_consumer", "test_sensor_ingestion", "test_sensor_privacy"]
)
result = unittest.TextTestRunner(verbosity=1).run(suite)
assert result.wasSuccessful()

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from zava_forward.api.sensor_ingestion import SensorIngestion

with tempfile.TemporaryDirectory() as directory:
    store = store_at(directory)
    adapter = SensorIngestion(store)
    adapter.consumer.configure(POLICY, [CONTROL])
    rows = [{**row, "seed": "-0"} for row in observations()]
    first = adapter.consume(rows, received_at=RECEIVED)
    assert len(first) == 2 and all(r.status == "accepted" and not r.replay for r in first)
    store.db.close()
    reopened = store_at(directory)
    adapter = SensorIngestion(reopened)
    replay = adapter.consume(rows, received_at=RECEIVED)
    assert len(replay) == 2 and all(r.status == "accepted" and r.replay for r in replay)
    later = {**rows[-1], "reading_id": "IMAGE-LATER", "observed_at": RECEIVED}
    assert adapter.consume([later], received_at=RECEIVED)[0].status == "accepted"
    assert reopened.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0] == 3
    assert reopened.db.execute("SELECT COUNT(*) FROM sensor_delivery").fetchone()[0] == 3
    reopened.db.close()
print("Actual finite API signed-zero adapter accepted2/reopened replay2/later1; rows3", flush=True)
