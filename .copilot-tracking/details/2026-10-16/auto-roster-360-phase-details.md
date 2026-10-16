# Automatic roster phase details

Task auto-roster-360, Refs #360.

## P01-T01

Extend existing SQL candidate output with existing Contractor scope only.
Keep missing/invalid supplier a validation failure. Shared infra person contract
must preserve existing ConfRm/desk/wksp exclusions and add room/shared/service
naming checks. Versioned envelope carries seed without changing actual rows;
SQL and setup readers both support it and reject malformed versions.
Exact envelope: version 1, nonnegative integer seed, nonempty staff array.
Automatic eligibility additionally requires Graph mailboxSettings/userPurpose
equal `user`; unavailable classification fails closed with permission guidance,
never grants permissions. SQL candidate bound=true stops regeneration.

## P01-T02

Profile evidence must bind to selected app or managed environment. Require
development profile and demo/test/dev environment. Production or contradictory
profile metadata refuses before generation, including read-only previews.
Profile tag is zava-forward-deployment-profile on app/environment. Read only
deployment outputResources matching their exact IDs for fallback parameters;
missing deploymentProfile means production. Any applicable non-development
profile refuses even when demo/test or direct-ingress tags are present.
Admin is an eligible member whose UPN begins admin@ case-insensitively;
explicit UPN may resolve none/many. Reserve the first ProgrammeManager code.
Sort codes and people before seeded shuffle. No insufficient-user writes.
One roster confirmation; write atomically outside Git with expected prior
template check; existing valid file is reused regardless of later seed flags.
No ProgrammeManager code stops. Explicit or one interactive UPN must match one
eligible user, otherwise stop without another question. Deficit counts only
eligible non-admin members against remaining codes.

## P01-T03

Preserve early local malformed-roster validation, then discover/verify lock
status before generation; acquire mutation lock only after confirmed persistence.
SQL candidate lookup failure reports one shell-quoted setup command retaining
safe mode/profile/app/seed options on an authorized private-connected host,
never an administrator UPN. Admin input is collected privately on that host.
Existing final Entra verification precedes SQL --check, confirmation and
--apply --restart. Read-only missing rosters preview only and do not pass a
nonexistent roster to SQL.

## P02-T01

Mock Graph and SQL, no live setup. Cover exact-template vs malformed partial
input, wrong roles, duplicate codes/people, guest/disabled/resource rejection,
admin ambiguity, stable ordering, repeated seed, persistence, readonly no writes,
0700/0600, symlink refusal, profile conflict, SQL failure and continuation order.

## P02-T02

Audit each owner criterion with offline evidence and explicit unmet live
boundaries. Preserve historical pack observations; append dated continuation.
No issue checkbox mutation.

## P02-T03

One review after implementation/validation, findings routed honestly.
GitHub-resolved privacy-safe local email, required coauthor trailer, topic push
and PR with Refs #360 only.
