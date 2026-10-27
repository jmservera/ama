-- Synthetic resident showcase boundary (issue 462). Reviewable T-SQL; applied only by
-- infra/scripts/resident_showcase_sql.py in a gated private step. Batches are split on GO.
--
-- Model: schema, table and view are owned by dbo, so the view reads dbo.cases through an unbroken
-- ownership chain. The showcase principal gets SELECT on the single view and nothing else, no role
-- membership, and is explicitly denied the base table and any write or DDL. The allowlist table
-- ships EMPTY: nothing is visible until an owner-approved step inserts rows with a provenance
-- reference. Email canonical form is identical to the application: trim spaces, lower-case, ASCII
-- only, compared with Latin1_General_100_BIN2; duplicates are counted across ALL cases. The view
-- is not capped: the application refuses more than 25 rows instead of silently truncating.
IF SCHEMA_ID(N'resident_showcase') IS NULL EXEC(N'CREATE SCHEMA resident_showcase AUTHORIZATION dbo');
GO
IF OBJECT_ID(N'resident_showcase.allowed_case', N'U') IS NULL
CREATE TABLE resident_showcase.allowed_case (
  case_id NVARCHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL PRIMARY KEY,
  provenance NVARCHAR(200) NOT NULL,
  valid_from DATETIME2(0) NOT NULL,
  valid_to DATETIME2(0) NOT NULL,
  revoked BIT NOT NULL CONSTRAINT df_allowed_case_revoked DEFAULT 0,
  CONSTRAINT ck_allowed_case_provenance CHECK (LEN(LTRIM(RTRIM(provenance))) > 0),
  CONSTRAINT ck_allowed_case_window CHECK (valid_to > valid_from AND valid_to <= '2026-11-01T00:00:00')
);
GO
-- Optional tables are bound only when present at the separately authorised view apply.
-- No sensor table is created and the resident principal receives no additional grant.
-- BIN2 equality still pads spaces; common Unicode byte lengths make each match exact.
DECLARE @history NVARCHAR(MAX) = N'CAST(NULL AS NVARCHAR(128)) AS sensor_home_id,
  N''[]'' AS sensors_json';
IF OBJECT_ID(N'dbo.sensor_register', N'U') IS NOT NULL
   AND OBJECT_ID(N'dbo.sensor_reading', N'U') IS NOT NULL
SET @history = N'JSON_VALUE(k.body, ''$.home.stock_id'') AS sensor_home_id,
  (SELECT TOP (48) r.home_id, CONVERT(VARCHAR(19), r.observed_at, 126) + ''Z'' AS observed_at,
          r.temperature_c, r.humidity_pct, r.source_type, r.injected_fault
   FROM dbo.sensor_reading AS r
   JOIN dbo.sensor_register AS s
     ON s.sensor_id COLLATE Latin1_General_100_BIN2 = r.sensor_id COLLATE Latin1_General_100_BIN2
    AND DATALENGTH(CONVERT(NVARCHAR(MAX), s.sensor_id)) =
          DATALENGTH(CONVERT(NVARCHAR(MAX), r.sensor_id))
   WHERE s.home_id COLLATE Latin1_General_100_BIN2 =
           JSON_VALUE(k.body, ''$.home.stock_id'') COLLATE Latin1_General_100_BIN2
     AND DATALENGTH(CONVERT(NVARCHAR(MAX), s.home_id)) =
           DATALENGTH(JSON_VALUE(k.body, ''$.home.stock_id''))
     AND r.home_id COLLATE Latin1_General_100_BIN2 =
           JSON_VALUE(k.body, ''$.home.stock_id'') COLLATE Latin1_General_100_BIN2
     AND DATALENGTH(CONVERT(NVARCHAR(MAX), r.home_id)) =
           DATALENGTH(JSON_VALUE(k.body, ''$.home.stock_id''))
     AND s.source_type COLLATE Latin1_General_100_BIN2 = ''SYNTHETIC''
     AND DATALENGTH(CONVERT(NVARCHAR(MAX), s.source_type)) = DATALENGTH(N''SYNTHETIC'')
     AND r.source_type COLLATE Latin1_General_100_BIN2 = ''SYNTHETIC''
     AND DATALENGTH(CONVERT(NVARCHAR(MAX), r.source_type)) = DATALENGTH(N''SYNTHETIC'')
   ORDER BY r.observed_at DESC, r.sensor_id, r.reading_id
   FOR JSON PATH, INCLUDE_NULL_VALUES) AS sensors_json';
DECLARE @view NVARCHAR(MAX) = N'CREATE OR ALTER VIEW resident_showcase.v_resident_case AS
WITH canon AS (
  SELECT c.id, c.stage, c.closed, c.body,
         CASE WHEN ISJSON(c.body) = 1
              THEN LOWER(LTRIM(RTRIM(JSON_VALUE(c.body, ''$.resident.email'')))) COLLATE Latin1_General_100_BIN2
         END AS email
  FROM dbo.cases AS c
), counted AS (
  SELECT id, stage, closed, body, email,
         CASE WHEN email IS NULL THEN 0 ELSE COUNT(*) OVER (PARTITION BY email) END AS email_count
  FROM canon
)
SELECT
  k.id AS case_id,
  k.email AS email,
  CAST(k.email_count AS INT) AS email_count,
  a.provenance AS provenance,
  a.valid_from AS valid_from,
  a.valid_to AS valid_to,
  a.revoked AS revoked,
  LEFT(JSON_VALUE(k.body, ''$.home.address''), 120) AS address,
  LEFT(JSON_VALUE(k.body, ''$.home.town''), 120) AS town,
  LEFT(JSON_VALUE(k.body, ''$.home.postcode''), 120) AS postcode,
  k.stage AS stage,
  CAST(k.closed AS BIT) AS closed,
  JSON_QUERY(k.body, ''$.measures'') AS measures_json,
  LEFT(JSON_VALUE(k.body, ''$.measures''), 1000) AS measures_text,
  ' + @history + N'
FROM counted AS k
JOIN resident_showcase.allowed_case AS a ON a.case_id = k.id
WHERE k.email IS NOT NULL;';
EXEC sys.sp_executesql @view;
GO
DENY SELECT, INSERT, UPDATE, DELETE, ALTER, REFERENCES ON OBJECT::dbo.cases TO [{{PRINCIPAL}}];
GO
DENY INSERT, UPDATE, DELETE, ALTER, EXECUTE, REFERENCES ON SCHEMA::resident_showcase TO [{{PRINCIPAL}}];
GO
GRANT SELECT ON OBJECT::resident_showcase.v_resident_case TO [{{PRINCIPAL}}];
