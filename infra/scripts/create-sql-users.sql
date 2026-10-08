-- Run once after deployment, connected as a member of the SQL Entra admin group
-- through the private network. Bicep cannot create contained database users.
-- Replace the names with the identity names output by the deployment.

CREATE USER [id-warm-dev-api] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [id-warm-dev-api];
ALTER ROLE db_datawriter ADD MEMBER [id-warm-dev-api];

CREATE USER [id-warm-dev-import] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [id-warm-dev-import];
ALTER ROLE db_datawriter ADD MEMBER [id-warm-dev-import];

-- The agents and orchestrator identities are deliberately not granted any
-- database access. They reach data only through the workbench API.
