"""Poll /healthz while the ask probe runs; prints latency lines (no credentials involved)."""
import sys, time, urllib.request, json
APP = "https://ca-cutover-test-demo-api.happyriver-ace49996.uksouth.azurecontainerapps.io"
end = time.time() + float(sys.argv[1]); rows = []
while time.time() < end:
    t0 = time.time()
    try:
        s = urllib.request.urlopen(APP + "/healthz", timeout=30).status
    except Exception as e:
        s = type(e).__name__
    rows.append([round(t0, 1), s, round(time.time() - t0, 2)])
    time.sleep(0.5)
json.dump(rows, open(sys.argv[2], "w"))
slow = [r for r in rows if isinstance(r[1], str) or r[2] > 1]
print(len(rows), "polls;", len(slow), "slow or failed;", "max", max(r[2] for r in rows))
