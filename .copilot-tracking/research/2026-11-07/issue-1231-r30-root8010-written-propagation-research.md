# Issue 1231 r30 root 8010a486 written/typed-runner propagation: research

Date: 2026-11-07. Same session b353a2c9. Historical r29 (d99e/61f3/f0af, FULL receipt 799026a3) is preserved and not edited; it is not current evidence for this change.

## Identities (refetched before any action)

* Child 61f3ebe1a841d2b109acbe0849990ad17b187872 / tree 3914c42a1793e24ad8d639f237a9dec9131be91c, ignored-clean, PR #1242 base feat/ranking-publication-runner-79.
* Root 8010a4867ef4db5df355531f5a8c1839f19ac7b2 / tree 41636ccda74271ec90547248858d3fe5e66bce1c, ignored-clean. d99e6901 is its ancestor. Main f0afa8d7 unchanged.

## Root delta d99e6901..8010a486 (read in full)

* Root R28 (4a88793f): existing-record/EEXIST loser reconfirms the directory; runner maps DurabilityUnconfirmedError to status committed_unconfirmed, exit 2, instead of publish_failed.
* Root R29 (8010a486): DurabilityUnconfirmedError gains optional written (None = unknown); _confirmed passes outcome["written"]; runner reports e.written. Four new core tests, README, log append, RPI records. Author-only, no independent or FULL result on 8010.
* Independent findings answered: root d99 High (missing reconfirmation for existing/EEXIST) and combined-child Medium (runner generic OSError no-write refusal for an already-linked unconfirmed record).

## Child state

* Helper already syncs the folder for existing records and EEXIST losers through _confirmed (r26). Missing here: written on the error, the runner handler, the exit-2 mapping, README wording.
* Runner currently turns every OSError, including the typed error, into publish_failed (the Medium finding applies to the child too).
* Child stages are .NAME.<hex>.tmp (O_EXCL 0600); _remove nonthrowing; stage_retained path-free. Root helper uses .publishing- and must not replace these.

## Conclusion

A bounded propagation: add the optional written field and pass it through _confirmed, add the runner handler and exit code, adopt README text and tests adapted to the child's stage prefix. No Store, schema, auth, API production change expected: the Store already audits the typed error and API returns path-free 409. Planning readiness: Ready. No material design gap; no owner decision needed.

## Limits

#1258/#1259 untouched. Cross-UID permissions, real unsupported mount, real directory-sync fault unproven. Only light checks planned; FULL is a separate later admission.
