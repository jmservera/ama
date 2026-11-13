"""Held-out token runner: fail-closed authorization, cost cap and spread (#432, #435)."""

from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any

from heldout_freeze_fixture import manifest
from zava_forward.agents import heldout_batch as hb

NOW = datetime(2026, 11, 13, 12, 0, tzinfo=UTC)
DRY = "dry-run simulation - not measured evidence"
LIVE = "measured held-out batch"


def auth(**over: Any) -> dict[str, Any]:
    a: dict[str, Any] = dict(
        approved_by="owner",
        authority_ref="slide22_plus_qa_authorize_5usd_batch",
        expires_utc=(NOW + timedelta(days=1)).isoformat(),
        max_calls=10,
        max_total_tokens=100_000,
        max_budget_usd="5.00",
        currency="USD",
        model="m-1",
        input_usd_per_1m="2.00",
        output_usd_per_1m="8.00",
        max_prompt_tokens=1000,
        max_completion_tokens=500,
    )
    a.update(over)
    return a


def proposals(n: int = 4, text: str = "hello world") -> list[dict[str, str]]:
    return [dict(id=f"h{i}", prompt=text) for i in range(1, n + 1)]


class Spy:
    def __init__(self, prompt: int = 100, completion: int = 50, cached: int | None = None) -> None:
        self.calls: list[tuple[str, str, int, int]] = []
        self.usage: dict[str, Any] = dict(
            prompt_tokens=prompt, completion_tokens=completion, total_tokens=prompt + completion
        )
        if cached is not None:
            self.usage["cached_tokens"] = cached

    def __call__(self, system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
        self.calls.append((system, prompt, max_tokens, timeout))
        return dict(outcome="returned", text="x", usage=dict(self.usage))


def run(
    spy: Any,
    a: dict[str, Any] | None = None,
    props: list[dict[str, str]] | None = None,
    mode: str = "live",
    m: dict[str, Any] | None = None,
    provider_model: str | None = "m-1",
) -> dict[str, Any]:
    return hb.run_batch(
        auth() if a is None else a,
        manifest() if m is None else m,
        proposals() if props is None else props,
        spy,
        mode=mode,
        provider_model=provider_model,
        now=NOW,
    )


class RefusalTests(unittest.TestCase):
    def refused(self, a: dict[str, Any], **kw: Any) -> dict[str, Any]:
        spy = Spy()
        report = run(spy, a, **kw)
        self.assertEqual(report["outcome"], "refused")
        self.assertEqual(spy.calls, [])
        self.assertEqual(report["calls"], 0)
        return report

    def test_each_required_field_is_needed(self) -> None:
        for key in auth():
            a = auth()
            del a[key]
            self.refused(a)

    def test_budget_above_hard_cap_or_non_positive(self) -> None:
        for value in ("5.01", "0", "-1", "nan", True, "abc"):
            self.refused(auth(max_budget_usd=value))
        self.assertEqual(run(Spy(), auth(max_budget_usd="5.00"))["outcome"], "completed")

    def test_calls_bounds_and_currency_and_expiry(self) -> None:
        self.refused(auth(max_calls=51))
        self.refused(auth(max_calls=0))
        self.refused(auth(max_calls=True))
        self.refused(auth(max_total_tokens=0))
        self.refused(auth(currency="GBP"))
        self.refused(auth(expires_utc=(NOW - timedelta(seconds=1)).isoformat()))
        self.refused(auth(expires_utc="2099-01-01T00:00:00"))
        self.refused(auth(expires_utc="not a date"))

    def test_rates_must_be_valid(self) -> None:
        self.refused(auth(input_usd_per_1m="0"))
        self.refused(auth(output_usd_per_1m="-1"))
        self.refused(auth(cached_input_usd_per_1m="-0.1"))
        self.refused(auth(approved_by="  "))

    def test_unfrozen_or_empty_manifest_refuses(self) -> None:
        self.assertIn("not frozen", " ".join(self.refused(auth(), m={})["problems"]))
        broken = manifest()
        del broken["versions"]["prompt"]
        self.refused(auth(), m=broken)

    def test_empty_unknown_or_duplicate_proposals_refuse(self) -> None:
        self.refused(auth(), props=[])
        self.refused(auth(), props=[dict(id="zz", prompt="x")])
        self.refused(auth(), props=[dict(id="h1", prompt="x"), dict(id="h1", prompt="y")])

    def test_model_must_match_manifest_and_provider(self) -> None:
        self.refused(auth(model="other"))
        self.refused(auth(), provider_model="other")
        self.refused(auth(), provider_model=None)

    def test_unknown_mode_refuses(self) -> None:
        self.refused(auth(), mode="yolo")


class StopTests(unittest.TestCase):
    def test_worst_case_cost_formula(self) -> None:
        self.assertEqual(hb.worst_case_usd(auth()), Decimal("0.006"))
        a = auth(cached_input_usd_per_1m="3.00")
        self.assertEqual(hb.worst_case_usd(a), Decimal("0.007"))

    def test_budget_stops_before_dispatch_never_exceeds_cap(self) -> None:
        spy = Spy(prompt=1000, completion=500)  # 0.006 per call
        report = run(spy, auth(max_budget_usd="0.015"), proposals(4))
        self.assertEqual(len(spy.calls), 2)
        self.assertEqual(report["stop_reason"], "budget")
        self.assertLessEqual(Decimal(report["accrued_usd"]), Decimal("0.015"))
        self.assertEqual(report["accrued_usd"], "0.012000")

    def test_call_limit_stops(self) -> None:
        spy = Spy()
        report = run(spy, auth(max_calls=2), proposals(4))
        self.assertEqual((len(spy.calls), report["stop_reason"]), (2, "max_calls"))

    def test_token_limit_reserves_next_call_maximum(self) -> None:
        spy = Spy(prompt=100, completion=50)
        report = run(spy, auth(max_total_tokens=1700), proposals(4))
        self.assertEqual(len(spy.calls), 2)  # 150 + 1500 fits, 300 + 1500 does not
        self.assertEqual(report["stop_reason"], "max_total_tokens")
        self.assertLessEqual(report["tokens"]["total"], 1700)

    def test_all_proposals_exhausted(self) -> None:
        report = run(Spy(), auth(), proposals(3))
        self.assertEqual((report["outcome"], report["stop_reason"]), ("completed", "exhausted"))
        self.assertEqual(report["calls"], 3)

    def test_oversized_prompt_stops_before_dispatch(self) -> None:
        spy = Spy()
        report = run(spy, auth(max_prompt_tokens=5), [dict(id="h1", prompt="x" * 50)])
        self.assertEqual((spy.calls, report["stop_reason"]), ([], "prompt-too-large"))

    def test_provider_receives_completion_bound(self) -> None:
        spy = Spy()
        run(spy, auth(max_completion_tokens=321), proposals(1))
        self.assertEqual(spy.calls[0][2], 321)

    def test_invalid_usage_charges_worst_case_and_stops(self) -> None:
        bad: list[dict[str, Any]] = [
            dict(prompt_tokens=-1, completion_tokens=1, total_tokens=0),
            dict(prompt_tokens=1, completion_tokens=1, total_tokens=3),
            dict(prompt_tokens=100, completion_tokens=1, total_tokens=101, cached_tokens=200),
            dict(prompt_tokens=2000, completion_tokens=1, total_tokens=2001),
            dict(prompt_tokens=1, completion_tokens=900, total_tokens=901),
            dict(prompt_tokens=True, completion_tokens=1, total_tokens=2),
        ]
        for usage in bad:
            spy = Spy()
            spy.usage = usage
            report = run(spy, auth(), proposals(3))
            self.assertEqual(len(spy.calls), 1, usage)
            self.assertEqual(report["stop_reason"], "unmeasured-call")
            self.assertEqual(report["accrued_usd"], "0.006000")

    def test_failed_envelope_stops(self) -> None:
        def fail(*_: Any) -> dict[str, Any]:
            return dict(outcome="provider-unavailable", usage=None, text=None)

        report = run(fail, auth(), proposals(3))
        self.assertEqual((report["calls"], report["stop_reason"]), (1, "unmeasured-call"))

    def test_provider_exception_is_charged_and_stops(self) -> None:
        def boom(*_: Any) -> dict[str, Any]:
            raise RuntimeError("x")

        report = run(boom, auth(), proposals(3))
        self.assertEqual((report["calls"], report["stop_reason"]), (1, "unmeasured-call"))
        self.assertEqual(report["accrued_usd"], "0.006000")


class CostTests(unittest.TestCase):
    def test_cached_tokens_use_cached_rate(self) -> None:
        a = auth(cached_input_usd_per_1m="0.50")
        report = run(Spy(prompt=1000, completion=500, cached=600), a, proposals(1))
        # 400*2 + 600*0.5 + 500*8 = 800 + 300 + 4000 = 5100 per 1M
        self.assertEqual(report["accrued_usd"], "0.005100")
        self.assertEqual(report["tokens"], dict(input=400, cached=600, output=500, total=1500))

    def test_explicit_zero_cached_rate_is_honoured(self) -> None:
        a = auth(cached_input_usd_per_1m="0")
        report = run(Spy(prompt=1000, completion=0, cached=1000), a, proposals(1))
        self.assertEqual(report["accrued_usd"], "0.000000")

    def test_missing_cached_rate_falls_back_to_input_rate(self) -> None:
        report = run(Spy(prompt=1000, completion=0, cached=1000), auth(), proposals(1))
        self.assertEqual(report["accrued_usd"], "0.002000")


class ReportTests(unittest.TestCase):
    def test_spread_nearest_rank(self) -> None:
        s = hb.spread([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.assertEqual(s, dict(count=10, min=10, p50=55.0, mean=55.0, p90=90, max=100))
        self.assertEqual(hb.spread([])["count"], 0)
        self.assertIsNone(hb.spread([])["min"])

    def test_live_report_labels_and_authority(self) -> None:
        report = run(Spy(), auth(), proposals(3))
        self.assertEqual(report["evidence_label"], LIVE)
        self.assertEqual(report["spend_authority_ref"], "slide22_plus_qa_authorize_5usd_batch")
        self.assertIn("provider_call", report["source"])
        self.assertEqual(report["spread"]["total"]["count"], 3)
        self.assertEqual(report["spread"]["total"]["max"], 150)
        self.assertEqual(report["currency"], "USD")

    def test_dry_run_makes_no_provider_call_and_is_labelled(self) -> None:
        report = hb.run_batch(
            auth(), manifest(), proposals(4), hb.dry_run_call, mode="dry-run", now=NOW
        )
        self.assertEqual(report["evidence_label"], DRY)
        self.assertEqual(report["outcome"], "completed")
        self.assertIn("estimator", report["source"])

    def test_dry_run_with_injected_stand_in_stays_unmeasured(self) -> None:
        spy = Spy()
        report = hb.run_batch(auth(), manifest(), proposals(2), spy, mode="dry-run", now=NOW)
        self.assertEqual((report["evidence_label"], report["source"]), (DRY, hb.SOURCE_DRY))

    def test_refused_report_has_no_measured_label(self) -> None:
        report = run(Spy(), auth(currency="EUR"))
        self.assertEqual(report["evidence_label"], DRY)
        self.assertIn("refused", report["outcome"])

    def test_deterministic_and_no_proposal_text(self) -> None:
        one = run(Spy(), auth(), proposals(3, "secret words"))
        two = run(Spy(), auth(), proposals(3, "secret words"))
        self.assertEqual(hb.render_json(one), hb.render_json(two))
        self.assertNotIn("secret words", hb.render_json(one))
        self.assertEqual(json.loads(hb.render_json(one))["calls"], 3)

    def test_markdown_table(self) -> None:
        md = hb.render_markdown(run(Spy(), auth(), proposals(3)))
        for needle in ("| min |", "p50", "mean", "p90", "max", LIVE, "slide22_plus_qa"):
            self.assertIn(needle, md)

    def test_input_not_mutated(self) -> None:
        a, m, p = auth(), manifest(), proposals()
        before = copy.deepcopy((a, m, p))
        run(Spy(), a, p, m=m)
        self.assertEqual((a, m, p), before)


class CliTests(unittest.TestCase):
    def files(self, tmp: str) -> list[str]:
        root = Path(tmp)
        (root / "a.json").write_text(
            json.dumps(auth(expires_utc="2099-01-01T00:00:00+00:00")), encoding="utf-8"
        )
        (root / "m.json").write_text(json.dumps(manifest()), encoding="utf-8")
        (root / "p.json").write_text(json.dumps(proposals(3)), encoding="utf-8")
        return [
            "--authorization", str(root / "a.json"),
            "--manifest", str(root / "m.json"),
            "--proposals", str(root / "p.json"),
        ]  # fmt: skip

    def call(self, argv: list[str], **kw: Any) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = hb.main(argv, **kw)
        return code, out.getvalue(), err.getvalue()

    def test_dry_run_prints_json_and_writes_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "r.json"
            code, stdout, _ = self.call(
                [*self.files(tmp), "--dry-run", "--json-out", str(out), "--markdown"]
            )
            self.assertEqual(code, 0)
            self.assertIn(DRY, stdout)
            self.assertEqual(json.loads(out.read_text(encoding="utf-8"))["calls"], 3)

    def test_mode_flag_is_required_and_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for extra in ([], ["--dry-run", "--execute-live"]):
                with self.assertRaises(SystemExit):
                    self.call([*self.files(tmp), *extra])

    def test_execute_live_without_provider_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, _, err = self.call([*self.files(tmp), "--execute-live"])
            self.assertEqual(code, hb.NOT_CONFIGURED)
            self.assertIn("no provider", err)

    def test_execute_live_with_injected_provider(self) -> None:
        spy = Spy()
        with tempfile.TemporaryDirectory() as tmp:
            code, stdout, _ = self.call(
                [*self.files(tmp), "--execute-live"], provider=spy, provider_model="m-1"
            )
        self.assertEqual((code, len(spy.calls)), (0, 3))
        self.assertIn(LIVE, stdout)

    def test_refused_batch_exits_nonzero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            argv = self.files(tmp)
            Path(argv[1]).write_text(json.dumps(auth(currency="GBP")), encoding="utf-8")
            code, stdout, _ = self.call([*argv, "--dry-run"])
        self.assertEqual(code, 1)
        self.assertIn("refused", stdout)


if __name__ == "__main__":
    unittest.main()
