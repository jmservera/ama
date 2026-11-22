# Plan: issue 2202 live deploy

1. Build zava-forward-api image from src (docker build -f src/api/Dockerfile src), tag by commit.
2. Push with /tmp/acr-push.sh <public-ip> <image>; capture digest; confirm ACR Disabled.
3. az containerapp update of ca-cutover-test-demo-api and az containerapp job update of job-live-simulator and job-live-receiver to the digest.
4. Prove: revision healthy, simulator coverage, consent, gauges, chat routing, receiver run.
5. Write research note, log entries, infra README entry, changes record with per-criterion table.
