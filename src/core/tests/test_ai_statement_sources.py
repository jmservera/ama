"""Statement boundaries retain their declared citations."""

import unittest

from zava_forward.core.ai_tasks import statement_sources


class StatementSources(unittest.TestCase):
    def test_quoted_statement_keeps_its_own_references(self) -> None:
        self.assertEqual(
            statement_sources(
                'The status is "Survey booked." [[First source]] '
                "Repairs are due. [[Second source]]",
                {"ZF-1": ["First source", "Second source"]},
            ),
            [
                dict(
                    text='The status is "Survey booked."',
                    citations=["First source"],
                    unresolved=[],
                ),
                dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
            ],
        )

    def test_closing_delimiters_preserve_sentence_and_reference_boundaries(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for punctuation in (".", "!", "?", "...", "?!", "!?", "...?!", "\u2026"):
            for opening, closing in (
                ('"', '"'),
                ("'", "'"),
                ("\u201c", "\u201d"),
                ("\u2018", "\u2019"),
                ("(", ")"),
                ("[", "]"),
                ("{", "}"),
                ('("', '")'),
                ("\u201c[(", ")]\u201d"),
                ("(", ")."),
                ('("', '").'),
            ):
                for separator in (" ", "\t", "\n", "\r\n"):
                    for placement in ("before", "after", "uncited"):
                        with self.subTest(
                            punctuation=punctuation,
                            closing=closing,
                            separator=repr(separator),
                            placement=placement,
                        ):
                            first = f"Status: {opening}Survey booked{punctuation}{closing}"
                            reference = "[[First source]] [[Unknown source]]"
                            if placement == "before":
                                text = (
                                    f"Status: {opening}Survey booked {reference}"
                                    f"{punctuation}{closing}"
                                )
                            elif placement == "after":
                                text = first + separator + reference
                            else:
                                text = first
                            self.assertEqual(
                                statement_sources(
                                    text + separator + "Repairs are due. [[Second source]]",
                                    sources,
                                ),
                                [
                                    dict(
                                        text=first,
                                        citations=[]
                                        if placement == "uncited"
                                        else ["First source"],
                                        unresolved=[]
                                        if placement == "uncited"
                                        else ["Unknown source"],
                                    ),
                                    dict(
                                        text="Repairs are due.",
                                        citations=["Second source"],
                                        unresolved=[],
                                    ),
                                ],
                            )

    def test_terminal_name_suffixes_do_not_borrow_next_statement_references(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for suffix in ("Jr.", "Sr."):
            for first_cited, second_cited in ((False, True), (True, False), (True, True)):
                with self.subTest(
                    suffix=suffix, first_cited=first_cited, second_cited=second_cited
                ):
                    first = f"Contact John Smith {suffix}"
                    second = "Repairs are due."
                    self.assertEqual(
                        statement_sources(
                            first
                            + (" [[First source]]" if first_cited else "")
                            + " "
                            + second
                            + (" [[Second source]]" if second_cited else ""),
                            sources,
                        ),
                        [
                            dict(
                                text=first,
                                citations=["First source"] if first_cited else [],
                                unresolved=[],
                            ),
                            dict(
                                text=second,
                                citations=["Second source"] if second_cited else [],
                                unresolved=[],
                            ),
                        ],
                    )

    def test_medial_name_suffixes_keep_the_first_statement_references(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for suffix in ("Jr.", "Sr."):
            first = f"Contact John Smith {suffix} about the survey."
            with self.subTest(suffix=suffix):
                self.assertEqual(
                    statement_sources(
                        first + " [[First source]] Repairs are due. [[Second source]]", sources
                    ),
                    [
                        dict(text=first, citations=["First source"], unresolved=[]),
                        dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
                    ],
                )

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
        for punctuation in (".", "!", "?", "...", "?!", "!?", "...?!", "\u2026"):
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

    def test_complete_punctuation_run_keeps_full_statement_objects(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for first in (
            "Still waiting...",
            "Still waiting?!",
            'Still waiting...")',
            "Still waiting?!]}",
            "Still waiting\u2026",
            "(Still waiting...).",
            '"Still waiting?!"!',
        ):
            with self.subTest(first=first):
                self.assertEqual(
                    statement_sources(
                        first + " [[First source]] Repairs are due. [[Second source]]",
                        sources,
                    ),
                    [
                        dict(text=first, citations=["First source"], unresolved=[]),
                        dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
                    ],
                )

    def test_closing_delimiters_after_a_citation_stay_with_their_statement(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        for first, closer in (
            ('The status is "Survey booked.', '"'),
            ("The status is (survey booked.", ")"),
            ("The status is [survey booked.", "]"),
            ("The status is \u201csurvey booked.", "\u201d"),
        ):
            with self.subTest(first=first):
                self.assertEqual(
                    statement_sources(
                        f"{first} [[First source]]{closer} Repairs are due. [[Second source]]",
                        sources,
                    ),
                    [
                        dict(text=first + closer, citations=["First source"], unresolved=[]),
                        dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
                    ],
                )

    def test_closer_run_after_citation_stays_and_next_opening_quote_is_kept(self) -> None:
        sources = {"ZF-1": ["First source", "Second source"]}
        self.assertEqual(
            statement_sources(
                "The status is [survey booked? [[First source]]]. "
                "Repairs are due. [[Second source]]",
                sources,
            ),
            [
                dict(
                    text="The status is [survey booked?].",
                    citations=["First source"],
                    unresolved=[],
                ),
                dict(text="Repairs are due.", citations=["Second source"], unresolved=[]),
            ],
        )
        for quote in ('"', "'", "\u201c"):
            end = {'"': '"', "'": "'", "\u201c": "\u201d"}[quote]
            with self.subTest(quote=quote):
                self.assertEqual(
                    statement_sources(
                        f"Survey is booked. [[First source]] "
                        f"{quote}Repairs are due.{end} [[Second source]]",
                        sources,
                    ),
                    [
                        dict(text="Survey is booked.", citations=["First source"], unresolved=[]),
                        dict(
                            text=f"{quote}Repairs are due.{end}",
                            citations=["Second source"],
                            unresolved=[],
                        ),
                    ],
                )
