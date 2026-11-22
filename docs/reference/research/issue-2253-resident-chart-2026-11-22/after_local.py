"""After-fix proof: serve the fixed web files with the sensor browser-check fixtures and measure at 1440x900."""

import json
import sys
import threading

from playwright.sync_api import sync_playwright
from zava_forward.core import resident_showcase as rs

from checks import resident_sensors_browser_check as c
from probe_chart import measure
from zava_forward.api.resident_demo import app as demo

reader = c.FixtureReader()
codec = rs.SessionCodec(b"fake-browser-test-session-key-only", rs.AUTHORITY_END, lambda: c.NOW.timestamp())
app = demo.ResidentDemo(
    reader, rs.build_identity_map(reader.list_rows(), c.NOW),
    rs.PasswordVerifier(rs.make_verifier(c.FAKE_PASSWORD, n=2**14)), codec, rs.LoginLimiter(),
    ("127.0.0.1",), rs.AUTHORITY_END, port=0, clock=lambda: c.NOW.timestamp(),
)
server = demo.serve(app)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{app.port}/"
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_context(viewport={"width": 1440, "height": 900}).new_page()
    c.sign_in(page, base, "alice@example.com")
    print(json.dumps(measure(page, sys.argv[1])))
    b.close()
server.shutdown()
