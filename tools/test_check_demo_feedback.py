"""Focused offline tests for tools/check-demo-feedback.py (Refs #350).

Fixtures are built with the real runtime builders (me_payload, navigation,
taskqueues.contract, ledger entries and verification). Nothing here touches
the network, credentials, private data or a real deployment.
"""

import ast
import contextlib
import copy
import functools
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from zava_forward.api.workbench import navigation
from zava_forward.core import ai_tasks, identity, ledger, projection, ranking, taskqueues
from zava_forward.core.store import Store

SCRIPT = Path(__file__).with_name("check-demo-feedback.py")
SPEC = importlib.util.spec_from_file_location("check_demo_feedback", SCRIPT)
cdf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cdf)

DIGEST = "sha256:" + "ab" * 32
REFERENCE = "server/zava-forward-api@" + DIGEST
STAFF = dict(
    name="Test Coordinator",
    email="coord@example.invalid",
    role="Retrofit Coordinator",
    code="C1",
)
CONTRACTOR_USER = dict(
    name="Test Contractor", role=projection.CONTRACTOR, contractor="CON-1"
)
OPTIONS = Namespace(
    expect_image_digest=DIGEST, expect_role=None, expect_programme_cases=980
)


def staff_me():
    body = projection.me_payload(
        STAFF,
        dict(mine=3, hazards=1, open=980),
        [dict(email=STAFF["email"], role=STAFF["role"])],
    )
    body.update(
        account=dict(
            name=STAFF["name"], email=STAFF["email"], provider="trusted-proxy"
        ),
        map=dict(
            tiles="https://tiles.example.invalid/{z}/{x}/{y}.png",
            attribution="Synthetic",
        ),
        navigation=navigation(STAFF),
        work_queues=taskqueues.contract(ranking.CURRENT),
    )
    return dict(status=200, body=json.loads(json.dumps(body)))


def contractor_me():
    body = projection.me_payload(CONTRACTOR_USER, {}, [])
    body.update(
        account=dict(name="Test Contractor", email="", provider="trusted-proxy"),
        map=dict(tiles="https://tiles.example.invalid", attribution="Synthetic"),
        navigation=navigation(CONTRACTOR_USER),
    )
    return dict(status=200, body=json.loads(json.dumps(body)))


def admin_me():
    user = identity.principal(
        "11111111-1111-4111-8111-111111111111",
        "22222222-2222-4222-8222-222222222222",
        identity.ADMIN_ROLE_NAME,
        name="Test Administrator",
        roles=(identity.ADMIN_ROLE_NAME,),
        app_admin=True,
    )
    body = projection.me_payload(user, {}, [])
    body.update(
        account=dict(name=user["name"], email="", provider="trusted-proxy"),
        map=dict(tiles=None, attribution=""),
        navigation=navigation(user),
        work_queues=taskqueues.contract(ranking.CURRENT),
    )
    return dict(status=200, body=json.loads(json.dumps(body)))


def handcrafted_contact(outcome, channel="Phone"):
    """Named handcrafted boundary constructor, used only where the constructed dataset cannot reach the state (the 40-contact cap)."""
    return dict(
        at="2026-10-22T10:00",
        purpose="Update",
        channel=channel,
        direction="Outbound",
        outcome=outcome,
        note="",
        by="Test",
    )


# Cached as immutable JSON text so no caller can mutate a shared baseline.
@functools.lru_cache(maxsize=None)
def _case_write_snapshot(outcome, note, prior):
    with tempfile.TemporaryDirectory() as directory:
        return json.dumps(
            RuntimeFixture(directory).case_write(outcome=outcome, note=note, prior=prior)
        )


@functools.lru_cache(maxsize=None)
def _ai_snapshot():
    with tempfile.TemporaryDirectory() as directory:
        return json.dumps(RuntimeFixture(directory).ai())


def runtime_case_write(outcome, note, prior):
    return json.loads(_case_write_snapshot(outcome, note, prior))


def runtime_ai_record():
    return json.loads(_ai_snapshot())


def case_write(outcome="Left voicemail", restart=True):
    """Runtime-produced baseline (two earlier contacts, then one write); restart=False only changes the declaration."""
    case = runtime_case_write(outcome, CALL_NOTE, ("Earlier one", "Earlier two"))
    case["restart_between_write_and_read"] = restart
    return case


def ai_record():
    return runtime_ai_record()


def programme(total=980):
    return dict(status=200, body=dict(items=[], total=total, limit=50, offset=0))


def bundle(**overrides):
    data = dict(
        schema_version=1,
        origin="synthetic-fixture",
        image=dict(reference=REFERENCE),
        me=staff_me(),
        programme=programme(),
        case_write=case_write(),
        ai=ai_record(),
    )
    data.update(overrides)
    return data


def report_for(data, options=OPTIONS):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "evidence.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return cdf.build_report(str(path), options)


def statuses(report):
    return {c["id"]: c["status"] for c in report["checks"]}


