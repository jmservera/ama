"""Stable module name for the alert chat keyboard and provenance tests."""

from test_home_chat_regulatory_keyboard_provenance import (  # noqa: F401
    NativeControlTests,
    ProvenanceAndOutcomeTests,
    RegulatoryDisclosureTests,
    WidgetKeyboardTests,
)

if __name__ == "__main__":
    import unittest

    unittest.main()
