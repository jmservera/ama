-- Accounting only. No case facts, prompts, answers, tokens or credentials are stored.
IF SCHEMA_ID(N'resident_ai') IS NULL EXEC(N'CREATE SCHEMA resident_ai AUTHORIZATION dbo');
GO
IF OBJECT_ID(N'resident_ai.budget', N'U') IS NULL
BEGIN
CREATE TABLE resident_ai.budget (
  id INT NOT NULL PRIMARY KEY CHECK (id = 1),
  reserved_cents INT NOT NULL CHECK (reserved_cents BETWEEN 0 AND 2000)
);
  INSERT INTO resident_ai.budget VALUES (1, 0);
END;
GO
IF OBJECT_ID(N'resident_ai.attempt', N'U') IS NULL
CREATE TABLE resident_ai.attempt (
  reservation UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
  resident CHAR(64) COLLATE Latin1_General_100_BIN2 NOT NULL,
  reserved_at DATETIME2(7) NOT NULL,
  prompt_tokens INT NULL CHECK (prompt_tokens BETWEEN 0 AND 8192),
  completion_tokens INT NULL CHECK (completion_tokens BETWEEN 0 AND 256)
);
GO
CREATE OR ALTER PROCEDURE resident_ai.reserve
  @resident VARCHAR(64), @reservation UNIQUEIDENTIFIER
AS
BEGIN
  SET NOCOUNT ON;
  SET XACT_ABORT ON;
  DECLARE @now DATETIME2(7) = SYSUTCDATETIME(), @spent INT, @count INT;
  IF DATALENGTH(@resident) <> 64 OR @resident COLLATE Latin1_General_100_BIN2 LIKE '%[^a-f0-9]%'
    THROW 51000, 'Invalid accounting identity', 1;
  BEGIN TRANSACTION;
  SELECT @spent = reserved_cents FROM resident_ai.budget WITH (UPDLOCK, HOLDLOCK) WHERE id = 1;
  SET @now = SYSUTCDATETIME();
  SELECT @count = COUNT(*) FROM resident_ai.attempt
    WHERE resident = @resident AND reserved_at > DATEADD(HOUR, -1, @now);
  IF @spent IS NULL OR @spent >= 2000 OR @count >= 5
     OR @now >= '2026-11-01T00:00:00'
     OR EXISTS (SELECT 1 FROM resident_ai.attempt WHERE reservation = @reservation)
  BEGIN
    COMMIT;
    SELECT CAST(0 AS INT) AS accepted;
    RETURN;
  END;
  UPDATE resident_ai.budget SET reserved_cents = reserved_cents + 1 WHERE id = 1;
  INSERT INTO resident_ai.attempt (reservation, resident, reserved_at)
    VALUES (@reservation, @resident, @now);
  COMMIT;
  SELECT CAST(1 AS INT) AS accepted;
END;
GO
CREATE OR ALTER PROCEDURE resident_ai.complete
  @reservation UNIQUEIDENTIFIER, @prompt INT, @completion INT
AS
BEGIN
  SET NOCOUNT ON;
  SET XACT_ABORT ON;
  IF @prompt IS NULL OR @completion IS NULL OR @prompt NOT BETWEEN 0 AND 8192
     OR @completion NOT BETWEEN 0 AND 256
    THROW 51001, 'Invalid usage counts', 1;
  UPDATE resident_ai.attempt SET prompt_tokens = @prompt, completion_tokens = @completion
    WHERE reservation = @reservation AND prompt_tokens IS NULL AND completion_tokens IS NULL;
  -- Duplicate completion cannot alter usage or release a reservation.
END;
GO
DENY SELECT, INSERT, UPDATE, DELETE, ALTER, REFERENCES ON SCHEMA::resident_ai TO [{{PRINCIPAL}}];
GRANT EXECUTE ON OBJECT::resident_ai.reserve TO [{{PRINCIPAL}}];
GRANT EXECUTE ON OBJECT::resident_ai.complete TO [{{PRINCIPAL}}];
