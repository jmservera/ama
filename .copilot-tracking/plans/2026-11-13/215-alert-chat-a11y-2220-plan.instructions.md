---
applyTo: '.copilot-tracking/changes/2026-11-13/215-alert-chat-a11y-2220-changes.md'
---
<!-- markdownlint-disable-file -->
# Implementation Plan: Issue 215 alert and chat WCAG cues, keyboard and plain language

## Overview

Close the criterion 3 software and markup gaps in the regulatory alerts panel and home regulatory chat. Criterion 5 stays unmet.

## Objectives

* Every alert state, grounding outcome, doubt route, no-source and unknown-coverage state has a text plus glyph or shape cue that is not colour-only.
* Chat disclosure closes on Escape and restores focus to its summary.
* Plain-language mode explains alert states, chat outcomes, no-source, doubt route and unknown coverage.

## Context Summary

* Research: [.copilot-tracking/research/2026-11-13/215-alert-chat-a11y-2220-research.md](../../research/2026-11-13/215-alert-chat-a11y-2220-research.md)
* Details: [.copilot-tracking/details/2026-11-13/215-alert-chat-a11y-2220-details.md](../../details/2026-11-13/215-alert-chat-a11y-2220-details.md)

## Implementation Checklist

### [x] Phase 1: Markup and CSS cues

* [x] Step 1.1: state classes in `chat.js` for alerts, chat outcomes, no-source, doubt, unknown coverage
* [x] Step 1.2: glyph and border-style rules in `style.css`

### [x] Phase 2: Plain language and keyboard

* [x] Step 2.1: plain explanations for outcomes, no-source, doubt, unknown coverage
* [x] Step 2.2: Escape closes chat disclosure and restores summary focus

### [x] Phase 3: Tests and records

* [x] Step 3.1: new `test_regulatory_a11y_cues.py` static tests
* [x] Step 3.2: extend browser check for Escape and cues
* [x] Step 3.3: update `src/api/README.md` criterion audit and WCAG baseline row
* [x] Step 3.4: run focused validation (unit, ruff, mypy, browser if available)

## Dependencies

* `/tmp/venv-215-2220` (pip), Chromium in `~/.cache/ms-playwright`.

## Success Criteria

* New and existing tests green; `test_accessibility_baseline.py` still pins eight sites; `test_content_standard.py` green.
* No change to `infra/`, ranking modules or queue screens.
* README states only engineering evidence; no conformance or comprehension claim.