class CheckStates(unittest.TestCase):
    def test_valid_fixture_never_passes_sql_durability_and_overall_is_blocked(self):
        report = report_for(bundle())
        expected = {k: "pass" for k in cdf.CHECKS}
        expected["case_write_reload"] = "blocked"
        self.assertEqual(
            {k: v for k, v in statuses(report).items() if k in cdf.CHECKS}, expected
        )
        self.assertEqual(statuses(report)["spend_bound"], "not-run")
        self.assertEqual(statuses(report)["admin_account"], "not-run")
        self.assertEqual(report["overall"], "blocked")
        self.assertEqual(report["acceptance"], "not-accepted")

    def test_no_evidence_is_not_run_and_loads_no_runtime(self):
        def loader():
            raise AssertionError("runtime must not load without evidence")

        report = cdf.build_report(
            None,
            Namespace(
                expect_image_digest=None, expect_role=None, expect_programme_cases=980
            ),
            loader,
        )
        self.assertEqual(report["overall"], "not-run")
        self.assertTrue(all(c["status"] == "not-run" for c in report["checks"]))

    def test_expected_digest_without_image_is_blocked(self):
        report = cdf.build_report(None, OPTIONS)
        self.assertEqual(statuses(report)["image_identity"], "blocked")
        self.assertEqual(report["overall"], "blocked")

    def test_missing_slots_are_not_run(self):
        data = bundle()
        for key in ("me", "programme", "case_write", "ai"):
            data.pop(key)
        data.pop("image")
        status = statuses(
            report_for(
                data,
                Namespace(
                    expect_image_digest=None,
                    expect_role=None,
                    expect_programme_cases=980,
                ),
            )
        )
        self.assertTrue(all(status[c] == "not-run" for c in cdf.CHECKS))

    def test_report_is_deterministic(self):
        self.assertEqual(
            json.dumps(report_for(bundle()), sort_keys=True),
            json.dumps(report_for(bundle()), sort_keys=True),
        )


class ImageIdentity(unittest.TestCase):
    def status(self, reference, options=OPTIONS):
        return statuses(report_for(bundle(image=dict(reference=reference)), options))[
            "image_identity"
        ]

    def test_tag_fails(self):
        self.assertEqual(self.status("server/zava-forward-api:latest"), "fail")

    def test_digest_mismatch_fails(self):
        self.assertEqual(
            self.status("server/zava-forward-api@sha256:" + "00" * 32), "fail"
        )

    def test_digest_without_expected_value_is_blocked(self):
        self.assertEqual(
            self.status(
                REFERENCE,
                Namespace(
                    expect_image_digest=None,
                    expect_role=None,
                    expect_programme_cases=980,
                ),
            ),
            "blocked",
        )

    def test_malformed_expected_digest_is_blocked(self):
        self.assertEqual(
            self.status(
                REFERENCE,
                Namespace(
                    expect_image_digest="abc",
                    expect_role=None,
                    expect_programme_cases=980,
                ),
            ),
            "blocked",
        )


