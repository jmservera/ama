import os,re,uuid,json
import mssql_python
from zava_forward.core.mssqlstore import connection_string
P="id-resident-demo"; CID="ba252cc4-6059-4248-9f21-f6ae7f0cd4d1"
SQL="-- Accounting only. No case facts, prompts, answers, tokens or credentials are stored.\nIF SCHEMA_ID(N'resident_ai') IS NULL EXEC(N'CREATE SCHEMA resident_ai AUTHORIZATION dbo');\nGO\nIF OBJECT_ID(N'resident_ai.budget', N'U') IS NULL\nBEGIN\nCREATE TABLE resident_ai.budget (\n  id INT NOT NULL PRIMARY KEY CHECK (id = 1),\n  reserved_cents INT NOT NULL CHECK (reserved_cents BETWEEN 0 AND 2000)\n);\n  INSERT INTO resident_ai.budget VALUES (1, 0);\nEND;\nGO\nIF OBJECT_ID(N'resident_ai.attempt', N'U') IS NULL\nCREATE TABLE resident_ai.attempt (\n  reservation UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,\n  resident CHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL,\n  reserved_at DATETIME2(7) NOT NULL,\n  prompt_tokens INT NULL CHECK (prompt_tokens BETWEEN 0 AND 8192),\n  completion_tokens INT NULL CHECK (completion_tokens BETWEEN 0 AND 256)\n);\nGO\nCREATE OR ALTER PROCEDURE resident_ai.reserve\n  @resident VARCHAR(64), @reservation UNIQUEIDENTIFIER\nAS\nBEGIN\n  SET NOCOUNT ON;\n  SET XACT_ABORT ON;\n  DECLARE @now DATETIME2(7) = SYSUTCDATETIME(), @spent INT, @count INT;\n  IF DATALENGTH(@resident) <> 64 OR @resident COLLATE Latin1_General_100_BIN2 LIKE '%[^a-f0-9]%'\n    THROW 51000, 'Invalid accounting identity', 1;\n  BEGIN TRANSACTION;\n  SELECT @spent = reserved_cents FROM resident_ai.budget WITH (UPDLOCK, HOLDLOCK) WHERE id = 1;\n  SET @now = SYSUTCDATETIME();\n  SELECT @count = COUNT(*) FROM resident_ai.attempt\n    WHERE resident = @resident AND reserved_at > DATEADD(HOUR, -1, @now);\n  IF @spent IS NULL OR @spent >= 2000 OR @count >= 5\n     OR @now >= '2026-11-01T00:00:00'\n     OR EXISTS (SELECT 1 FROM resident_ai.attempt WHERE reservation = @reservation)\n  BEGIN\n    COMMIT;\n    SELECT CAST(0 AS INT) AS accepted;\n    RETURN;\n  END;\n  UPDATE resident_ai.budget SET reserved_cents = reserved_cents + 1 WHERE id = 1;\n  INSERT INTO resident_ai.attempt (reservation, resident, reserved_at)\n    VALUES (@reservation, @resident, @now);\n  COMMIT;\n  SELECT CAST(1 AS INT) AS accepted;\nEND;\nGO\nCREATE OR ALTER PROCEDURE resident_ai.complete\n  @reservation UNIQUEIDENTIFIER, @prompt INT, @completion INT\nAS\nBEGIN\n  SET NOCOUNT ON;\n  SET XACT_ABORT ON;\n  IF @prompt IS NULL OR @completion IS NULL OR @prompt NOT BETWEEN 0 AND 8192\n     OR @completion NOT BETWEEN 0 AND 256\n    THROW 51001, 'Invalid usage counts', 1;\n  UPDATE resident_ai.attempt SET prompt_tokens = @prompt, completion_tokens = @completion\n    WHERE reservation = @reservation AND prompt_tokens IS NULL AND completion_tokens IS NULL;\n  -- Duplicate completion cannot alter usage or release a reservation.\nEND;\nGO\nDENY SELECT, INSERT, UPDATE, DELETE, ALTER, REFERENCES ON SCHEMA::resident_ai TO [{{PRINCIPAL}}];\nGRANT EXECUTE ON OBJECT::resident_ai.reserve TO [{{PRINCIPAL}}];\nGRANT EXECUTE ON OBJECT::resident_ai.complete TO [{{PRINCIPAL}}];\n"
env=dict(os.environ,ZF_SQL_AUTH="msi")
c=mssql_python.connect(connection_string(env),autocommit=True); cur=c.cursor()
def q(s,a=()):
    cur.execute(s,a); return cur.fetchall() if cur.description else []
def state():
    return {"schema":q("SELECT SCHEMA_ID(N'resident_ai')")[0][0] is not None,
     "reserve":q("SELECT OBJECT_ID(N'resident_ai.reserve')")[0][0] is not None,
     "complete":q("SELECT OBJECT_ID(N'resident_ai.complete')")[0][0] is not None,
     "budget":q("SELECT OBJECT_ID(N'resident_ai.budget')")[0][0] is not None,
     "db":q("SELECT DB_NAME()")[0][0]}
print("before",json.dumps(state()),flush=True)
row=q("SELECT CONVERT(varchar(256), sid, 1) FROM sys.database_principals WHERE name=?",(P,))
sid="0x"+uuid.UUID(CID).bytes_le.hex()
ok=bool(row) and row[0][0].lower()==sid.lower()
print("principal_sid_match",ok,flush=True)
s=state()
if ok and not (s["reserve"] and s["complete"] and s["budget"]):
    for b in [b.strip() for b in re.split(r"^GO\s*$",SQL,flags=re.M)]:
        if b: cur.execute(b.replace("{{PRINCIPAL}}",P))
    print("applied",flush=True)
print("after",json.dumps(state()),flush=True)
if ok:
    r=q("SELECT reserved_cents FROM resident_ai.budget WHERE id=1")
    print("reserved_cents",r[0][0] if r else None,flush=True)
c.close()
