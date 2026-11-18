import pexpect, re, sys
cmds = ["id", "grep Cap /proc/self/status", "grep NoNew /proc/self/status", "grep overlay /proc/mounts",
        "touch /usr/zz", "touch /tmp/zz144r4 && echo tmp-ok", "rm -f /tmp/zz144r4", "env | grep -c ZF_CONTAINER"]
c = pexpect.spawn("az containerapp exec -g ama -n ca-cutover-test-demo-api --container api --command sh",
                  encoding="utf-8", timeout=90)
log = []
try:
    c.expect(r"\$ ", timeout=90)
    log.append(c.before)
    for cmd in cmds:
        c.sendline(cmd)
        c.expect(r"\$ ", timeout=30)
        log.append("$ " + cmd + "\n" + c.before.split("\n", 1)[-1])
    c.sendline("exit")
finally:
    c.close()
out = "\n".join(log)
out = re.sub(r"Replica: '[^']+'", "Replica: '<replica>'", out)
out = re.sub(r"containerFs/[^/]+", "containerFs/<id>", out)
print(out)