class MeContract(unittest.TestCase):
    def status(self, me, options=OPTIONS, origin="synthetic-fixture"):
        return statuses(report_for(bundle(me=me, origin=origin), options))[
            "me_contract"
        ]

    def test_denials_and_redirects_fail(self):
        for code in (301, 302, 401, 403, 500):
            with self.subTest(code=code):
                me = dict(status=code, body={})
                self.assertEqual(self.status(me), "fail")
        report = report_for(bundle(me=dict(status=302, body={})))
        reason = next(c["reason"] for c in report["checks"] if c["id"] == "me_contract")
        self.assertIn("not an authorized functional success", reason)

    def test_malformed_response_is_blocked(self):
        self.assertEqual(self.status(dict(body={})), "blocked")

    def test_runtime_admin_only_response_passes_without_acceptance(self):
        report = report_for(bundle(me=admin_me()))
        self.assertEqual(statuses(report)["me_contract"], "pass")
        self.assertEqual(report["overall"], "blocked")
        self.assertEqual(report["acceptance"], "not-accepted")
        self.assertEqual(statuses(report)["admin_account"], "not-run")

    def test_admin_payload_rejects_business_data_or_missing_flag(self):
        for mutate in (
            lambda b: b.update(counts=dict(mine=1, hazards=0, open=2)),
            lambda b: b.update(staff=[dict(email="a@example.invalid", role="x")]),
            lambda b: b["user"].update(app_admin=False),
            lambda b: b.pop("work_queues"),
        ):
            with self.subTest(mutate=mutate):
                me = admin_me()
                mutate(me["body"])
                self.assertEqual(self.status(me), "fail")

    def test_contractor_contract_passes(self):
        self.assertEqual(self.status(contractor_me()), "pass")

    def test_account_fields_reject_wrong_json_types(self):
        for make_me in (staff_me, contractor_me):
            for field in ("name", "email", "provider"):
                for value in (
                    None,
                    [],
                    ["text"],
                    {},
                    {"text": "value"},
                    False,
                    True,
                    0,
                    1.5,
                ):
                    with self.subTest(role=make_me.__name__, field=field, value=value):
                        me = make_me()
                        me["body"]["account"][field] = value
                        report = report_for(bundle(me=me))
                        check = next(
                            c for c in report["checks"] if c["id"] == "me_contract"
                        )
                        self.assertEqual(check["status"], "fail")
                        self.assertIn("account", check["reason"])
                        if field != "provider":
                            self.assertIn(field, check["reason"])

    def test_map_fields_reject_wrong_json_types(self):
        for make_me in (staff_me, contractor_me):
            for field in ("tiles", "attribution"):
                for value in (
                    None,
                    [],
                    ["text"],
                    {},
                    {"text": "value"},
                    False,
                    True,
                    0,
                    1.5,
                ):
                    if field == "tiles" and value is None:
                        continue
                    with self.subTest(role=make_me.__name__, field=field, value=value):
                        me = make_me()
                        me["body"]["map"][field] = value
                        report = report_for(bundle(me=me))
                        check = next(
                            c for c in report["checks"] if c["id"] == "me_contract"
                        )
                        self.assertEqual(check["status"], "fail")
                        self.assertIn("map", check["reason"])
                        self.assertIn(field, check["reason"])

    def test_string_fields_have_no_new_content_restrictions(self):
        for make_me in (staff_me, contractor_me):
            for section, field in (
                ("account", "name"),
                ("account", "email"),
                ("map", "tiles"),
                ("map", "attribution"),
            ):
                for value in ("", " ", "arbitrary text"):
                    with self.subTest(
                        role=make_me.__name__, section=section, field=field, value=value
                    ):
                        me = make_me()
                        me["body"][section][field] = value
                        report = report_for(bundle(me=me))
                        self.assertEqual(statuses(report)["me_contract"], "pass")
                        self.assertEqual(
                            statuses(report)["case_write_reload"], "blocked"
                        )
                        self.assertEqual(report["overall"], "blocked")
                        self.assertEqual(report["acceptance"], "not-accepted")

    def test_unconfigured_tiles_and_empty_attribution_pass(self):
        for make_me in (staff_me, contractor_me):
            with self.subTest(role=make_me.__name__):
                me = make_me()
                me["body"]["map"] = dict(tiles=None, attribution="")
                report = report_for(bundle(me=me))
                self.assertEqual(statuses(report)["me_contract"], "pass")
                self.assertEqual(statuses(report)["case_write_reload"], "blocked")
                self.assertEqual(report["overall"], "blocked")
                self.assertEqual(report["acceptance"], "not-accepted")

    def test_contractor_empty_account_email_passes(self):
        me = contractor_me()
        self.assertEqual(me["body"]["account"]["email"], "")
        self.assertEqual(self.status(me), "pass")

    def test_provider_content_checks_are_unchanged(self):
        for make_me in (staff_me, contractor_me):
            for provider in ("", " ", "password", "arbitrary text", "trusted-proxy"):
                for origin in ("synthetic-fixture", "deployed-capture"):
                    with self.subTest(
                        role=make_me.__name__, provider=provider, origin=origin
                    ):
                        me = make_me()
                        me["body"]["account"]["provider"] = provider
                        expected = (
                            "pass"
                            if provider.strip()
                            and (
                                origin == "synthetic-fixture"
                                or provider == "trusted-proxy"
                            )
                            else "fail"
                        )
                        self.assertEqual(self.status(me, origin=origin), expected)

    def test_contractor_with_staff_data_fails(self):
        me = contractor_me()
        me["body"]["staff"] = [
            dict(email="x@example.invalid", role="Retrofit Coordinator")
        ]
        self.assertEqual(self.status(me), "fail")

    def test_unknown_role_fails(self):
        me = staff_me()
        me["body"]["user"]["role"] = "Janitor"
        self.assertEqual(self.status(me), "fail")

    def test_expected_role_mismatch_fails(self):
        options = Namespace(
            expect_image_digest=DIGEST,
            expect_role="Resident Liaison Officer",
            expect_programme_cases=980,
        )
        self.assertEqual(self.status(staff_me(), options), "fail")

    def test_stale_work_queues_fail(self):
        me = staff_me()
        me["body"]["work_queues"]["version"] = "stale"
        self.assertEqual(self.status(me), "fail")

    def test_navigation_drift_fails(self):
        me = staff_me()
        me["body"]["navigation"] = me["body"]["navigation"][:-1]
        self.assertEqual(self.status(me), "fail")

    def test_missing_work_queues_and_extra_keys_fail(self):
        me = staff_me()
        del me["body"]["work_queues"]
        self.assertEqual(self.status(me), "fail")
        me = staff_me()
        me["body"]["extra"] = 1
        self.assertEqual(self.status(me), "fail")

    def test_deployed_capture_needs_trusted_proxy(self):
        me = staff_me()
        me["body"]["account"]["provider"] = "password"
        self.assertEqual(self.status(me, origin="deployed-capture"), "fail")
        self.assertEqual(self.status(staff_me(), origin="deployed-capture"), "pass")


