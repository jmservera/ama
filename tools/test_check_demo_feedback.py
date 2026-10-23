"""Focused offline tests for tools/check-demo-feedback.py (Refs #350).

Fixtures are built with the real runtime builders (me_payload, navigation,
taskqueues.contract, ledger entries and verification). Nothing here touches
the network, credentials, private data or a real deployment.
"""

import ast
import contextlib
import copy
import importlib.util
import io
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from zava_forward.api.workbench import navigation
from zava_forward.core import ai_tasks, ledger, projection, ranking, taskqueues
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


def ledger_report(count):
    entries, prev = [], ledger.GENESIS
    for n in range(count):
        entry = ledger.make_entry(
            "coord@example.invalid",
            "log_contact",
            "ZF-1",
            f"outcome {n}",
            prev,
            at="2026-10-22T10:00:00",
        )
        entries.append(entry)
        prev = entry["hash"]
    return dict(status=200, body=ledger.verify_entries(entries))


def contact(outcome, channel="Phone"):
    return dict(
        at="2026-10-22T10:00",
        purpose="Update",
        channel=channel,
        direction="Outbound",
        outcome=outcome,
        note="",
        by="Test",
    )


def case_write(outcome="Left voicemail", restart=True):
    old = [contact("Earlier two"), contact("Earlier one")]
    new = [contact(outcome[:80])] + old
    return dict(
        synthetic=True,
        case_id="ZF-1",
        request=dict(outcome=outcome, note="", channel="Phone"),
        before=dict(status=200, body=dict(id="ZF-1", contacts=old)),
        write=dict(status=200, body=dict(id="ZF-1", contacts=copy.deepcopy(new))),
        after=dict(status=200, body=dict(id="ZF-1", contacts=copy.deepcopy(new))),
        audit_before=ledger_report(2),
        audit_after=ledger_report(3),
        restart_between_write_and_read=restart,
    )


def ai_record():
    item = dict(
        case_id="ZF-1",
        resident="R",
        address="A",
        stage="S",
        rank=1,
        reason="Because.",
        cites=["Stage: S"],
    )
    return dict(
        status=200,
        body=dict(
            id="r1",
            source="ai",
            model="synthetic-model",
            validated=True,
            mode="ai",
            status="Proposed",
            label=Store.REC_LABEL,
            fallback_reason=None,
            latency_ms=812,
            quarantine=None,
            release=dict(id="rel-1", version="1", digest="sha256:" + "cd" * 32),
            release_denied=False,
            epoch_current=True,
            items=[item],
        ),
    )


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
        old = [contact(f"Earlier {n}") for n in range(40)]
        new = [contact("Left voicemail")] + old[:39]
        case = case_write()
        case["before"]["body"]["contacts"] = old
        for name in ("write", "after"):
            case[name]["body"]["contacts"] = copy.deepcopy(new)
        self.assertEqual(self.status(case), "blocked")
        case["write"]["body"]["contacts"] = [contact("Left voicemail")] + copy.deepcopy(
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
    def blocked_reason(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            path.write_bytes(content)
            report = cdf.build_report(str(path), OPTIONS)
        self.assertEqual(report["overall"], "blocked")
        self.assertTrue(
            all(
                c["status"] == "blocked"
                for c in report["checks"]
                if c["id"] in cdf.CHECKS
            )
        )

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

    def test_non_standard_json_constants_are_blocked(self):
        for constant in ("NaN", "Infinity", "-Infinity"):
            raw = json.dumps(bundle()).replace(
                '"latency_ms": 812', f'"latency_ms": {constant}'
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


if __name__ == "__main__":
    unittest.main()
