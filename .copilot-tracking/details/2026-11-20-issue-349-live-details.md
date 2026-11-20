# Details
Test only, no src change. For principals (a) valid aad, tenant ok, roles=() ; (b) wrong tenant with a staff role:
/app -> 403 containing the sign-out link, /api/me -> 401. Anonymous /app stays 302 to /sign-in.