class CaseWriteReload(unittest.TestCase):
    def status(self, case):
        return statuses(report_for(bundle(case_write=case)))["case_write_reload"]

    def test_consistent_write_reload_is_blocked_not_passed(self):
        self.assertEqual(self.status(case_write()), "blocked")
        report = report_for(bundle())
        reason = next(
            c["reason"] for c in report["checks"] if c["id"] == "case_write_reload"
        )
        self.assertIn("cannot be verified offline", reason)

    def test_mismatched_write_response_with_matching_reload_fails(self):
        case = case_write()
        case["write"]["body"]["contacts"][0]["outcome"] = "Different"
        case["after"]["body"]["contacts"][0]["outcome"] = "Different"
        self.assertEqual(self.status(case), "fail")
        case = case_write()
        case["write"]["body"]["contacts"][0]["channel"] = "Email"
        self.assertEqual(self.status(case), "fail")

    def test_write_response_differing_from_reload_in_any_field_fails(self):
        case = copy.deepcopy(case_write())
        case["after"]["body"]["contacts"][0]["by"] = "Someone else"
        self.assertEqual(self.status(case), "fail")

    def test_note_mismatch_with_matching_snapshots_fails(self):
        case = case_write()
        case["request"]["note"] = "Asked to call back"
        self.assertEqual(self.status(case), "fail")

    def test_matching_note_is_compared_and_truncated_like_runtime(self):
        case = case_write()
        case["request"]["note"] = "n" * 600
        for name in ("write", "after"):
            case[name]["body"]["contacts"][0]["note"] = "n" * 500
        self.assertEqual(self.status(case), "blocked")
        case["after"]["body"]["contacts"][0]["note"] = "n" * 600
        self.assertEqual(self.status(case), "fail")

    def test_existing_contacts_are_newest_first(self):
        case = case_write()
        self.assertEqual(
            case["write"]["body"]["contacts"][0]["outcome"], "Left voicemail"
        )
        self.assertEqual(self.status(case), "blocked")
        oldest_first = case_write()
        for name in ("write", "after"):
            oldest_first[name]["body"]["contacts"].reverse()
        self.assertEqual(self.status(oldest_first), "fail")

    def test_older_contacts_must_match_before_detail(self):
        case = case_write()
        case["write"]["body"]["contacts"][1]["outcome"] = "Altered"
        self.assertEqual(self.status(case), "fail")

    def test_capped_response_keeps_forty_newest(self):
        old = [handcrafted_contact(f"Earlier {n}") for n in range(40)]
        new = [handcrafted_contact("Left voicemail")] + old[:39]
        case = case_write()
        case["request"]["note"] = ""
        case["before"]["body"]["contacts"] = old
        for name in ("write", "after"):
            case[name]["body"]["contacts"] = copy.deepcopy(new)
        self.assertEqual(self.status(case), "blocked")
        case["write"]["body"]["contacts"] = [handcrafted_contact("Left voicemail")] + copy.deepcopy(
            old
        )
        self.assertEqual(self.status(case), "fail")

    def test_held_note_is_blocked(self):
        case = case_write()
        case["request"]["note"] = "x"
        for name in ("write", "after"):
            case[name]["body"]["contacts"][0]["note"] = projection.NOTE_HELD
        self.assertEqual(self.status(case), "blocked")

    def test_held_write_response_is_blocked(self):
        case = case_write()
        case["write"]["body"]["contacts"][0]["outcome"] = projection.NOTE_HELD
        self.assertEqual(self.status(case), "blocked")

    def test_long_outcome_matches_stored_truncation(self):
        self.assertEqual(self.status(case_write("x" * 120)), "blocked")
        case = case_write("x" * 120)
        case["after"]["body"]["contacts"][0]["outcome"] = "x" * 120
        case["write"]["body"]["contacts"][0]["outcome"] = "x" * 120
        self.assertEqual(self.status(case), "fail")

    def test_missing_restart_is_blocked(self):
        self.assertEqual(self.status(case_write(restart=False)), "blocked")

    def test_non_synthetic_is_blocked(self):
        case = case_write()
        case["synthetic"] = False
        self.assertEqual(self.status(case), "blocked")

    def test_held_outcome_is_blocked(self):
        case = case_write()
        case["after"]["body"]["contacts"][0]["outcome"] = projection.NOTE_HELD
        self.assertEqual(self.status(case), "blocked")

    def test_lost_write_fails(self):
        case = case_write()
        case["after"]["body"]["contacts"] = case["before"]["body"]["contacts"]
        self.assertEqual(self.status(case), "fail")

    def test_wrong_outcome_fails(self):
        case = case_write()
        case["after"]["body"]["contacts"][0]["outcome"] = "Different"
        self.assertEqual(self.status(case), "fail")

    def test_denied_write_fails(self):
        for code in (302, 403):
            case = case_write()
            case["write"]["status"] = code
            self.assertEqual(self.status(case), "fail")

    def test_unchanged_ledger_head_fails(self):
        case = case_write()
        case["audit_after"] = copy.deepcopy(case["audit_before"])
        self.assertEqual(self.status(case), "fail")

    def test_broken_ledger_fails(self):
        case = case_write()
        case["audit_after"]["body"]["intact"] = False
        self.assertEqual(self.status(case), "fail")


