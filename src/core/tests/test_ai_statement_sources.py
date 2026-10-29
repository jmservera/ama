"""Statement boundaries retain their declared citations."""

import unittest

from zava_forward.core.ai_tasks import statement_sources


class StatementSources(unittest.TestCase):
    def test_line_breaks_before_trailing_citations(self) -> None:
        sources = {"ZF-1": ["Stage: Survey booked", "Days in stage: 3"]}
        for separator in ("\n", "\r\n", " \n\t"):
            with self.subTest(separator=repr(separator)):
                self.assertEqual(
                    statement_sources(
                        f"Survey is booked.{separator}[[ZF-1: Stage: Survey booked]] "
                        "The case has waited three days. [[ZF-1: Days in stage: 3]]",
                        sources,
                    ),
                    [
                        dict(
                            text="Survey is booked.",
                            citations=["ZF-1: Stage: Survey booked"],
                            unresolved=[],
                        ),
                        dict(
                            text="The case has waited three days.",
                            citations=["ZF-1: Days in stage: 3"],
                            unresolved=[],
                        ),
                    ],
                )
        self.assertEqual(
            statement_sources(
                "Survey is booked.\n[[ZF-1: Stage: Survey booked]]\r\n[[Unknown]]\n"
                "The next claim is uncited.\nA separate line is uncited",
                sources,
            ),
            [
                dict(
                    text="Survey is booked.",
                    citations=["ZF-1: Stage: Survey booked"],
                    unresolved=["Unknown"],
                ),
                dict(text="The next claim is uncited.", citations=[], unresolved=[]),
                dict(text="A separate line is uncited", citations=[], unresolved=[]),
            ],
        )

    def test_titles_and_medial_abbreviations_preserve_statement(self) -> None:
        sources = {"ZF-1": ["Stage: Survey booked"]}
        statements = [
            f"Contact {title} Jones about the survey."
            for title in ("Dr.", "Mr.", "Mrs.", "Ms.", "Mx.", "Prof.", "Rev.", "Sr.", "Jr.")
        ] + [
            "St. Mary's needs repairs.",
            "The survey at St. John is booked.",
            "Check options, e.g. survey dates.",
            "Check options, i.e. survey dates.",
            "Compare booked vs. pending surveys.",
            "Check the record, cf. survey dates.",
            "Allow approx. three days.",
            "Check dates etc. before booking.",
        ]
        for statement in statements:
            with self.subTest(statement=statement):
                self.assertEqual(
                    statement_sources(statement[:-1] + " [[ZF-1: Stage: Survey booked]].", sources),
                    [
                        dict(
                            text=statement,
                            citations=["ZF-1: Stage: Survey booked"],
                            unresolved=[],
                        )
                    ],
                )

    def test_abbreviations_do_not_hide_sentence_or_newline_boundaries(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for first in ("The address is High St.", "Check the dates etc."):
            with self.subTest(first=first):
                self.assertEqual(
                    statement_sources(first + " Repairs are due. [[Second source]]", sources),
                    [
                        dict(text=first, citations=[], unresolved=[]),
                        dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
                    ],
                )
        self.assertEqual(
            statement_sources(
                "Dr. Smith checked the case. [[First source]] Repairs are due. [[Second source]]",
                sources,
            ),
            [
                dict(
                    text="Dr. Smith checked the case.",
                    citations=["First source"],
                    unresolved=[],
                ),
                dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
            ],
        )
        self.assertEqual(
            statement_sources("Contact Dr.\nJones is available [[Second source]].", sources),
            [
                dict(text="Contact Dr.", citations=[], unresolved=[]),
                dict(text="Jones is available.", citations=["Second source"], unresolved=[]),
            ],
        )

    def test_trailing_citations_preserve_sentence_and_source_boundaries(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for punctuation in ".!?":
            for separator in (" ", "  ", "\t", "\n"):
                with self.subTest(punctuation=punctuation, separator=repr(separator)):
                    text = (
                        f"First{punctuation} [[First source]]{separator}Second. [[Second source]]"
                    )
                    self.assertEqual(
                        statement_sources(text, sources),
                        [
                            dict(
                                text=f"First{punctuation}",
                                citations=["First source"],
                                unresolved=[],
                            ),
                            dict(text="Second.", citations=["Second source"], unresolved=[]),
                        ],
                    )
        self.assertEqual(
            statement_sources(
                "First. [[First source]] [[Unknown source]] Second. [[Second source]]",
                sources,
            ),
            [
                dict(text="First.", citations=["First source"], unresolved=["Unknown source"]),
                dict(text="Second.", citations=["Second source"], unresolved=[]),
            ],
        )
