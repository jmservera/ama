# Details: issue 2202 live2

check_hardening(runner, group, name, kind) runs `containerapp show` or `containerapp job show` with a JMESPath query for the ZF_CONTAINER_HARDENING env value of the first container; PASS when `enforced`, FAIL otherwise (including absent), FAIL on runner error.