class AiEvidence(unittest.TestCase):
    def status(self, record):
        return statuses(report_for(bundle(ai=record)))["ai_evidence"]

    def test_runtime_shaped_capture_passes(self):
        self.assertEqual(self.status(ai_record()), "pass")

    def test_duplicate_case_ids_fail(self):
        item = ai_record()["body"]["items"][0]
        other = dict(item, case_id="ZF-2")
        repeated = dict(item, reason="Another reason.", cites=["Stage: T"])
        for origin in cdf.ORIGINS:
            for items in (
                [item, copy.deepcopy(item)],
                [item, repeated],
                [item, other, repeated],
            ):
                with self.subTest(origin=origin, items=items):
                    record = ai_record()
                    record["body"]["items"] = items
                    report = report_for(bundle(ai=record, origin=origin))
                    check = next(
                        c for c in report["checks"] if c["id"] == "ai_evidence"
                    )
                    self.assertEqual(check["status"], "fail")
                    self.assertIn("duplicate case IDs", check["reason"])
                    self.assertEqual(report["acceptance"], "not-accepted")

    def test_distinct_case_ids_preserve_offline_boundaries(self):
        item = ai_record()["body"]["items"][0]
        for origin in cdf.ORIGINS:
            for case_ids in (
                ("ZF-1", "ZF-2"),
                ("ZF-1", "zf-1"),
                ("ZF-1", " ZF-1 "),
            ):
                with self.subTest(origin=origin, case_ids=case_ids):
                    record = ai_record()
                    record["body"]["items"] = [
                        dict(item, case_id=case_id) for case_id in case_ids
                    ]
                    report = report_for(bundle(ai=record, origin=origin))
                    self.assertEqual(statuses(report)["ai_evidence"], "pass")
                    self.assertEqual(statuses(report)["case_write_reload"], "blocked")
                    self.assertEqual(statuses(report)["spend_bound"], "not-run")
                    self.assertEqual(statuses(report)["admin_account"], "not-run")
                    self.assertEqual(report["overall"], "blocked")
                    self.assertEqual(report["acceptance"], "not-accepted")

    def test_missing_item_fields_fail(self):
        for field in ("case_id", "reason", "cites"):
            with self.subTest(field=field):
                record = ai_record()
                del record["body"]["items"][0][field]
                self.assertEqual(self.status(record), "fail")

    def test_item_text_fields_require_nonempty_strings(self):
        for field in ("case_id", "reason"):
            for value in (None, False, True, 0, 1.5, [], ["text"], {}, "", " \t\n"):
                with self.subTest(field=field, value=value):
                    record = ai_record()
                    record["body"]["items"][0][field] = value
                    report = report_for(bundle(ai=record))
                    check = next(
                        c for c in report["checks"] if c["id"] == "ai_evidence"
                    )
                    self.assertEqual(check["status"], "fail")
                    self.assertIn("cited items", check["reason"])
                    self.assertEqual(report["acceptance"], "not-accepted")

    def test_citations_require_nonempty_list_of_nonempty_strings(self):
        invalid = (None, False, True, 0, 1.5, {}, [], "", " \t\n")
        for cites in (
            "Stage: S",
            *invalid,
            *([value] for value in invalid),
            *(["Stage: S", value] for value in invalid),
        ):
            with self.subTest(cites=cites):
                record = ai_record()
                record["body"]["items"][0]["cites"] = cites
                self.assertEqual(self.status(record), "fail")

    def test_items_require_nonempty_list_of_valid_objects(self):
        valid = ai_record()["body"]["items"][0]
        malformed = dict(valid, reason=False)
        for items in (
            None,
            {},
            [],
            [None],
            ["item"],
            [valid, None],
            [valid, malformed],
            [malformed, valid],
        ):
            with self.subTest(items=items):
                record = ai_record()
                record["body"]["items"] = items
                self.assertEqual(self.status(record), "fail")

    def test_reproduced_malformed_captures_fail(self):
        for items in (
            [{"cites": [{}]}],
            [{"case_id": None, "reason": False, "cites": ["Stage: S"]}],
        ):
            with self.subTest(items=items):
                record = ai_record()
                record["body"]["items"] = items
                self.assertEqual(self.status(record), "fail")

    def test_runtime_validated_items_retain_offline_acceptance_boundaries(self):
        proposed = [
            dict(case_id="ZF-1", reason=" Because. ", cites=["Stage: S"]),
            dict(case_id="ZF-2", reason="Another reason.", cites=["Stage: T"]),
        ]
        items, dropped, error = ai_tasks.priority_items(
            json.dumps(proposed),
            2,
            {"ZF-1": ["Stage: S"], "ZF-2": ["Stage: T"]},
        )
        self.assertIsNone(error)
        self.assertEqual(dropped, 0)
        self.assertEqual(items[0]["reason"], "Because.")
        record = ai_record()
        record["body"]["items"] = items
        report = report_for(bundle(ai=record))
        self.assertEqual(statuses(report)["ai_evidence"], "pass")
        self.assertEqual(statuses(report)["case_write_reload"], "blocked")
        self.assertEqual(statuses(report)["spend_bound"], "not-run")
        self.assertEqual(statuses(report)["admin_account"], "not-run")
        self.assertEqual(report["overall"], "blocked")
        self.assertEqual(report["acceptance"], "not-accepted")

    def test_template_fails(self):
        record = ai_record()
        record["body"].update(
            source="template", fallback_reason="No model available", model="template"
        )
        self.assertEqual(self.status(record), "fail")

    def test_mode_ai_alone_does_not_prove_ai(self):
        record = ai_record()
        record["body"]["source"] = "template"
        self.assertEqual(self.status(record), "fail")

    def test_workflow_only_fails(self):
        record = ai_record()
        record["body"]["mode"] = "workflow-only"
        self.assertEqual(self.status(record), "fail")

    def test_get_wrapper_and_null_fail(self):
        self.assertEqual(
            self.status(
                dict(status=200, body=dict(recommendation=ai_record()["body"]))
            ),
            "fail",
        )
        self.assertEqual(
            self.status(dict(status=200, body=dict(recommendation=None))), "fail"
        )

    def test_uncited_quarantined_or_denied_fail(self):
        for field, value in (
            ("items", [dict(case_id="ZF-1", reason="Because.", cites=[])]),
            ("quarantine", dict(reason="late")),
            ("release_denied", True),
            ("epoch_current", False),
            ("label", "Approved"),
            ("validated", False),
        ):
            record = ai_record()
            record["body"][field] = value
            with self.subTest(field=field):
                self.assertEqual(self.status(record), "fail")

    def test_negative_or_non_numeric_latency_fails(self):
        for value in (-1, True, "812", 10**400 * -1):
            record = ai_record()
            record["body"]["latency_ms"] = value
            with self.subTest(value=value):
                self.assertEqual(self.status(record), "fail")

    def test_huge_integer_latency_is_accepted_without_crashing(self):
        record = ai_record()
        record["body"]["latency_ms"] = 10**400
        self.assertEqual(self.status(record), "pass")

    def test_in_memory_non_finite_latency_fails(self):
        for value in (float("nan"), float("inf")):
            record = ai_record()
            record["body"]["latency_ms"] = value
            with self.assertRaises(cdf.Verdict) as caught:
                cdf.check_ai({"ai": record}, cdf.load_runtime())
            self.assertEqual(caught.exception.status, "fail")

    def test_denial_is_not_ai_success(self):
        self.assertEqual(self.status(dict(status=403, body={})), "fail")


