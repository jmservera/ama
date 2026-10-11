-- Run once after deployment, connected as a member of the SQL Entra admin group
-- through the private network. Bicep cannot create contained database users.
-- Replace the names with the identity names output by the deployment.
-- When the SQL server has no Directory Readers identity, FROM EXTERNAL PROVIDER fails; create the user
-- from the managed identity's client id instead, as a literal binary SID:
--   CREATE USER [id-warm-dev-api] WITH SID = 0x<client id as little-endian GUID bytes>, TYPE = E;
-- The MVP app (mvp/) also needs db_ddladmin on first start so it can create its tables.
-- infra/scripts/create-sql-users.py does all of this (SID form, idempotent) and grants db_ddladmin to the API identity.

CREATE USER [id-warm-dev-api] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [id-warm-dev-api];
ALTER ROLE db_datawriter ADD MEMBER [id-warm-dev-api];

CREATE USER [id-warm-dev-import] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [id-warm-dev-import];
ALTER ROLE db_datawriter ADD MEMBER [id-warm-dev-import];

-- The agents and orchestrator identities are deliberately not granted any
-- database access. They reach data only through the workbench API.
