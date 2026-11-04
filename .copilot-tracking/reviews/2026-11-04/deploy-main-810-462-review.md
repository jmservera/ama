# Review (2026-11-04)

Execution: executed once. Outcome: deployment conformant; #810 NOT resolved; #462 partially verified.

* #810: unauthenticated Easy Auth requests through the live demo API (transport Http) still gave empty-body 500s under concurrency: 3 of 160 (mixed paths), then 5 of 144, then 3 of 80 on `/healthz` (about 2 to 3.5 percent). Sequential 60 of 60 were 200. Control: resident app (no Easy Auth) 80 of 80 200. 500s carry `content-length: 0` and `x-ms-middleware-request-id` (Easy Auth middleware). Authenticated calls could not be made (no token without a new role).
* #462: 320px sign-in verified live (no horizontal overflow, 44px targets, labelled fields). Live `demo.js` is byte-identical to main and contains `Europe/London`, `(UK time)` and the sign-out failure wording. Signed-in history, sensor wording and sign-out were NOT exercised: the shared password is owner-held.
* Routed follow-ups: (1) #810 needs another approach (Easy Auth sidecar/ingress, e.g. replicas, HTTP/2 client protocol, or removing Easy Auth for public paths) under a new approval; (2) owner runs the signed-in #462 walk-through or supplies the password route.
