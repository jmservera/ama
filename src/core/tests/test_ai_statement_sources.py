"""Statement boundaries retain their declared citations."""

import unittest

from zava_forward.core.ai_tasks import statement_sources


class StatementSources(unittest.TestCase):
    def test_trailing_citations_preserve_sentence_and_source_boundaries(self):
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