class BaselineDistinction(unittest.TestCase):
    def status(self, page):
        return statuses(report_for(bundle(programme=page)))["baseline_distinction"]

    def test_expected_programme_passes(self):
        self.assertEqual(self.status(programme(980)), "pass")

    def test_stock_homes_are_not_cases(self):
        self.assertEqual(self.status(programme(60000)), "fail")

    def test_other_total_fails(self):
        self.assertEqual(self.status(programme(979)), "fail")

    def test_denied_page_fails(self):
        self.assertEqual(self.status(dict(status=401, body={})), "fail")


class InputSafety(unittest.TestCase):
    def blocked_reason(self, content, expected_reason=None):
        def loader():
            raise AssertionError("runtime must not load for invalid evidence")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_bytes(content)
            report = cdf.build_report(str(path), OPTIONS, loader)
        self.assertEqual(report["overall"], "blocked")
        self.assertTrue(report["offline_only"])
        self.assertEqual(report["acceptance"], "not-accepted")
        for name in cdf.GAPS:
            self.assertEqual(statuses(report)[name], "not-run")
        self.assertTrue(
            all(
                c["status"] == "blocked"
                for c in report["checks"]
                if c["id"] in cdf.CHECKS
            )
        )
        if expected_reason is not None:
            for check in report["checks"]:
                if check["id"] in cdf.CHECKS:
                    self.assertIn(expected_reason, check["reason"])

    def test_exponent_overflow_is_blocked_before_runtime(self):
        for token in ("1e999", "-1e999", "1.0e999"):
            for location in ("latency", "rank", "nested_extra"):
                with self.subTest(token=token, location=location):
                    data = bundle()
                    if location == "latency":
                        data["ai"]["body"]["latency_ms"] = "NUMBER_TOKEN"
                    elif location == "rank":
                        data["ai"]["body"]["items"][0]["rank"] = "NUMBER_TOKEN"
                    else:
                        data["programme"]["body"]["extra"] = [{"value": "NUMBER_TOKEN"}]
                    raw = json.dumps(data)
                    self.assertEqual(raw.count('"NUMBER_TOKEN"'), 1)
                    raw = raw.replace('"NUMBER_TOKEN"', token)
                    self.blocked_reason(
                        raw.encode(), "Evidence file is not valid JSON: non-finite"
                    )

    def test_schema_version_requires_supported_integer_type(self):
        for value in (True, False, 1.0, 2):
            with self.subTest(value=value):
                self.blocked_reason(
                    json.dumps(bundle(schema_version=value)).encode(),
                    "schema_version must be integer 1",
                )

    def test_supported_integer_schema_preserves_offline_boundaries(self):
        report = report_for(bundle(schema_version=1))
        self.assertEqual(statuses(report)["ai_evidence"], "pass")
        self.assertEqual(statuses(report)["case_write_reload"], "blocked")
        for name in cdf.GAPS:
            self.assertEqual(statuses(report)[name], "not-run")
        self.assertEqual(report["overall"], "blocked")
        self.assertTrue(report["offline_only"])
        self.assertEqual(report["acceptance"], "not-accepted")

    def test_finite_float_tokens_preserve_field_scope(self):
        for token in ("1.25", "1e308", "1e-999", "-1.25"):
            for field in ("rank", "latency_ms"):
                with self.subTest(token=token, field=field):
                    data = bundle()
                    target = data["ai"]["body"]
                    if field == "rank":
                        target = target["items"][0]
                    target[field] = "NUMBER_TOKEN"
                    raw = json.dumps(data)
                    self.assertEqual(raw.count('"NUMBER_TOKEN"'), 1)
                    raw = raw.replace('"NUMBER_TOKEN"', token)
                    with tempfile.TemporaryDirectory() as directory:
                        path = Path(directory) / "evidence.json"
                        path.write_text(raw, encoding="utf-8")
                        decoded = cdf.load_evidence(path)
                        decoded_target = decoded["ai"]["body"]
                        if field == "rank":
                            decoded_target = decoded_target["items"][0]
                        self.assertIs(type(decoded_target[field]), float)
                        self.assertEqual(decoded_target[field], float(token))
                        report = cdf.build_report(str(path), OPTIONS)
                    expected = (
                        "fail" if field == "latency_ms" and token == "-1.25" else "pass"
                    )
                    self.assertEqual(statuses(report)["ai_evidence"], expected)
                    self.assertEqual(statuses(report)["case_write_reload"], "blocked")
                    self.assertEqual(
                        report["overall"], "fail" if expected == "fail" else "blocked"
                    )
                    self.assertEqual(report["acceptance"], "not-accepted")

    def test_numeric_strings_keep_existing_field_rules(self):
        for field in ("rank", "latency_ms"):
            with self.subTest(field=field):
                data = bundle()
                target = data["ai"]["body"]
                if field == "rank":
                    target = target["items"][0]
                target[field] = "1e999"
                report = report_for(data)
                self.assertEqual(
                    statuses(report)["ai_evidence"],
                    "pass" if field == "rank" else "fail",
                )
                self.assertEqual(report["acceptance"], "not-accepted")

    def test_bad_inputs_are_blocked(self):
        for content in (
            b"{",
            b"[]",
            b"\xff\xfe",
            json.dumps(bundle(origin="live")).encode(),
            json.dumps(dict(schema_version=2)).encode(),
            json.dumps(bundle(extra=1)).encode(),
            b" " * (cdf.MAX_EVIDENCE_BYTES + 1),
        ):
            with self.subTest(content=content[:12]):
                self.blocked_reason(content)

    def test_excessive_json_nesting_is_blocked_not_raised(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text("[" * 10000 + "]" * 10000, encoding="utf-8")
            report = cdf.build_report(str(path), OPTIONS)
        self.assertEqual(report["overall"], "blocked")
        self.assertIn("nesting", json.dumps(report))

    def test_non_standard_json_constants_are_blocked(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            latency = ai_record()["body"]["latency_ms"]
            raw = json.dumps(bundle()).replace(
                f'"latency_ms": {json.dumps(latency)}', f'"latency_ms": {constant}'
            )
            self.assertIn(constant, raw)
            with self.subTest(constant=constant):
                self.blocked_reason(raw.encode())

    def test_missing_file_is_blocked(self):
        report = cdf.build_report("/nonexistent/evidence.json", OPTIONS)
        self.assertEqual(report["overall"], "blocked")

    def test_missing_runtime_is_blocked_not_passed(self):
        def loader():
            raise cdf.Verdict(cdf.BLOCKED, "packages missing")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_text(json.dumps(bundle()), encoding="utf-8")
            report = cdf.build_report(str(path), OPTIONS, loader)
        self.assertEqual(statuses(report)["me_contract"], "blocked")

    def test_source_has_no_broad_handlers_network_or_environment(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                self.assertIsNotNone(node.type)
                names = [n.id for n in ast.walk(node.type) if isinstance(n, ast.Name)]
                self.assertFalse({"Exception", "BaseException"} & set(names))
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                modules = [a.name for a in node.names] + [
                    getattr(node, "module", None) or ""
                ]
                for module in modules:
                    self.assertNotIn(
                        module.split(".")[0],
                        {"socket", "http", "urllib", "requests", "subprocess", "os"},
                    )


class CommandLine(unittest.TestCase):
    def run_main(self, argv):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = cdf.main(argv)
        return code, buffer.getvalue()

    def test_exit_codes_and_formats(self):
        code, out = self.run_main([])
        self.assertEqual(code, 3)
        self.assertEqual(json.loads(out)["overall"], "not-run")
        code, out = self.run_main(["--format", "text"])
        self.assertEqual(code, 3)
        self.assertIn("overall: not-run", out)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "e.json"
            path.write_text(
                json.dumps(bundle(me=dict(status=403, body={}))), encoding="utf-8"
            )
            code, _ = self.run_main(
                ["--evidence", str(path), "--expect-image-digest", DIGEST]
            )
            self.assertEqual(code, 1)
            path.write_text(json.dumps(bundle()), encoding="utf-8")
            code, out = self.run_main(
                ["--evidence", str(path), "--expect-image-digest", DIGEST]
            )
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(out)["acceptance"], "not-accepted")


CORE_TESTS = Path(__file__).resolve().parents[1] / "src" / "core" / "tests"
HAZARD_CITE = "Open safety issues: 1"
CALL_NOTE = "Synthetic runtime note"
CALL_OUTCOME = "Left voicemail"


def core_helpers():
    """Load the repository's constructed dataset and offline release helper, bound to this checkout."""
    if str(CORE_TESTS) not in sys.path:
        sys.path.insert(0, str(CORE_TESTS))
    import dataset
    import release_support

    for module in (dataset, release_support):
        if Path(module.__file__).resolve().parent != CORE_TESTS.resolve():
            raise AssertionError(f"{module.__name__} resolved outside {CORE_TESTS}: {module.__file__}")
    return dataset, release_support


def ok(body):
    return dict(status=200, body=json.loads(json.dumps(body)))


class RuntimeFixture:
    """Evidence produced by the real Store methods behind the server routes, with only the AI boundary scripted."""

    def __init__(self, directory, ai_items=None):
        dataset, release_support = core_helpers()
        self.directory = Path(directory)
        data_path = self.directory / "zavaforward.json"
        data_path.write_text(json.dumps(dataset.DATA), encoding="utf-8")
        self.paths = (
            str(data_path),
            str(self.directory / "live.json"),
            str(self.directory / "audit.jsonl"),
        )
        self.store = Store(*self.paths)
        self.user = dataset.DATA["staff"][0]
        self.store.ai.endpoint = "http://scripted-model.invalid"
        self.items = ai_items or [
            dict(case_id="ZF-4", reason="Open damp hazard.", cites=[HAZARD_CITE])
        ]
        self.store.ai._chat = lambda *a, **k: json.dumps(self.items)
        release_support.install(self.store)

    def case_write(self, case_id="ZF-1", outcome=CALL_OUTCOME, note=CALL_NOTE, channel="Phone", prior=()):
        store = self.store
        for earlier in prior:
            store.log_call(self.user, case_id, earlier, "", "Phone")
        before = ok(store.detail(case_id, self.user))
        audit_before = ok(store.verify_ledger())
        store.log_call(self.user, case_id, outcome, note, channel)
        write = ok(store.detail(case_id, self.user))
        audit_after = ok(store.verify_ledger())
        reloaded = Store(*self.paths)
        return dict(
            synthetic=True,
            case_id=case_id,
            request=dict(outcome=outcome, note=note, channel=channel),
            before=before,
            write=write,
            after=ok(reloaded.detail(case_id, self.user)),
            audit_before=audit_before,
            audit_after=audit_after,
            restart_between_write_and_read=True,
        )

    def ai(self):
        return ok(self.store.ai_priority(self.user, 1))


class RuntimeProducedEvidence(unittest.TestCase):
    def test_default_bundle_sections_are_copies_of_runtime_returns(self):
        captured = {}
        real_case, real_ai = RuntimeFixture.case_write, RuntimeFixture.ai

        def spy_case(self, *args, **kwargs):
            captured["case_write"] = real_case(self, *args, **kwargs)
            return captured["case_write"]

        def spy_ai(self):
            captured["ai"] = real_ai(self)
            return captured["ai"]

        _case_write_snapshot.cache_clear()
        _ai_snapshot.cache_clear()
        self.addCleanup(_case_write_snapshot.cache_clear)
        self.addCleanup(_ai_snapshot.cache_clear)
        RuntimeFixture.case_write, RuntimeFixture.ai = spy_case, spy_ai
        self.addCleanup(setattr, RuntimeFixture, "case_write", real_case)
        self.addCleanup(setattr, RuntimeFixture, "ai", real_ai)
        data = bundle()
        self.assertEqual(sorted(captured), ["ai", "case_write"])
        for key in ("case_write", "ai"):
            self.assertEqual(data[key], captured[key])
            self.assertIsNot(data[key], captured[key])
        self.assertEqual(len(data["case_write"]["write"]["body"]["contacts"]), 3)
        self.assertEqual(data["ai"]["body"]["release"]["id"], "offline-output-test:priority")

    def test_default_fixtures_are_isolated_copies(self):
        first, second = case_write(), case_write()
        first["write"]["body"]["contacts"][0]["outcome"] = "Changed"
        self.assertEqual(second["write"]["body"]["contacts"][0]["outcome"], CALL_OUTCOME)
        ai_record()["body"]["items"].clear()
        self.assertTrue(ai_record()["body"]["items"])

    def test_long_outcome_is_truncated_by_the_runtime_not_the_fixture(self):
        written = case_write("x" * 120)["write"]["body"]["contacts"][0]
        self.assertEqual(written["outcome"], "x" * 80)

    def build(self, **kwargs):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return RuntimeFixture(directory.name, **kwargs)

    def test_runtime_contact_and_ai_evidence_pass_the_unchanged_checker(self):
        fixture = self.build()
        ai = fixture.ai()
        body = ai["body"]
        self.assertEqual(body["source"], "ai")
        self.assertIs(body["validated"], True)
        self.assertIsNone(body.get("fallback_reason"))
        self.assertIs(body["release_denied"], False)
        self.assertEqual(body["release"]["id"], "offline-output-test:priority")
        self.assertEqual(body["release"]["version"], "scripted-output-v1")
        report = report_for(bundle(case_write=fixture.case_write(), ai=ai))
        states = statuses(report)
        self.assertEqual(states["case_write_reload"], "blocked", report)
        reason = next(c["reason"] for c in report["checks"] if c["id"] == "case_write_reload")
        self.assertIn("response-shape consistent", reason)
        self.assertEqual(states["ai_evidence"], "pass", report)
        self.assertEqual(report["overall"], "blocked")
        self.assertEqual(report["acceptance"], "not-accepted")

    def test_runtime_contact_is_newest_first_and_survives_reload(self):
        evidence = self.build().case_write()
        newest = evidence["after"]["body"]["contacts"][0]
        self.assertEqual(newest["outcome"], CALL_OUTCOME)
        self.assertEqual(newest["note"], CALL_NOTE)
        self.assertEqual(
            evidence["after"]["body"]["contacts"], evidence["write"]["body"]["contacts"]
        )
        self.assertEqual(
            len(evidence["write"]["body"]["contacts"]),
            len(evidence["before"]["body"]["contacts"]) + 1,
        )

    def test_runtime_contact_mutations_fail_closed(self):
        fixture = self.build()
        ai = fixture.ai()
        evidence = fixture.case_write()
        dropped = copy.deepcopy(evidence)
        dropped["after"]["body"]["contacts"] = dropped["before"]["body"]["contacts"]
        changed = copy.deepcopy(evidence)
        changed["request"]["outcome"] = "Different outcome"
        broken = copy.deepcopy(evidence)
        broken["audit_after"]["body"]["intact"] = False
        for name, mutated in (("dropped", dropped), ("changed", changed), ("broken", broken)):
            with self.subTest(name):
                report = report_for(bundle(case_write=mutated, ai=ai))
                self.assertEqual(statuses(report)["case_write_reload"], "fail", report)

    def test_runtime_template_fallbacks_are_rejected_by_the_checker(self):
        scripts = {
            "unresolved citation": [
                dict(case_id="ZF-4", reason="Open damp hazard.", cites=["Invented source: 9"])
            ],
            "hazard case omitted": [
                dict(case_id="ZF-1", reason="Routine.", cites=["Stage: Survey"])
            ],
        }
        for name, items in scripts.items():
            with self.subTest(name):
                fixture = self.build(ai_items=items)
                ai = fixture.ai()
                self.assertNotEqual(ai["body"]["source"], "ai")
                report = report_for(bundle(case_write=fixture.case_write(), ai=ai))
                self.assertEqual(statuses(report)["ai_evidence"], "fail", report)

    def test_runtime_ai_mutations_fail_closed(self):
        fixture = self.build()
        ai = fixture.ai()
        for name, change in (
            ("no cites", lambda b: b["items"][0].update(cites=[])),
            ("wrong label", lambda b: b.update(label="Approved")),
            ("denied release", lambda b: b.update(release_denied=True)),
        ):
            with self.subTest(name):
                mutated = copy.deepcopy(ai)
                change(mutated["body"])
                report = report_for(bundle(case_write=fixture.case_write(), ai=mutated))
                self.assertEqual(statuses(report)["ai_evidence"], "fail", report)


if __name__ == "__main__":
    unittest.main()
