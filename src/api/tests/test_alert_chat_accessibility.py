"""Stable module name for the alert and chat accessibility cue and provenance tests."""

from test_home_chat_regulatory_keyboard_provenance import ProvenanceAndOutcomeTests  # noqa: F401
from test_regulatory_a11y_cues import RegulatoryCueTests  # noqa: F401

if __name__ == "__main__":
    import unittest

    unittest.main()
