"""Audit that every documented child of Epics #104, #149 and #165 has one explicit disposition.

Refs #104, Refs #149, Refs #165, Refs #440. Read-only over the repository evidence;
it never asserts live GitHub state and never promotes a child to approved.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs/architecture/cutover-evidence-pack.md"
MATRIX = ROOT / "docs/architecture/mvp-to-src-parity-matrix.md"
RESEARCH = ROOT / "docs/reference/research"

CLOSED = "closed"
UNVERIFIED = "implemented-unverified"
DEFERRED = "deferred"
IN_PROGRESS = "in-progress"
DISPOSITIONS = {CLOSED, UNVERIFIED, DEFERRED, IN_PROGRESS}

# Child -> disposition recorded by the repository evidence (pack, parity matrix, research).
CHILDREN = {
    "#104": {
        105: CLOSED,
        106: CLOSED,
        107: IN_PROGRESS,
        108: DEFERRED,
        432: DEFERRED,
        435: DEFERRED,
    },
    "#149": {
        150: UNVERIFIED,
        151: UNVERIFIED,
        152: UNVERIFIED,
        153: IN_PROGRESS,
        154: DEFERRED,
        155: DEFERRED,
        156: IN_PROGRESS,
        **{n: IN_PROGRESS for n in range(225, 234)},
    },
    "#165": {
        166: CLOSED,
        167: UNVERIFIED,
        175: UNVERIFIED,
        176: IN_PROGRESS,
        177: UNVERIFIED,
        184: DEFERRED,
        190: UNVERIFIED,
    },
}

RESIDUAL = re.compile(
    r"\bopen\b|unmet|unverified|not observed|not-generated|not recorded|unproven"
    r"|\bheld\b|gated|\bnot (?:yet )?(?:ticked|met|shown|approved|accepted)"
    r"|whole-parent|owner|named human|human|\bblocked\b|deferr|proposal|draft|pending",
    re.IGNORECASE,
)
NEGATION = re.compile(
    r"\bnot\b|\bno\b|\bnothing\b|\bnor\b|\bneither\b|\bnever\b|stay|\bhold|held|gate"
    r"|until|unless|\bif\b|before|criteria|closure|\bor\b|prerequisite|open|unticked",
    re.IGNORECASE,
)
REOPEN = re.compile(r"Reopen\s+((?:#\d+(?:,\s*|\s+and\s+)?)+)")


def lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def mentions(number, text):
    return re.search(rf"(?:#|/issues/){number}\b", text) is not None


def evidence_lines(number, window=1):
    pattern = re.compile(rf"(?:#|/issues/){number}\b")
    found = []
    for path in [PACK, MATRIX, *sorted(RESEARCH.rglob("*.md"))]:
        text = lines(path)
        for index, line in enumerate(text):
            if pattern.search(line):
                found.append(" ".join(text[index : index + window]))
    return found


def all_children():
    return {n: d for group in CHILDREN.values() for n, d in group.items()}


class EpicChildDispositionAudit(unittest.TestCase):
    def test_catalogue_matches_issue_numbers_and_dispositions(self):
        children = all_children()
        self.assertEqual(sum(len(g) for g in CHILDREN.values()), len(children))
        self.assertEqual(set(CHILDREN), {"#104", "#149", "#165"})
        for number, disposition in children.items():
            self.assertIn(disposition, DISPOSITIONS, f"#{number}")

    def test_every_child_is_documented_in_repository_evidence(self):
        for number in all_children():
            self.assertTrue(
                evidence_lines(number), f"#{number} has no repository evidence"
            )

    def test_non_closed_children_carry_an_explicit_residual(self):
        for number, disposition in all_children().items():
            if disposition == CLOSED:
                continue
            residual = [
                ln for ln in evidence_lines(number, window=9) if RESIDUAL.search(ln)
            ]
            self.assertTrue(
                residual, f"#{number} ({disposition}) records no open residual"
            )

    def test_closed_children_are_not_on_the_matrix_reopen_list(self):
        reopened = set()
        for match in REOPEN.finditer(MATRIX.read_text(encoding="utf-8")):
            reopened.update(int(n) for n in re.findall(r"#(\d+)", match.group(1)))
        self.assertTrue(reopened & set(all_children()))
        for number in reopened & set(all_children()):
            self.assertNotEqual(all_children()[number], CLOSED, f"#{number}")

    def test_closed_children_have_explicit_closed_evidence(self):
        for number, disposition in all_children().items():
            if disposition != CLOSED:
                continue
            claim = re.compile(
                rf"#{number}\b[^|]{{0,60}}\bclosed\b|\bclosed\b[^|]{{0,30}}#{number}\b"
            )
            hit = any(claim.search(ln) for ln in lines(PACK) + lines(MATRIX))
            self.assertTrue(hit, f"#{number} lacks explicit closed evidence")

    def test_pack_never_claims_non_closed_child_closed_or_approved(self):
        claim_template = r"#{n}\b[^|]{{0,60}}\b(?:closed|approved|accepted)\b|\b(?:closed|approved|accepted)\b[^|]{{0,30}}#{n}\b"
        for number, disposition in all_children().items():
            if disposition == CLOSED:
                continue
            claim = re.compile(claim_template.format(n=number), re.IGNORECASE)
            for line in lines(PACK):
                if claim.search(line):
                    self.assertRegex(line, NEGATION, f"#{number}: {line[:120]}")

    def test_no_child_is_claimed_approved_where_residuals_remain(self):
        approved = re.compile(r"#(\d+)\b[^|.]{0,40}\bapproved\b", re.IGNORECASE)
        children = all_children()
        for line in lines(PACK):
            for match in approved.finditer(line):
                number = int(match.group(1))
                if number in children:
                    self.assertRegex(line, NEGATION, f"#{number}: {line[:120]}")

    def test_epics_are_never_recorded_closed(self):
        epic = re.compile(
            r"#(?:104|149|165)\b[^|.]{0,40}\b(?:closed|approved)\b", re.IGNORECASE
        )
        for line in lines(PACK):
            if epic.search(line):
                self.assertRegex(line, NEGATION, line[:120])
        self.assertTrue(any("all five epics are open" in ln for ln in lines(PACK)))


if __name__ == "__main__":
    unittest.main()
