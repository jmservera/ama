"""Validate coordinator instructions and handoff/status Markdown for Issue #1204.

Checks two surfaces offline without network access:
1. `.github/agents/ama-backlog-delivery-coordinator.agent.md` defines valid
   frontmatter, resolved relative Markdown links, all five required issue-state
   classification categories (`merged`, `active session`, `human-blocked`,
   `dependency-blocked`, `ready to start`), concrete link rules for blocked
   categories, anti-idle / unverified-blocker / unclassified-open-issue guards,
   and live-command refresh requirements for handoffs and checkpoints.
2. Coordinator handoff, scheduled-check status, and checkpoint Markdown files
   render valid five-category classification tables before any idle, waiting,
   "nothing changed", or pause summary, carry concrete non-bare-self blocker
   links on `human-blocked` and `dependency-blocked` rows, reject unsupported
   idle/waiting summaries when unclassified or actionable `ready to start`
   open issues exist, and flag stale count/SHA/timestamp handoff blocks.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from bisect import bisect_left, bisect_right
from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_RELATIVE_PATH = Path(".github/agents/ama-backlog-delivery-coordinator.agent.md")
DEFAULT_LOCAL_REPO = "jmservera/ama"

REQUIRED_CATEGORIES: tuple[str, ...] = (
    "merged",
    "active session",
    "human-blocked",
    "dependency-blocked",
    "ready to start",
)
LINK_REQUIRED_CATEGORIES: tuple[str, ...] = (
    "human-blocked",
    "dependency-blocked",
)
NON_MERGED_CATEGORIES: frozenset[str] = frozenset(c for c in REQUIRED_CATEGORIES if c != "merged")
DEFAULT_SESSION_CAP = 8

BlockerRef = tuple[str, int | str]

FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
ISO_DATE_TOKEN_RE = re.compile(r"\b20\d{2}-\d{2}-\d{2}\b")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+)")
BLOCKQUOTE_PREFIX_RE = re.compile(r"^[ \t]*((?:>[ \t]*)+)(.*)")
LIST_MARKER_RE = re.compile(r"^(?:[*+-]|\d+[.)])[ \t]+")
MD_LINK_RE = re.compile(r"\[([^\[\]\n]+)\]\(([^()\s]+)\)")
URL_RE = re.compile(r"https?://[^\s)>`]+")
COMMENT_ANCHOR_RE = re.compile(
    r"(?:#(?:\d+#)?|\b)(?:issuecomment-\d+|pullrequestreview-\d+|discussion_r\d+)\b"
)
GITHUB_FRAGMENT_ANCHOR_RE = re.compile(
    r"^#(?:\d+#)?(?:issuecomment-\d+|pullrequestreview-\d+|discussion_r\d+)$"
)
SCOPED_FRAGMENT_ISSUE_RE = re.compile(
    r"^#(\d+)#(?:issuecomment-\d+|pullrequestreview-\d+|discussion_r\d+)$"
)
GITHUB_REPO_URL_PREFIX_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?:/|$)",
    re.IGNORECASE,
)
GITHUB_REPO_ISSUE_PR_URL_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/(?:issues|pull)/(\d+)"
    r"(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)
EXTERNAL_HOST_ISSUE_PR_URL_RE = re.compile(
    r"^https?://([^/\s]+)(/[^\s?#]*?)/(?:issues|pull)/(\d+)(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)
RELATIVE_REPO_ISSUE_PR_RE = re.compile(
    r"^/?([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/(?:issues|pull)/(\d+)(?![A-Za-z0-9_-])",
    re.IGNORECASE,
)
BARE_GITHUB_ISSUE_URL_RE = re.compile(
    r"^(?:https?://(?:www\.)?github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/|"
    r"(?:(?:\./)?|/)?(?:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/)?)issues/(\d+)/?$",
    re.IGNORECASE,
)
GITHUB_ISSUE_PR_URL_RE = re.compile(r"(?:^|/)(?:issues|pull)/(\d+)(?![A-Za-z0-9_-])", re.IGNORECASE)
GITHUB_ISSUES_ONLY_URL_RE = re.compile(r"/issues/(\d+)(?![A-Za-z0-9_-])", re.IGNORECASE)
HASH_ISSUE_RE = re.compile(r"#(\d+)(?![A-Za-z0-9_-])")
REPO_PATH_CHARS: frozenset[str] = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-/"
)
PLAIN_SINGLE_ISSUE_CELL_RE = re.compile(r"^#?(\d+)$")
LINKED_SINGLE_ISSUE_CELL_RE = re.compile(r"^\[([^\[\]\n]+)\]\(([^()\s]+)\)$")
TABLE_SEP_CELL_RE = re.compile(r"^:?-{3,}:?$")
KV_LINE_RE = re.compile(r"^[ \t]*(?:[*+-][ \t]+)?([A-Za-z][A-Za-z0-9 /_-]{1,42}):[ \t]*(.+)")
HEX_SHA_RE = re.compile(r"^[0-9a-fA-F]{7,40}$")
BACKTICK_TOKEN_RE = re.compile(r"`([^`\n]+)`")
BACKTICK_OR_URL_RE = re.compile(r"`[^`\n]*`|https?://[^\s)>`]+")
WORD_TOKEN_RE = re.compile(r"[A-Za-z0-9_']+")
SENTENCE_SPLIT_RE = re.compile(r"[.;!?]")
RPI_SESSION_RE = re.compile(r"^rpi-(\d+)(?:-[A-Za-z0-9_.-]+)?$")
STANDALONE_ISSUE_NUM_RE = re.compile(r"(?<!\d)(\d+)(?!\d)")

CLAUSE_SPLIT_RE = re.compile(
    r"[;.!?:]|(?<=\s)--\s+|"
    r",\s+(?:(?:so|but|yet|then|while)\b|"
    r"(?=(?:\"nothing\s+changed\"|nothing\s+changed|status:|idle\s+tick|reporting\s+idle|"
    r"waiting\s+(?:on|for|summary)|paused\s+summary|all\s+lanes\s+(?:waiting|paused)|"
    r"(?:(?:scheduled\s+)?check|(?:coordinator\s+)?run|delivery|schedule|tick)\s+(?:is\s+)?"
    r"paus(?:ed|ing)\b|paus(?:ed|ing|e)\b|"
    r"blocked\s+(?:on|by)|counts?\s+copied|copied\s+from|carried\s+over|cached\s+from)))",
    re.IGNORECASE,
)

PROHIBITION_HEAD_RE = re.compile(
    r"\b(?:(never|cannot|can't|must\s+not|do\s+not|don't)(?:\s+ever)?|"
    r"(forbid\w*|prohibit\w*|bars?|excludes?|reject\w*))\b",
    re.IGNORECASE,
)
INLINE_LITERAL_SPAN_RE = re.compile(
    r"\"[^\"\n]*\"|(?<![A-Za-z0-9])'[^'\n]*'(?![A-Za-z0-9])|`[^`\n]*`"
)
GOV_VERB_TOKEN_RE = re.compile(
    r"^(?:"
    r"repeat\w*|claim\w*|report\w*|emit\w*|say\w*|stat\w*|writ\w*|assert\w*|"
    r"accept\w*|allow\w*|permit\w*|launch\w*|start\w*|dispatch\w*|spawn\w*|"
    r"paus\w*|wait\w*|cop(?:y|ies|ied|ying)|carr(?:y|ies|ied|ying)|"
    r"cach\w*|reus\w*|rel(?:y|ies|ied|ying)"
    r")$",
    re.IGNORECASE,
)
TRAILING_PREP_DET_TOKENS: frozenset[str] = frozenset(
    {"on", "for", "a", "an", "the", "any", "global"}
)
GOV_CONTINUATION_TOKENS: frozenset[str] = frozenset(
    {
        "qtok",
        "or",
        "nor",
        "on",
        "for",
        "over",
        "a",
        "an",
        "the",
        "any",
        "global",
        "idle",
        "waiting",
        "pause",
        "tick",
        "ticks",
        "summary",
        "summaries",
        "state",
        "states",
        "claim",
        "claims",
        "count",
        "counts",
        "sha",
        "shas",
        "session",
        "sessions",
        "snapshot",
        "snapshots",
    }
)

ZERO_UNCLASSIFIED_PRECOND_RE = re.compile(
    r"\b(?:permitted\s+only\s+when|only\s+after)\b",
    re.IGNORECASE,
)
ZERO_UNCLASSIFIED_TARGET_RE = re.compile(
    r"\bzero\s+(?:open\s+issues\s+)?unclassified\b",
    re.IGNORECASE,
)

IDLE_CLAIM_RE = re.compile(
    r"(?:"
    r"\"nothing\s+changed\"|"
    r"\bnothing\s+changed\b|"
    r"\bno\s+changes\s+since\s+(?:the\s+)?last\b|"
    r"\bidle\s+tick\b|"
    r"\bstatus:\s*idle\b|"
    r"\breporting\s+idle\b|"
    r"\bno\s+actionable\s+(?:open\s+)?(?:work|issues|items)\b|"
    r"\ball\s+(?:remaining\s+|open\s+)?(?:issues|items|work)\s+(?:are|is)\s+"
    r"(?:human-blocked|dependency-blocked|blocked|merged)\b"
    r")",
    re.IGNORECASE,
)

PAUSE_HEAD_PAT = (
    r"\bstatus:\s*paus(?:ed|ing|e)\b|"
    r"\bpaused\s+summary\b|"
    r"\ball\s+lanes\s+paused\b|"
    r"\b(?:(?:scheduled\s+)?check|(?:coordinator\s+)?run|delivery|schedule|tick)\s+"
    r"(?:is\s+)?paus(?:ed|ing)\b|"
    r"\bpaus(?:ed|ing|e)\s+(?:the\s+)?"
    r"(?:run|schedule|delivery|check|tick|on\b|for\b|until\b|due\s+to\b|because\b|owing\s+to\b)"
)

WAITING_OR_PAUSE_RE = re.compile(
    r"(?:"
    r"\bstatus:\s*waiting\b|"
    r"\bwaiting\s+summary\b|"
    r"\ball\s+lanes\s+waiting\b|"
    r"\bnothing\s+ready\s+to\s+start\b|"
    r"\bwaiting\s+(?:on|for|until)\b|" + PAUSE_HEAD_PAT + r")",
    re.IGNORECASE,
)

DIRECT_GLOBAL_WAIT_RE = re.compile(
    r"(?:"
    r"\bstatus:\s*waiting\b|"
    r"\bwaiting\s+summary\b|"
    r"\ball\s+lanes\s+waiting\b|"
    r"\bnothing\s+ready\s+to\s+start\b|" + PAUSE_HEAD_PAT + r")",
    re.IGNORECASE,
)
WAITING_ON_FOR_RE = re.compile(
    r"\b(?:waiting\s+(?:on|for|until)|blocked\s+(?:on|by))\b",
    re.IGNORECASE,
)
HOLD_CONTINUATION_RE = re.compile(
    r"\b(?:before|until|prior\s+to|instead\s+of)\s+"
    r"(?:continuing|starting|launching|proceeding|dispatching)\b",
    re.IGNORECASE,
)

READY_LAUNCH_RE = re.compile(
    r"(?:"
    r"\b(?:launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing))\s+"
    r"(?:(?:new|next|tmux|worker|session|issue)\s+){0,4}"
    r"(?:#(\d+)(?![A-Za-z0-9_-])|`?rpi-(\d+)(?:-[A-Za-z0-9_.-]+)?`?)|"
    r"(?:(?:issue|worker|session)\s+)?"
    r"(?:#(\d+)(?![A-Za-z0-9_-])|`?rpi-(\d+)(?:-[A-Za-z0-9_.-]+)?`?)\s+"
    r"(?:is|has)\s+(?:now\s+)?"
    r"(?:launch(?:ed|ing)|start(?:ed|ing)|dispatch(?:ed|ing)|spawn(?:ed|ing))\b"
    r")",
    re.IGNORECASE,
)

LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE = re.compile(
    r"\b(?:"
    r"before|until|without|instead\s+of|prior\s+to|unless|if|"
    r"not|no|never|cannot|can't|must\s+not|do\s+not|don't|"
    r"unable\s+to|fail(?:ed|ing|s)?\s+to|"
    r"defer\w*|postpon\w*|skip\w*|(?:hold(?:ing)?|held)\s+off(?:\s+on)?|"
    r"will|would|could|should|might|may|"
    r"(?:plan(?:ning|ned|s)?|intend(?:ing|ed|s)?)\s+(?:to|on)|"
    r"going\s+to"
    r")\b|n't\b",
    re.IGNORECASE,
)

NON_CURRENT_LAUNCH_SUBCLAUSE_RE = re.compile(
    r"\b(?:"
    r"previously|earlier|already|yesterday|formerly|later|tomorrow|eventually|soon|"
    r"after|once|when|whenever|if|unless|until|before|pending|upon|awaiting|"
    r"deferred|postponed|skipped|failed|aborted|cancell?ed"
    r")\b|"
    r"(?<!since\s)(?<!since\sthe\s)\b"
    r"(?:last|prior|previous|next|future|following|subsequent|upcoming)\s+"
    r"(?:tick|check|run|turn|wave|slot|window|cycle|pass)\b",
    re.IGNORECASE,
)

SUBCLAUSE_SPLIT_RE = re.compile(r"\bwhile\b|,\s+and\b", re.IGNORECASE)

UNVERIFIED_BLOCKER_RE = re.compile(
    r"\b(?:unverified|assumed|unconfirmed|cached|suspected)\s+blocker\b",
    re.IGNORECASE,
)

NEXT_CHECK_NOUN_LOOKAHEAD_PAT = (
    r"(?:(?:a|an|the)[ \t]+)?(?:next[ \t]+)?(?:scheduled[ \t]+|coordinator[ \t]+)?"
    r"(?:check|tick|run|poll|cycle|pass|turn|window)\b"
)
WAIT_INTRODUCER_TAIL_PAT = (
    r"(?:\s+(?:on|for|until|due\s+to|because(?:\s+of)?|owing\s+to|"
    r"(?:pending|awaiting)(?![ \t]+" + NEXT_CHECK_NOUN_LOOKAHEAD_PAT + r"))\b)?"
)

WAIT_OR_BLOCKER_SPAN_TRIGGER_RE = re.compile(
    r"\b(?:"
    r"status:\s*waiting\b" + WAIT_INTRODUCER_TAIL_PAT + r"|"
    r"status:\s*paus(?:ed|ing|e)\b" + WAIT_INTRODUCER_TAIL_PAT + r"|"
    r"waiting\s+summary\b" + WAIT_INTRODUCER_TAIL_PAT + r"|"
    r"paused\s+summary\b" + WAIT_INTRODUCER_TAIL_PAT + r"|"
    r"all\s+lanes\s+(?:waiting|paused)\b" + WAIT_INTRODUCER_TAIL_PAT + r"|"
    r"(?:(?:scheduled\s+)?check|(?:coordinator\s+)?run|delivery|schedule|tick)\s+"
    r"(?:is\s+)?paus(?:ed|ing)\b" + WAIT_INTRODUCER_TAIL_PAT + r"|"
    r"paus(?:ed|ing|e)\b(?:\s+(?:the\s+)?(?:run|schedule|delivery|check|tick)\b)?"
    + WAIT_INTRODUCER_TAIL_PAT
    + r"|"
    r"blocked\s+(?:on|by)\b|"
    r"waiting\s+(?:on|for|until)\b"
    r")",
    re.IGNORECASE,
)

INTRO_PREFIX_BETWEEN_RE = re.compile(
    r"^(?:[\s:,\-\u2013\u2014]*|"
    r"[\s,]*(?:and|or|also|plus|as\s+well\s+as|because(?:\s+of)?|due\s+to|owing\s+to)\s+)$",
    re.IGNORECASE,
)

EXTRA_BLOCKER_CONJUNCTION_RE = re.compile(
    r"\b(?:and|or|plus|because|due\s+to)\b",
    re.IGNORECASE,
)
NON_CAPACITY_BLOCKER_WORD_RE = re.compile(
    r"\b(?:"
    r"approv\w*|stakeholders?|owners?|reviews?|humans?|sign-?offs?|decisions?|feedback|"
    r"input|repl(?:y|ies)|responses?|clearances?|permissions?|legal|security|outages?|"
    r"upstream|ci|checks|(?:ci|pr|hosted|status|required|merge)\s+check|plans?"
    r")\b",
    re.IGNORECASE,
)
NEXT_CHECK_TIMING_TAIL_PAT = (
    r"(?:(?:\s+|,\s*)(?:"
    r"(?:until|before|for|pending|awaiting|till)\s+(?:(?:a|an|the)\s+)?(?:next\s+)?"
    r"(?:scheduled\s+|coordinator\s+)?(?:check|tick|run|poll|cycle|pass|turn|window)|"
    r"at\s+the\s+next\s+(?:scheduled\s+|coordinator\s+)?"
    r"(?:check|tick|run|poll|cycle|pass|turn|window)"
    r"))?"
)
SESSION_CAPACITY_WAIT_SPAN_RE = re.compile(
    r"^[\s:,\-\u2013\u2014(]*(?:(?:on|for|until|at|during|under)\s+)?"
    r"(?:(?:a|an|the|any|next)\s+)?"
    r"(?:"
    r"(?:(?:free|open|available|active|worker|tmux|session|concurrency)\s+)+"
    r"(?:slots?|sessions?|capacity|cap)|"
    r"\d+\s*/\s*\d+\s*(?:(?:active|worker|tmux)\s+)?(?:sessions?|slots?|capacity|cap)"
    r")"
    r"(?:\s+(?:(?:at|under|within)\s+\d+\s*/\s*\d+\s*"
    r"(?:(?:active|worker|tmux|session)\s+)?(?:sessions?|slots?|capacity|cap)|"
    r"to\s+(?:open|free(?:\s+up)?|clear|finish|complete)))?"
    + NEXT_CHECK_TIMING_TAIL_PAT
    + r"[\s)]*$",
    re.IGNORECASE,
)
PR_DRAIN_WAIT_SPAN_RE = re.compile(
    r"^[\s:,\-\u2013\u2014(]*(?:(?:on|for|until|at|during|under)\s+)?"
    r"(?:(?:a|an|the|any|active)\s+)?"
    r"(?:"
    r"pr\s+drain\w*|"
    r"open[- ]pr\s+(?:cap|drain\w*|hysteresis|limit)|"
    r"drain\w*\s+(?:open\s+)?(?:prs?|pull\s+requests?)|"
    r"(?:open\s+)?(?:prs?|pull\s+requests?)\s+(?:to\s+drain|drain\w*|below\s+\d+|under\s+\d+)"
    r")"
    r"(?:\s+(?:(?:below|under|until\s+<=?|<=?)\s*\d+(?:\s+open\s+(?:prs?|pull\s+requests?))?|"
    r"to\s+(?:clear|complete|finish|drain)|active|hysteresis))*"
    + NEXT_CHECK_TIMING_TAIL_PAT
    + r"[\s)]*$",
    re.IGNORECASE,
)
COORDINATED_WAIT_SPLIT_RE = re.compile(
    r",(?![ \t]*(?:"
    r"(?:until|before|for|till|at|during|under|in|on|with|without)\b|"
    r"(?:pending|awaiting)[ \t]+" + NEXT_CHECK_NOUN_LOOKAHEAD_PAT + r"))[ \t]*(?:"
    r"(?:and|or|plus|as\s+well\s+as|because(?:\s+of)?|due\s+to|owing\s+to)\b[ \t]*|"
    r"(?:pending|awaiting)\b(?![ \t]+" + NEXT_CHECK_NOUN_LOOKAHEAD_PAT + r")[ \t]*)?|"
    r"(?<=\S)[ \t]+(?:"
    r"(?:and|or|plus|as\s+well\s+as|because(?:\s+of)?|due\s+to|owing\s+to)\b|"
    r"(?<!\bis)(?<!\bare)(?<!\bwas)(?<!\bwere)(?<!\bbe)(?<!\bbeen)"
    r"(?<!\bstill)(?<!\bremain)(?<!\bremains)"
    r"(?:pending|awaiting)\b(?![ \t]+" + NEXT_CHECK_NOUN_LOOKAHEAD_PAT + r"))(?=[ \t]+\S)",
    re.IGNORECASE,
)
SHARED_REF_LIFECYCLE_SEG_RE = re.compile(
    r"^\s*(?:of\s+)?(?:(?:its|their|the)\s+)?"
    r"(?:hosted\s+ci|ci|required\s+checks?|status\s+checks?|pr\s+checks?|merge\s+checks?|"
    r"checks?|merge(?:ability)?|automerge|rebase|builds?|tests?|pipelines?)"
    r"(?:\s+(?:(?:is|are)\s+(?:still\s+)?(?:running|pending|queued|in\s+progress)|"
    r"to\s+(?:pass|complete|finish|succeed)))?\s*$",
    re.IGNORECASE,
)

BLOCKER_SPAN_STOP_RE = re.compile(
    r"[.;!?]|"
    r":\s*(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b|"
    r"(?<=\s)--\s+(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b|"
    r"(?:,\s*)?\b(?:and|or|also)\s+(?=\b(?:"
    r"status:\s*waiting\b|waiting\s+summary\b|all\s+lanes\s+waiting\b|"
    r"paus(?:e|ed|ing)\s+(?:(?:the\s+)?(?:run|schedule|delivery|check|tick)\b|"
    r"(?:on|for|until|due\s+to|because)\b)|"
    r"blocked\s+(?:on|by)\b|waiting\s+(?:on|for|until)\b"
    r"))|"
    r",\s+(?:so|but|yet|then|while|whereas)\b|"
    r",\s+and\s+(?:(?:now|meanwhile|concurrently)\s+)?"
    r"(?:"
    r"(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b|"
    r"(?:we|coordinator|delivery|independent\s+(?:lanes?|work|issues?)|"
    r"(?:(?:issue|worker|session)\s+)?(?:#\d+|_+|rpi-\d+(?:-[A-Za-z0-9_.-]+)?))\s+"
    r"(?:(?:is|are|has|have)\s+(?:now\s+)?)?"
    r"(?:launch(?:ed|ing|es)|start(?:ed|ing|s)|dispatch(?:ed|ing|es)|spawn(?:ed|ing|s)|"
    r"running|continu(?:e|es|ed|ing)|proceed(?:s|ed|ing))\b"
    r")|"
    r"\bwhile\b|"
    r"\b(?:never|cannot|can't|must\s+not|do\s+not|don't)\b|"
    r"\b(?:before|until|instead\s+of|then|to|and(?:\s+now)?)\s+"
    r"(?:launch\w*|start\w*|dispatch\w*|spawn\w*|continu\w*|proceed\w*)\b",
    re.IGNORECASE,
)

STALE_CARRY_RE = re.compile(
    r"(?:"
    r"\bcopied\s+from\s+(?:prior|previous|earlier|last)\b|"
    r"\bcarried\s+over\s+from\b|"
    r"\bcached\s+from\s+(?:prior|previous|earlier|last)\b|"
    r"\bfrom\s+(?:prior|previous|earlier)\s+(?:handoff|tick|check|snapshot)\b|"
    r"\b(?:counts?|shas?|sessions?)\s+not\s+refreshed\b|"
    r"\bunrefreshed\s+(?:counts?|shas?|sessions?|snapshot)\b|"
    r"\b(?:stale|reused)\s+/tmp/brief"
    r")",
    re.IGNORECASE,
)

ISSUE_COL_HEADERS: frozenset[str] = frozenset({"issue", "issues", "work item", "item"})
STATE_COL_HEADERS: frozenset[str] = frozenset(
    {
        "state",
        "issue state",
        "issue-state",
        "classification",
        "state classification",
        "issue-state classification",
        "category",
    }
)
NON_BLOCKER_COL_RE = re.compile(
    r"\b(?:owner|notes?|summary|title|priority|progress|sprint|wave)\b|^actions?$",
    re.IGNORECASE,
)
BLOCKER_EXPLICIT_COL_RE = re.compile(
    r"\b(?:blockers?|blocking|evidence|links?|dependenc(?:y|ies))\b",
    re.IGNORECASE,
)
BLOCKER_COL_RE = re.compile(
    r"\b(?:blockers?|blocking|evidence|links?|dependenc(?:y|ies)|reasons?|prs?|checks?)\b",
    re.IGNORECASE,
)
KNOWN_METADATA_KEYS: frozenset[str] = frozenset(
    {
        "observed utc",
        "observed_at",
        "observed at",
        "snapshot utc",
        "written utc",
        "written_at",
        "written at",
        "handoff utc",
        "live commands",
        "commands",
        "open issues",
        "open-issue count",
        "open issue count",
        "open issue list",
        "open issues list",
        "open prs",
        "open-pr count",
        "open pr count",
        "active sessions",
        "active tmux sessions",
        "active session status",
        "unclassified issues",
        "unclassified open issues",
        "unassessed closure",
        "unassessed items",
        "head sha",
        "head",
        "current head",
        "source sha",
        "origin/main sha",
        "origin/main",
        "main sha",
        "target/base sha",
        "target sha",
        "base sha",
        "parent-topic sha",
        "target base sha",
    }
)


@dataclass(frozen=True)
class ProhibitionHead:
    start: int
    end: int
    is_modal_neg: bool
    first_tok_idx: int
    inside_literal_end: int | None


@dataclass(frozen=True)
class ClauseTokens:
    start: int
    end: int
    raw: str
    tok_starts: tuple[int, ...]
    tok_ends: tuple[int, ...]
    tok_vals: tuple[str, ...]
    is_verb: tuple[bool, ...]
    prev_non_prep: tuple[int, ...]
    next_non_cont: tuple[int, ...]
    lit_starts: tuple[int, ...]
    lit_ends: tuple[int, ...]
    prohibitions: tuple[ProhibitionHead, ...]
    pm_ends: tuple[int, ...]


@dataclass(frozen=True)
class ClauseIndex:
    raw_text: str
    span_masked_text: str
    clause_starts: tuple[int, ...]
    clause_ends: tuple[int, ...]
    clauses: tuple[ClauseTokens, ...]
    subclause_starts: tuple[int, ...]
    subclause_ends: tuple[int, ...]
    sentence_bounds: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class IssueRow:
    lineno: int
    issue_number: int | None
    raw_issue: str
    state: str
    non_issue_cells: tuple[str, ...]
    blocker_cells: tuple[str, ...]
    has_valid_blocker_link: bool
    broken_anchors: tuple[str, ...] = ()
    mismatched_links: tuple[str, ...] = ()


@dataclass
class ClassificationTable:
    header_line: int
    end_line: int
    rows: list[IssueRow] = field(default_factory=list)


@dataclass
class ParsedTable:
    header_line: int
    end_line: int
    headers: list[str]
    rows: list[tuple[int, list[str]]]


def _is_dated_h2(line: str) -> bool:
    return line.startswith("## ") and bool(ISO_DATE_TOKEN_RE.search(line))


def _normalize_repo_key(raw_repo: str) -> str:
    cleaned = raw_repo.strip().strip("/").lower()
    if not cleaned or cleaned == DEFAULT_LOCAL_REPO:
        return ""
    return cleaned


def _normalize_generic_url(cleaned: str) -> str:
    scheme_end = cleaned.find("://")
    if scheme_end == -1:
        return cleaned.rstrip("/")
    rest = cleaned[scheme_end + 3 :]
    slash_idx = rest.find("/")
    if slash_idx == -1:
        return f"{cleaned[:scheme_end].lower()}://{rest.lower()}"
    path_tail = rest[slash_idx:].rstrip("/")
    return f"{cleaned[:scheme_end].lower()}://{rest[:slash_idx].lower()}{path_tail}"


def _iter_issue_refs(text: str) -> Iterator[tuple[str, int]]:
    """Yield `(repo_key, number)` for `#<n>` and `owner/repo#<n>` in linear O(N) time."""
    for match in HASH_ISSUE_RE.finditer(text):
        hash_pos = match.start()
        if hash_pos > 0 and text[hash_pos - 1] in {"#", "&"}:
            continue
        pos = hash_pos
        while pos > 0 and text[pos - 1] in REPO_PATH_CHARS:
            pos -= 1
        if pos < hash_pos and pos > 0 and text[pos - 1] in {"#", "&", ":", "@"}:
            continue
        prefix = text[pos:hash_pos]
        issue_num = int(match.group(1))
        if not prefix:
            yield ("", issue_num)
            continue
        if "/" not in prefix:
            yield ("", issue_num)
            continue
        parts = prefix.split("/")
        if len(parts) == 2 and parts[0] and parts[1]:
            yield (_normalize_repo_key(prefix), issue_num)


def _extract_url_blocker_refs(url: str) -> list[BlockerRef]:
    """Extract normalized `(repo_key, id_or_url)` references from a URL or path."""
    cleaned = url.strip().rstrip(".,;:!?")
    if not cleaned:
        return []
    gh_m = GITHUB_REPO_ISSUE_PR_URL_RE.match(cleaned)
    if gh_m:
        return [(_normalize_repo_key(gh_m.group(1)), int(gh_m.group(2)))]
    ext_m = EXTERNAL_HOST_ISSUE_PR_URL_RE.match(cleaned)
    if ext_m:
        host = ext_m.group(1).lower()
        repo_path = ext_m.group(2).strip("/").lower()
        key = f"{host}:{repo_path}" if repo_path else host
        return [(key, int(ext_m.group(3)))]
    if cleaned.lower().startswith(("http://", "https://")):
        return [("url", _normalize_generic_url(cleaned))]
    rel_repo_m = RELATIVE_REPO_ISSUE_PR_RE.match(cleaned)
    if rel_repo_m:
        return [(_normalize_repo_key(rel_repo_m.group(1)), int(rel_repo_m.group(2)))]
    return [("", int(n_str)) for n_str in GITHUB_ISSUE_PR_URL_RE.findall(cleaned)]


def _is_bare_self_issue_url(
    url: str,
    issue_number: int | None,
    self_repo_key: str = "",
) -> bool:
    """Return True when `url` points only to the row's own `/issues/<self>` without a comment fragment."""
    if issue_number is None:
        return False
    cleaned = url.strip().rstrip(".,;:!?")
    if not cleaned:
        return False
    if "#" in cleaned:
        base, frag = cleaned.split("#", 1)
        frag_clean = frag.strip()
        if frag_clean and frag_clean != str(issue_number):
            return False
        cleaned = base
    cleaned = cleaned.split("?", 1)[0]
    m = BARE_GITHUB_ISSUE_URL_RE.match(cleaned)
    if not m:
        return False
    repo = m.group(1) or m.group(2)
    num = int(m.group(3))
    if num != issue_number:
        return False
    return repo is None or _normalize_repo_key(repo) == _normalize_repo_key(self_repo_key)


def _extract_refs_from_fragment(
    fragment: str,
    *,
    skip_broken_targets: set[str] | None = None,
    valid_heading_slugs: frozenset[str] | None = None,
    enforce_link_validity: bool = False,
    include_label_refs: bool = True,
    self_issue_number: int | None = None,
    self_repo_key: str = "",
) -> list[BlockerRef]:
    """Extract `BlockerRef` tuples resolving Markdown `[label](target)` pairs first."""
    refs: list[BlockerRef] = []
    seen: set[BlockerRef] = set()

    def _add(ref: BlockerRef) -> None:
        if ref not in seen:
            seen.add(ref)
            refs.append(ref)

    for link_m in MD_LINK_RE.finditer(fragment):
        lbl = link_m.group(1)
        tgt = link_m.group(2).strip()
        if enforce_link_validity:
            if not tgt or tgt.lower().startswith(("javascript:", "data:")):
                continue
            if skip_broken_targets and tgt in skip_broken_targets:
                continue
            if _is_bare_self_issue_url(tgt, self_issue_number, self_repo_key):
                continue
            if tgt.startswith("#") and not GITHUB_FRAGMENT_ANCHOR_RE.match(tgt):
                slug = tgt[1:].strip().lower()
                if not slug or (
                    valid_heading_slugs is not None and slug not in valid_heading_slugs
                ):
                    continue

        target_refs: list[BlockerRef] = []
        inherited_repo = ""
        if tgt.startswith("#"):
            scoped_m = SCOPED_FRAGMENT_ISSUE_RE.match(tgt)
            if scoped_m:
                target_refs.append(("", int(scoped_m.group(1))))
            elif GITHUB_FRAGMENT_ANCHOR_RE.match(tgt):
                target_refs.append(("anchor", tgt.lower()))
            else:
                slug = tgt[1:].strip().lower()
                if slug:
                    target_refs.append(("anchor", f"#{slug}"))
        else:
            target_refs = _extract_url_blocker_refs(tgt)
            gh_prefix_m = GITHUB_REPO_URL_PREFIX_RE.match(tgt)
            if gh_prefix_m:
                inherited_repo = _normalize_repo_key(gh_prefix_m.group(1))
            elif target_refs and isinstance(target_refs[0][1], int):
                inherited_repo = target_refs[0][0]

        target_nums = {val for _rk, val in target_refs if isinstance(val, int)}
        for tref in target_refs:
            _add(tref)

        if include_label_refs:
            for rq, lnum in _iter_issue_refs(lbl):
                if rq:
                    _add((rq, lnum))
                elif lnum in target_nums:
                    continue
                else:
                    _add((inherited_repo, lnum))

    without_md_links = MD_LINK_RE.sub(" ", fragment)
    for url_m in URL_RE.finditer(without_md_links):
        raw_url = url_m.group(0)
        if enforce_link_validity and _is_bare_self_issue_url(
            raw_url, self_issue_number, self_repo_key
        ):
            continue
        for uref in _extract_url_blocker_refs(raw_url):
            _add(uref)

    prose_only = URL_RE.sub(" ", without_md_links)
    for pref in _iter_issue_refs(prose_only):
        _add(pref)
    for anc_m in COMMENT_ANCHOR_RE.finditer(prose_only):
        raw_anc = anc_m.group(0)
        scoped_anc = SCOPED_FRAGMENT_ISSUE_RE.match(raw_anc)
        if scoped_anc:
            _add(("", int(scoped_anc.group(1))))
        else:
            norm_anc = raw_anc.lower() if raw_anc.startswith("#") else f"#{raw_anc.lower()}"
            _add(("anchor", norm_anc))

    return refs


def _iter_unfenced_lines(text: str) -> list[tuple[int, str]]:
    """Return 1-based `(lineno, line)` pairs outside Markdown code fences."""
    out: list[tuple[int, str]] = []
    fence_char = ""
    fence_len = 0
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if match:
            marker = match.group(1)
            if not fence_char:
                fence_char = marker[0]
                fence_len = len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len:
                fence_char = ""
                fence_len = 0
                continue
        if not fence_char:
            out.append((lineno, line))
    return out


def _heading_slug(heading_text: str) -> str:
    cleaned = re.sub(r"[`*_~]", "", heading_text.strip().lower())
    cleaned = re.sub(r"[^a-z0-9\s-]", "", cleaned)
    return re.sub(r"\s+", "-", cleaned).strip("-")


def _strip_md_formatting(value: str) -> str:
    return " ".join(value.strip("`*_~ \t\r\n").split())


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip().removeprefix("|").removesuffix("|")
    return [cell.strip() for cell in stripped.split("|")]


def _is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(TABLE_SEP_CELL_RE.match(cell.replace(" ", "")) for cell in cells)


def _parse_markdown_tables(unfenced: list[tuple[int, str]]) -> list[ParsedTable]:
    tables: list[ParsedTable] = []
    idx = 0
    total = len(unfenced)
    while idx + 1 < total:
        lineno, line = unfenced[idx]
        next_lineno, next_line = unfenced[idx + 1]
        if (
            "|" in line
            and "|" in next_line
            and next_lineno == lineno + 1
            and line.lstrip().startswith("|")
            and next_line.lstrip().startswith("|")
        ):
            headers = [_strip_md_formatting(h).lower() for h in _split_table_row(line)]
            sep_cells = _split_table_row(next_line)
            if (
                len(headers) >= 2
                and len(sep_cells) == len(headers)
                and _is_separator_row(sep_cells)
            ):
                rows: list[tuple[int, list[str]]] = []
                end_line = next_lineno
                idx += 2
                while idx < total:
                    row_lineno, row_line = unfenced[idx]
                    if not row_line.lstrip().startswith("|") or "|" not in row_line:
                        break
                    cells = _split_table_row(row_line)
                    if _is_separator_row(cells):
                        end_line = row_lineno
                        idx += 1
                        continue
                    if len(cells) < len(headers):
                        cells.extend([""] * (len(headers) - len(cells)))
                    rows.append((row_lineno, cells[: len(headers)]))
                    end_line = row_lineno
                    idx += 1
                tables.append(
                    ParsedTable(
                        header_line=lineno,
                        end_line=end_line,
                        headers=headers,
                        rows=rows,
                    )
                )
                continue
        idx += 1
    return tables


def _mask_backtick_or_url(match: re.Match[str]) -> str:
    raw = match.group(0)
    if raw.startswith("`"):
        return "_" * len(raw)
    core = raw.rstrip(".;!?:,")
    return ("_" * len(core)) + raw[len(core) :]


def _has_zero_unclassified_guard(clause: str) -> bool:
    pre_m = ZERO_UNCLASSIFIED_PRECOND_RE.search(clause)
    if pre_m is None:
        return False
    return ZERO_UNCLASSIFIED_TARGET_RE.search(clause, pre_m.end()) is not None


def _has_conditional_guard_suffix(trailing_clause: str) -> bool:
    """Constant-time check whether a `<= 160`-char suffix ends in `only after` / `permitted only when`."""
    raw_tail = trailing_clause.rstrip(" \t\"'`").rsplit(None, 8)
    if len(raw_tail) < 2:
        return False
    tokens = [tok.lower() for tok in raw_tail[-7:]]
    popped = 0
    while tokens and popped < 4 and tokens[-1] in TRAILING_PREP_DET_TOKENS:
        tokens.pop()
        popped += 1
    if len(tokens) >= 2 and tokens[-2].lstrip("\"'`([") == "only" and tokens[-1] == "after":
        return True
    return (
        len(tokens) >= 3
        and tokens[-3].lstrip("\"'`([") == "permitted"
        and tokens[-2:] == ["only", "when"]
    )


def _build_clause_tokens(
    raw_text: str,
    span_masked_text: str,
    c_start: int,
    c_end: int,
) -> ClauseTokens:
    clause_raw = raw_text[c_start:c_end]
    clause_masked = span_masked_text[c_start:c_end]
    lit_spans = [(m.start(), m.end()) for m in INLINE_LITERAL_SPAN_RE.finditer(clause_raw)]
    lit_starts = tuple(s for s, _e in lit_spans)
    lit_ends = tuple(e for _s, e in lit_spans)

    tok_starts_l: list[int] = []
    tok_ends_l: list[int] = []
    tok_vals_l: list[str] = []
    cursor = 0
    for lit_s, lit_e in lit_spans:
        if cursor < lit_s:
            for wm in WORD_TOKEN_RE.finditer(clause_raw, cursor, lit_s):
                tok_starts_l.append(wm.start())
                tok_ends_l.append(wm.end())
                tok_vals_l.append(wm.group(0).lower())
        tok_starts_l.append(lit_s)
        tok_ends_l.append(lit_e)
        tok_vals_l.append("qtok")
        cursor = lit_e
    if cursor < len(clause_raw):
        for wm in WORD_TOKEN_RE.finditer(clause_raw, cursor):
            tok_starts_l.append(wm.start())
            tok_ends_l.append(wm.end())
            tok_vals_l.append(wm.group(0).lower())

    total_toks = len(tok_vals_l)
    is_verb_l = [bool(GOV_VERB_TOKEN_RE.match(tv)) for tv in tok_vals_l]
    is_prep_l = [tv in TRAILING_PREP_DET_TOKENS for tv in tok_vals_l]
    is_cont_l = [
        (tv in GOV_CONTINUATION_TOKENS) or is_verb_l[idx] for idx, tv in enumerate(tok_vals_l)
    ]

    prev_non_prep_l = [-1] * total_toks
    last_non_prep = -1
    for idx in range(total_toks):
        if not is_prep_l[idx]:
            last_non_prep = idx
        prev_non_prep_l[idx] = last_non_prep

    next_non_cont_l = [total_toks] * total_toks
    nxt_non_cont = total_toks
    for idx in range(total_toks - 1, -1, -1):
        if not is_cont_l[idx]:
            nxt_non_cont = idx
        next_non_cont_l[idx] = nxt_non_cont

    prohibitions_l: list[ProhibitionHead] = []
    pm_ends_l: list[int] = []
    for pm in PROHIBITION_HEAD_RE.finditer(clause_masked):
        li = bisect_right(lit_starts, pm.start()) - 1
        inside_lit_end = lit_ends[li] if (li >= 0 and pm.start() < lit_ends[li]) else None
        first_tok_idx = bisect_left(tok_starts_l, pm.end())
        prohibitions_l.append(
            ProhibitionHead(
                start=pm.start(),
                end=pm.end(),
                is_modal_neg=bool(pm.group(1)),
                first_tok_idx=first_tok_idx,
                inside_literal_end=inside_lit_end,
            )
        )
        pm_ends_l.append(pm.end())

    return ClauseTokens(
        start=c_start,
        end=c_end,
        raw=clause_raw,
        tok_starts=tuple(tok_starts_l),
        tok_ends=tuple(tok_ends_l),
        tok_vals=tuple(tok_vals_l),
        is_verb=tuple(is_verb_l),
        prev_non_prep=tuple(prev_non_prep_l),
        next_non_cont=tuple(next_non_cont_l),
        lit_starts=lit_starts,
        lit_ends=lit_ends,
        prohibitions=tuple(prohibitions_l),
        pm_ends=tuple(pm_ends_l),
    )


def _mask_inline_literal_interior(match: re.Match[str]) -> str:
    s = match.group(0)
    if len(s) <= 2:
        return s
    return s[0] + ("_" * (len(s) - 2)) + s[-1]


def _build_clause_index(text: str) -> ClauseIndex:
    """Build single-pass O(N) clause/prohibition/sentence index for a normalized prose block."""
    span_masked = BACKTICK_OR_URL_RE.sub(_mask_backtick_or_url, text)
    clause_split_masked = INLINE_LITERAL_SPAN_RE.sub(_mask_inline_literal_interior, span_masked)

    c_starts: list[int] = []
    c_ends: list[int] = []
    clauses: list[ClauseTokens] = []
    sub_starts: list[int] = []
    sub_ends: list[int] = []

    def _append_clause(cs: int, ce: int) -> None:
        c_starts.append(cs)
        c_ends.append(ce)
        clauses.append(_build_clause_tokens(text, span_masked, cs, ce))
        cur_sub = cs
        for sub_m in SUBCLAUSE_SPLIT_RE.finditer(span_masked, cs, ce):
            sub_starts.append(cur_sub)
            sub_ends.append(sub_m.start())
            cur_sub = sub_m.end()
        sub_starts.append(cur_sub)
        sub_ends.append(ce)

    last_start = 0
    for sep_m in CLAUSE_SPLIT_RE.finditer(clause_split_masked):
        _append_clause(last_start, sep_m.start())
        last_start = sep_m.end()
    _append_clause(last_start, len(text))

    s_bounds: list[tuple[int, int]] = []
    s_start = 0
    for sent_m in SENTENCE_SPLIT_RE.finditer(span_masked):
        s_bounds.append((s_start, sent_m.start()))
        s_start = sent_m.end()
    s_bounds.append((s_start, len(text)))

    return ClauseIndex(
        raw_text=text,
        span_masked_text=span_masked,
        clause_starts=tuple(c_starts),
        clause_ends=tuple(c_ends),
        clauses=tuple(clauses),
        subclause_starts=tuple(sub_starts),
        subclause_ends=tuple(sub_ends),
        sentence_bounds=tuple(s_bounds),
    )


def _tokens_govern_claim(tokens: list[str], *, is_modal_neg: bool) -> bool:
    trimmed = list(tokens)
    while trimmed and trimmed[-1] in TRAILING_PREP_DET_TOKENS:
        trimmed.pop()
    if is_modal_neg:
        if not trimmed or trimmed == ["be"]:
            return True
        return bool(GOV_VERB_TOKEN_RE.match(trimmed[0])) and all(
            tok in GOV_CONTINUATION_TOKENS or bool(GOV_VERB_TOKEN_RE.match(tok))
            for tok in trimmed[1:]
        )
    return all(
        tok in GOV_CONTINUATION_TOKENS or bool(GOV_VERB_TOKEN_RE.match(tok)) for tok in trimmed
    )


def _fallback_prohibition_check(
    ct: ClauseTokens,
    clause_raw: str,
    rel_pos: int,
    *,
    only_literal_end: int | None = None,
) -> bool:
    pm_hi = bisect_right(ct.pm_ends, rel_pos)
    for pm in reversed(ct.prohibitions[max(0, pm_hi - 4) : pm_hi]):
        if only_literal_end is not None:
            if pm.inside_literal_end != only_literal_end:
                continue
        elif pm.inside_literal_end is not None and rel_pos >= pm.inside_literal_end:
            continue
        if CLAUSE_SPLIT_RE.search(clause_raw, pm.end, rel_pos) is not None:
            continue
        rest = clause_raw[pm.end : rel_pos]
        masked_rest = INLINE_LITERAL_SPAN_RE.sub(" qtok ", rest)
        tokens = WORD_TOKEN_RE.findall(masked_rest.lower())
        if _tokens_govern_claim(tokens, is_modal_neg=pm.is_modal_neg):
            return True
    return False


def _is_claim_negated_at(
    idx: ClauseIndex,
    match_start: int,
    *,
    allow_conditional_guards: bool = True,
) -> bool:
    """Return True in O(log N) when a same-clause prohibition governs `match_start`."""
    if match_start <= 0:
        return False
    ci = bisect_right(idx.clause_starts, match_start) - 1
    if ci < 0:
        return False
    ct = idx.clauses[ci]
    if match_start > ct.end:
        return False
    rel_pos = match_start - ct.start
    if rel_pos <= 0:
        return False

    if allow_conditional_guards:
        tail_start = max(ct.start, match_start - 160)
        if _has_conditional_guard_suffix(idx.raw_text[tail_start:match_start]):
            return True

    if not ct.prohibitions:
        return False

    clause_raw = ct.raw
    li = bisect_right(ct.lit_starts, rel_pos - 1) - 1
    if li >= 0 and ct.lit_starts[li] < rel_pos < ct.lit_ends[li]:
        if _fallback_prohibition_check(
            ct,
            clause_raw,
            rel_pos,
            only_literal_end=ct.lit_ends[li],
        ):
            return True
        rel_pos = ct.lit_starts[li]

    end_tok_excl = bisect_right(ct.tok_ends, rel_pos)
    if end_tok_excl < len(ct.tok_starts) and ct.tok_starts[end_tok_excl] < rel_pos:
        return _fallback_prohibition_check(ct, clause_raw, rel_pos)

    last_raw_idx = end_tok_excl - 1
    pm_hi = bisect_right(ct.pm_ends, rel_pos)
    for pm in reversed(ct.prohibitions[max(0, pm_hi - 4) : pm_hi]):
        if pm.inside_literal_end is not None and rel_pos >= pm.inside_literal_end:
            continue
        first_idx = pm.first_tok_idx
        last_idx = ct.prev_non_prep[last_raw_idx] if last_raw_idx >= first_idx else first_idx - 1
        if pm.is_modal_neg:
            if last_idx < first_idx:
                return True
            if last_idx == first_idx and ct.tok_vals[first_idx] == "be":
                return True
            if ct.is_verb[first_idx] and (
                first_idx + 1 > last_idx or ct.next_non_cont[first_idx + 1] > last_idx
            ):
                return True
        elif last_idx < first_idx or ct.next_non_cont[first_idx] > last_idx:
            return True
    return False


def _is_claim_negated(
    line: str,
    match_start: int,
    *,
    allow_conditional_guards: bool = True,
) -> bool:
    """Convenience wrapper building a `ClauseIndex` when checking a standalone clause."""
    if match_start <= 0:
        return False
    return _is_claim_negated_at(
        _build_clause_index(line),
        match_start,
        allow_conditional_guards=allow_conditional_guards,
    )


def _has_global_wait_or_pause(text: str, idx: ClauseIndex) -> bool:
    """Linear-time O(N) check for global waiting/pause or sentence-scoped hold-before-continuing."""
    if any(not _is_claim_negated_at(idx, m.start()) for m in DIRECT_GLOBAL_WAIT_RE.finditer(text)):
        return True
    for s_start, s_end in idx.sentence_bounds:
        if s_start >= s_end:
            continue
        last_hold_start: int | None = None
        for hm in HOLD_CONTINUATION_RE.finditer(text, s_start, s_end):
            last_hold_start = hm.start()
        if last_hold_start is None:
            continue
        for wm in WAITING_ON_FOR_RE.finditer(text, s_start, last_hold_start):
            if not _is_claim_negated_at(idx, wm.start()):
                return True
    return False


def _launched_ready_issues_in_current_tick(
    text: str,
    idx: ClauseIndex,
    ready_issue_nums: set[int],
) -> set[int]:
    """Return `ready_issue_nums` actively launched in `text` in linear O(N) time."""
    launched: set[int] = set()
    if not ready_issue_nums:
        return launched

    non_current_by_subclause: dict[int, bool] = {}
    min_hold_end_by_subclause: dict[int, int] = {}
    masked = idx.span_masked_text
    for m in READY_LAUNCH_RE.finditer(text):
        raw_num = next((g for g in m.groups() if g is not None), None)
        if raw_num is None:
            continue
        target_num = int(raw_num)
        if target_num not in ready_issue_nums or target_num in launched:
            continue
        if _is_claim_negated_at(idx, m.start()):
            continue

        si = bisect_right(idx.subclause_starts, m.start()) - 1
        sub_start = idx.subclause_starts[si] if si >= 0 else 0
        sub_end = idx.subclause_ends[si] if si >= 0 else len(text)

        if si not in non_current_by_subclause:
            non_current_by_subclause[si] = bool(
                NON_CURRENT_LAUNCH_SUBCLAUSE_RE.search(masked, sub_start, sub_end)
            )
        if non_current_by_subclause[si]:
            continue

        if si not in min_hold_end_by_subclause:
            hm_first = LAUNCH_SUBCLAUSE_NEG_OR_HOLD_RE.search(masked, sub_start, sub_end)
            min_hold_end_by_subclause[si] = hm_first.end() if hm_first is not None else -1
        min_hold_end = min_hold_end_by_subclause[si]
        if min_hold_end != -1 and min_hold_end <= m.start():
            continue
        launched.add(target_num)
    return launched


def _strip_trailing_trigger_bridge(span_masked: str, start: int, end: int) -> int:
    """Trim trailing coordinating/causal bridge words before the next trigger in O(tail_len)."""
    r = end
    while r > start and span_masked[r - 1].isspace():
        r -= 1
    if r <= start:
        return end

    def _consume_word_back(pos: int, word: str) -> int | None:
        w_start = pos - len(word)
        if w_start < start or span_masked[w_start:pos].lower() != word:
            return None
        if w_start > start and (
            span_masked[w_start - 1].isalnum() or span_masked[w_start - 1] == "_"
        ):
            return None
        return w_start

    def _consume_ws_back(pos: int) -> int:
        p = pos
        while p > start and span_masked[p - 1].isspace():
            p -= 1
        return p

    conn_start: int | None = None
    p_as2 = _consume_word_back(r, "as")
    if p_as2 is not None:
        p_ws1 = _consume_ws_back(p_as2)
        if p_ws1 < p_as2:
            p_well = _consume_word_back(p_ws1, "well")
            if p_well is not None:
                p_ws2 = _consume_ws_back(p_well)
                if p_ws2 < p_well:
                    conn_start = _consume_word_back(p_ws2, "as")
    if conn_start is None:
        p_of = _consume_word_back(r, "of")
        if p_of is not None:
            p_ws = _consume_ws_back(p_of)
            if p_ws < p_of:
                conn_start = _consume_word_back(p_ws, "because")
    if conn_start is None:
        p_to = _consume_word_back(r, "to")
        if p_to is not None:
            p_ws = _consume_ws_back(p_to)
            if p_ws < p_to:
                conn_start = _consume_word_back(p_ws, "due")
                if conn_start is None:
                    conn_start = _consume_word_back(p_ws, "owing")
    if conn_start is None:
        for kw in ("because", "also", "plus", "and", "or"):
            conn_start = _consume_word_back(r, kw)
            if conn_start is not None:
                break

    if conn_start is not None:
        p = _consume_ws_back(conn_start)
        if p > start and span_masked[p - 1] == ",":
            return p - 1
        if p < conn_start:
            return p

    if span_masked[r - 1] == ",":
        return r - 1
    return end


def _is_exempt_capacity_or_drain_wait(
    target_span: str,
    *,
    at_session_capacity: bool,
    pr_drain_active: bool,
) -> bool:
    """Return True only when `target_span` waits strictly on slot capacity or PR drain."""
    if not (at_session_capacity or pr_drain_active):
        return False
    if EXTRA_BLOCKER_CONJUNCTION_RE.search(target_span):
        return False
    if NON_CAPACITY_BLOCKER_WORD_RE.search(target_span):
        return False
    if at_session_capacity and SESSION_CAPACITY_WAIT_SPAN_RE.search(target_span):
        return True
    return bool(pr_drain_active and PR_DRAIN_WAIT_SPAN_RE.search(target_span))


def _extract_wait_and_blocker_spans(
    text: str,
    idx: ClauseIndex,
    *,
    at_session_capacity: bool = False,
    pr_drain_active: bool = False,
) -> tuple[list[BlockerRef], bool]:
    """Extract deduplicated `BlockerRef` tuples and detect uncited non-capacity waits in O(N)."""
    cited: list[BlockerRef] = []
    seen: set[BlockerRef] = set()
    has_uncited_wait = False
    triggers = [
        tm
        for tm in WAIT_OR_BLOCKER_SPAN_TRIGGER_RE.finditer(text)
        if not _is_claim_negated_at(idx, tm.start())
    ]
    for i, tm in enumerate(triggers):
        next_start = triggers[i + 1].start() if i + 1 < len(triggers) else len(text)
        if i + 1 < len(triggers) and INTRO_PREFIX_BETWEEN_RE.match(text[tm.end() : next_start]):
            continue
        stop_m = BLOCKER_SPAN_STOP_RE.search(idx.span_masked_text, tm.end(), next_start)
        if stop_m is not None:
            end_pos = stop_m.start()
        else:
            end_pos = (
                _strip_trailing_trigger_bridge(idx.span_masked_text, tm.end(), next_start)
                if i + 1 < len(triggers)
                else next_start
            )
        target_span = text[tm.end() : end_pos] if tm.end() < end_pos else ""
        if not target_span.strip():
            if not _is_exempt_capacity_or_drain_wait(
                target_span,
                at_session_capacity=at_session_capacity,
                pr_drain_active=pr_drain_active,
            ):
                has_uncited_wait = True
            continue

        link_masked_span = MD_LINK_RE.sub(
            lambda m: "_" * len(m.group(0)),
            idx.span_masked_text[tm.end() : end_pos],
        )
        segments: list[str] = []
        seg_start = 0
        for split_m in COORDINATED_WAIT_SPLIT_RE.finditer(link_masked_span):
            segments.append(target_span[seg_start : split_m.start()])
            seg_start = split_m.end()
        segments.append(target_span[seg_start:])

        seg_refs_list: list[list[BlockerRef]] = []
        for seg in segments:
            seg_refs = _extract_refs_from_fragment(
                seg,
                enforce_link_validity=False,
                include_label_refs=True,
            )
            seg_refs_list.append(seg_refs)
            for ref in seg_refs:
                if ref not in seen:
                    seen.add(ref)
                    cited.append(ref)

        n_seg = len(segments)
        has_seg_ref = [bool(sr) for sr in seg_refs_list]
        is_life_seg = [bool(SHARED_REF_LIFECYCLE_SEG_RE.match(seg)) for seg in segments]
        life_attached = [False] * n_seg
        cited_chain = False
        for j in range(n_seg):
            if has_seg_ref[j]:
                cited_chain = True
            elif is_life_seg[j] and cited_chain:
                life_attached[j] = True
            else:
                cited_chain = False
        cited_chain = False
        for j in range(n_seg - 1, -1, -1):
            if has_seg_ref[j]:
                cited_chain = True
            elif is_life_seg[j] and cited_chain:
                life_attached[j] = True
            else:
                cited_chain = False

        for j, seg in enumerate(segments):
            if has_seg_ref[j] or life_attached[j]:
                continue
            if _is_exempt_capacity_or_drain_wait(
                seg,
                at_session_capacity=at_session_capacity,
                pr_drain_active=pr_drain_active,
            ):
                continue
            has_uncited_wait = True
    return cited, has_uncited_wait


def _is_known_metadata_line(line: str) -> bool:
    kv_m = KV_LINE_RE.match(line)
    if kv_m is None or not kv_m.group(2).strip():
        return False
    return _strip_md_formatting(kv_m.group(1)).lower() in KNOWN_METADATA_KEYS


def _iter_section_prose_blocks(
    section_lines: list[tuple[int, str]],
    table_line_numbers: set[int] | None = None,
) -> list[tuple[int, str]]:
    """Collapse hard-wrapped Markdown paragraphs, list items, and blockquotes into blocks."""
    skip_lines = table_line_numbers or set()
    blocks: list[tuple[int, str]] = []
    current_start: int | None = None
    current_parts: list[str] = []
    current_bq_depth = 0
    current_is_metadata = False
    prev_lineno: int | None = None

    def _flush() -> None:
        nonlocal current_start, current_parts, current_bq_depth, current_is_metadata
        if current_parts and current_start is not None:
            if len(current_parts) == 1:
                blocks.append((current_start, current_parts[0]))
            else:
                blocks.append(
                    (
                        current_start,
                        current_parts[0].rstrip() + " " + " ".join(current_parts[1:]),
                    )
                )
        current_start = None
        current_parts = []
        current_bq_depth = 0
        current_is_metadata = False

    for lineno, raw_line in section_lines:
        if lineno in skip_lines:
            _flush()
            prev_lineno = None
            continue
        if prev_lineno is not None and lineno != prev_lineno + 1:
            _flush()
        prev_lineno = lineno

        bq_m = BLOCKQUOTE_PREFIX_RE.match(raw_line)
        if bq_m:
            bq_depth = bq_m.group(1).count(">")
            body = bq_m.group(2)
        else:
            bq_depth = 0
            body = raw_line

        stripped = body.strip()
        if not stripped or stripped.startswith("|"):
            _flush()
            continue

        if current_parts and bq_depth != current_bq_depth:
            _flush()

        if HEADING_RE.match(stripped):
            _flush()
            blocks.append((lineno, stripped))
            continue

        is_list_item = bool(LIST_MARKER_RE.match(stripped))
        is_metadata = _is_known_metadata_line(stripped)
        is_indented_cont = body.startswith((" ", "\t")) and not is_list_item

        if current_parts and (
            is_list_item or is_metadata or (current_is_metadata and not is_indented_cont)
        ):
            _flush()

        if current_start is None:
            current_start = lineno
            current_bq_depth = bq_depth
            current_is_metadata = is_metadata
            current_parts.append(stripped if bq_depth > 0 else body.rstrip("\r\n"))
        else:
            current_parts.append(stripped)

    _flush()
    return blocks


def _iter_normalized_prose_clauses(
    unfenced: list[tuple[int, str]],
) -> list[tuple[int, str]]:
    """Collapse hard-wrapped Markdown paragraphs/bullets/blockquotes into sentence clauses."""
    clauses: list[tuple[int, str]] = []
    for start_lineno, block_text in _iter_section_prose_blocks(unfenced):
        joined = " ".join(block_text.split())
        if not joined:
            continue
        masked = BACKTICK_OR_URL_RE.sub(_mask_backtick_or_url, joined)
        last_idx = 0
        for sep_m in re.finditer(r"[.;!?](?=\s|$)", masked):
            seg = joined[last_idx : sep_m.start()].strip()
            if seg:
                clauses.append((start_lineno, seg))
            last_idx = sep_m.end()
        tail = joined[last_idx:].strip()
        if tail:
            clauses.append((start_lineno, tail))
    return clauses


def _find_broken_local_anchors(
    issue_number: int | None,
    cells: tuple[str, ...],
    valid_heading_slugs: frozenset[str],
) -> tuple[str, ...]:
    broken: list[str] = []
    joined = " | ".join(cells)
    for _label, target in MD_LINK_RE.findall(joined):
        cleaned_target = target.strip()
        if not cleaned_target.startswith("#"):
            continue
        if GITHUB_FRAGMENT_ANCHOR_RE.match(cleaned_target):
            continue
        slug = cleaned_target[1:].strip().lower()
        if not slug or (issue_number is not None and slug == str(issue_number)):
            continue
        if slug not in valid_heading_slugs:
            broken.append(cleaned_target)
    return tuple(broken)


def _inspect_blocker_links(
    issue_number: int | None,
    blocker_cells: tuple[str, ...],
    valid_heading_slugs: frozenset[str],
) -> tuple[bool, tuple[str, ...], tuple[str, ...]]:
    """Verify concrete link in blocker/evidence columns, rejecting self-only or mismatched links."""
    joined = " | ".join(blocker_cells)
    has_valid_link = False
    broken_anchors: list[str] = []
    mismatched_links: list[str] = []

    if COMMENT_ANCHOR_RE.search(joined):
        has_valid_link = True

    for label, target in MD_LINK_RE.findall(joined):
        cleaned_target = target.strip()
        if not cleaned_target:
            continue
        if cleaned_target.lower().startswith(("javascript:", "data:")):
            continue

        is_bare_self_url = _is_bare_self_issue_url(cleaned_target, issue_number)
        target_issue_pr_refs: set[tuple[str, int]] = set()
        inherited_repo = ""
        if cleaned_target.startswith("#"):
            scoped_m = SCOPED_FRAGMENT_ISSUE_RE.match(cleaned_target)
            if scoped_m:
                target_issue_pr_refs.add(("", int(scoped_m.group(1))))
            if GITHUB_FRAGMENT_ANCHOR_RE.match(cleaned_target):
                has_valid_link = True
            else:
                slug = cleaned_target[1:].strip().lower()
                if not slug or (issue_number is not None and slug == str(issue_number)):
                    pass
                elif slug in valid_heading_slugs:
                    has_valid_link = True
                else:
                    broken_anchors.append(cleaned_target)
        else:
            if not is_bare_self_url:
                has_valid_link = True
            for rk, rval in _extract_url_blocker_refs(cleaned_target):
                if isinstance(rval, int):
                    target_issue_pr_refs.add((rk, rval))
            gh_prefix_m = GITHUB_REPO_URL_PREFIX_RE.match(cleaned_target)
            if gh_prefix_m:
                inherited_repo = _normalize_repo_key(gh_prefix_m.group(1))
            elif target_issue_pr_refs:
                inherited_repo = next(iter(target_issue_pr_refs))[0]

        for rq, lnum in _iter_issue_refs(label):
            eff_repo = rq if rq else inherited_repo
            if eff_repo == "" and issue_number is not None and lnum == issue_number:
                continue
            if (eff_repo, lnum) not in target_issue_pr_refs:
                lbl_disp = f"{eff_repo}#{lnum}" if eff_repo else f"#{lnum}"
                mismatched_links.append(f"{lbl_disp} -> {cleaned_target}")

    without_md_links = MD_LINK_RE.sub(" ", joined)
    if not has_valid_link:
        for url_m in URL_RE.finditer(without_md_links):
            if not _is_bare_self_issue_url(url_m.group(0), issue_number):
                has_valid_link = True
                break

    if not has_valid_link:
        prose_without_links = URL_RE.sub(" ", without_md_links)
        for repo_key, ref_num in _iter_issue_refs(prose_without_links):
            if repo_key or issue_number is None or ref_num != issue_number:
                has_valid_link = True
                break

    return has_valid_link, tuple(broken_anchors), tuple(mismatched_links)


def _has_non_bare_self_link(
    issue_number: int | None,
    blocker_cells: tuple[str, ...],
    valid_heading_slugs: frozenset[str] = frozenset(),
) -> bool:
    """Verify concrete link in blocker columns, rejecting bare same-issue `#<self>`."""
    has_valid_link, _broken, _mismatched = _inspect_blocker_links(
        issue_number,
        blocker_cells,
        valid_heading_slugs,
    )
    return has_valid_link


def _parse_issue_cell(
    raw_issue: str,
    valid_heading_slugs: frozenset[str],
) -> tuple[int | None, tuple[str, ...]]:
    """Parse a single local `#<n>` or `[#<n>](url)` Issue column cell."""
    cleaned_cell = _strip_md_formatting(raw_issue)
    plain_m = PLAIN_SINGLE_ISSUE_CELL_RE.match(cleaned_cell)
    if plain_m:
        return int(plain_m.group(1)), ()

    link_m = LINKED_SINGLE_ISSUE_CELL_RE.match(cleaned_cell)
    if not link_m:
        return None, ()

    label_clean = _strip_md_formatting(link_m.group(1))
    target_clean = link_m.group(2).strip()
    num_m = PLAIN_SINGLE_ISSUE_CELL_RE.match(label_clean)
    if not num_m or not target_clean:
        return None, ()
    issue_num = int(num_m.group(1))

    if target_clean.lower().startswith(("javascript:", "data:")):
        return None, ()
    if target_clean.startswith("#"):
        if GITHUB_FRAGMENT_ANCHOR_RE.match(target_clean):
            scoped_m = re.match(r"^#(\d+)#", target_clean)
            if scoped_m and int(scoped_m.group(1)) != issue_num:
                return None, ()
            return issue_num, ()
        slug = target_clean[1:].strip().lower()
        if not slug or slug == str(issue_num):
            return None, ()
        if slug not in valid_heading_slugs:
            return None, (target_clean,)
        return issue_num, ()

    gh_repo_m = GITHUB_REPO_URL_PREFIX_RE.match(target_clean)
    if gh_repo_m and _normalize_repo_key(gh_repo_m.group(1)) != "":
        return None, ()
    url_issue_nums = [int(n) for n in GITHUB_ISSUES_ONLY_URL_RE.findall(target_clean)]
    if url_issue_nums and any(n != issue_num for n in url_issue_nums):
        return None, ()
    return issue_num, ()


def _is_non_blocker_col_header(header: str) -> bool:
    if BLOCKER_EXPLICIT_COL_RE.search(header):
        return False
    if NON_BLOCKER_COL_RE.search(header):
        return True
    return bool(re.search(r"\bnext\b", header) and re.search(r"\b(?:actions?|steps?)\b", header))


def _select_blocker_col_indices(
    headers: list[str],
    issue_col: int,
    state_col: int,
) -> tuple[int, ...]:
    explicit_cols: list[int] = []
    fallback_cols: list[int] = []
    for idx, header in enumerate(headers):
        if idx in (issue_col, state_col):
            continue
        if _is_non_blocker_col_header(header):
            continue
        fallback_cols.append(idx)
        if BLOCKER_COL_RE.search(header):
            explicit_cols.append(idx)
    return tuple(explicit_cols if explicit_cols else fallback_cols)


def _extract_verified_evidence_refs(
    issue_number: int | None,
    blocker_cells: tuple[str, ...],
    broken_anchors: tuple[str, ...],
    valid_heading_slugs: frozenset[str],
) -> set[BlockerRef]:
    """Extract verified non-self `BlockerRef` tuples from scoped blocker cells."""
    joined = " | ".join(blocker_cells)
    extracted = _extract_refs_from_fragment(
        joined,
        skip_broken_targets=set(broken_anchors),
        valid_heading_slugs=valid_heading_slugs,
        enforce_link_validity=True,
        include_label_refs=False,
        self_issue_number=issue_number,
    )
    return {
        (repo_key, val)
        for repo_key, val in extracted
        if repo_key != "" or issue_number is None or val != issue_number
    }


def _extract_classification_tables(
    tables: list[ParsedTable],
    valid_heading_slugs: frozenset[str] = frozenset(),
) -> list[ClassificationTable]:
    extracted: list[ClassificationTable] = []
    for table in tables:
        issue_col: int | None = None
        state_col: int | None = None
        for idx, header in enumerate(table.headers):
            if issue_col is None and header in ISSUE_COL_HEADERS:
                issue_col = idx
            elif state_col is None and header in STATE_COL_HEADERS:
                state_col = idx
        if issue_col is None or state_col is None:
            continue
        blocker_col_indices = _select_blocker_col_indices(table.headers, issue_col, state_col)
        blocker_col_set = set(blocker_col_indices)
        parsed_rows: list[IssueRow] = []
        for row_lineno, cells in table.rows:
            raw_issue = cells[issue_col].strip()
            issue_num, issue_broken_anchors = _parse_issue_cell(raw_issue, valid_heading_slugs)
            norm_state = _strip_md_formatting(cells[state_col]).lower()
            other_cells = tuple(c for i, c in enumerate(cells) if i not in (issue_col, state_col))
            blocker_cells = tuple(cells[i] for i in blocker_col_indices)
            non_blocker_other = tuple(
                c
                for i, c in enumerate(cells)
                if i not in (issue_col, state_col) and i not in blocker_col_set
            )
            has_link, blocker_broken_anchors, mismatched_links = _inspect_blocker_links(
                issue_num,
                blocker_cells,
                valid_heading_slugs,
            )
            extra_broken_anchors = _find_broken_local_anchors(
                issue_num,
                non_blocker_other,
                valid_heading_slugs,
            )
            parsed_rows.append(
                IssueRow(
                    lineno=row_lineno,
                    issue_number=issue_num,
                    raw_issue=raw_issue,
                    state=norm_state,
                    non_issue_cells=other_cells,
                    blocker_cells=blocker_cells,
                    has_valid_blocker_link=has_link,
                    broken_anchors=(
                        issue_broken_anchors + blocker_broken_anchors + extra_broken_anchors
                    ),
                    mismatched_links=mismatched_links,
                )
            )
        extracted.append(
            ClassificationTable(
                header_line=table.header_line,
                end_line=table.end_line,
                rows=parsed_rows,
            )
        )
    return extracted


def _split_handoff_sections(
    unfenced: list[tuple[int, str]],
) -> list[list[tuple[int, str]]]:
    """Split append-only multi-date checkpoint files by dated H2 sections."""
    dated_indices = [i for i, (_ln, line) in enumerate(unfenced) if _is_dated_h2(line)]
    if len(dated_indices) < 2:
        return [unfenced]
    sections: list[list[tuple[int, str]]] = []
    for pos, start_idx in enumerate(dated_indices):
        end_idx = dated_indices[pos + 1] if pos + 1 < len(dated_indices) else len(unfenced)
        sections.append(unfenced[start_idx:end_idx])
    return sections


def _parse_iso_utc(raw: str) -> datetime | None:
    token = _strip_md_formatting(raw).split()[0] if _strip_md_formatting(raw) else ""
    if not token:
        return None
    if token.endswith("Z"):
        token = token[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(token)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _shas_compatible(sha_a: str, sha_b: str) -> bool:
    low_a = sha_a.lower()
    low_b = sha_b.lower()
    return low_a.startswith(low_b) or low_b.startswith(low_a)


def check_agent_instructions(agent_path: Path, root: Path | None = None) -> list[str]:
    """Validate `.github/agents/ama-backlog-delivery-coordinator.agent.md` contract."""
    repo_root = (root or ROOT).resolve()
    resolved = agent_path.resolve()
    try:
        display = resolved.relative_to(repo_root).as_posix()
    except ValueError:
        display = agent_path.as_posix()

    if not resolved.is_file():
        return [f"{display}:1: missing-agent-file: coordinator instruction file not found"]

    text = resolved.read_text(encoding="utf-8")
    lines = text.splitlines()
    violations: list[str] = []

    if not lines or lines[0].strip() != "---":
        violations.append(f"{display}:1: invalid-frontmatter: missing opening YAML frontmatter")
    else:
        closing_idx: int | None = None
        for idx in range(1, min(len(lines), 40)):
            if lines[idx].strip() == "---":
                closing_idx = idx
                break
        if closing_idx is None:
            violations.append(f"{display}:1: invalid-frontmatter: unclosed YAML frontmatter")
        else:
            fm_keys: dict[str, str] = {}
            for fm_line in lines[1:closing_idx]:
                if ":" in fm_line:
                    key, val = fm_line.split(":", 1)
                    fm_keys[key.strip()] = val.strip().strip("\"'")
            for req_key in ("name", "description"):
                if not fm_keys.get(req_key):
                    violations.append(
                        f"{display}:1: invalid-frontmatter: missing non-empty `{req_key}`"
                    )

    unfenced = _iter_unfenced_lines(text)
    unfenced_body = "\n".join(line for _ln, line in unfenced)
    lowered_body = unfenced_body.lower()

    for category in REQUIRED_CATEGORIES:
        if category not in lowered_body:
            violations.append(
                f"{display}:1: missing-classification-category: "
                f"required issue-state category `{category}` missing from instructions"
            )

    for linked_cat in LINK_REQUIRED_CATEGORIES:
        pattern = re.compile(rf"`?{re.escape(linked_cat)}`?[^\n]{{0,260}}\blink\b", re.IGNORECASE)
        if not pattern.search(unfenced_body):
            violations.append(
                f"{display}:1: missing-blocker-link-rule: "
                f"`{linked_cat}` must explicitly require a concrete link"
            )

    prose_clauses = _iter_normalized_prose_clauses(unfenced)
    found_prohibited_idle_unclassified = False
    found_prohibited_unverified_blocker = False

    for clause_lineno, clause in prose_clauses:
        low_clause = clause.lower()
        clause_idx: ClauseIndex | None = None
        if "nothing changed" in low_clause and "unclassified" in low_clause:
            clause_idx = _build_clause_index(clause)
            for nc_m in re.finditer(r"nothing\s+changed", clause, flags=re.IGNORECASE):
                if _is_claim_negated_at(clause_idx, nc_m.start(), allow_conditional_guards=False):
                    found_prohibited_idle_unclassified = True
                elif not _has_zero_unclassified_guard(clause):
                    violations.append(
                        f"{display}:{clause_lineno}: inverted-guard-polarity: "
                        "clause pairs 'nothing changed' with 'unclassified' without a governing "
                        "prohibition or zero-unclassified precondition"
                    )
        if "unverified blocker" in low_clause:
            if clause_idx is None:
                clause_idx = _build_clause_index(clause)
            for ub_m in re.finditer(r"unverified\s+blocker", clause, flags=re.IGNORECASE):
                if _is_claim_negated_at(clause_idx, ub_m.start(), allow_conditional_guards=False):
                    found_prohibited_unverified_blocker = True
                else:
                    violations.append(
                        f"{display}:{clause_lineno}: inverted-guard-polarity: "
                        "clause references 'unverified blocker' without a preceding prohibition"
                    )

    if not found_prohibited_idle_unclassified:
        violations.append(
            f"{display}:1: missing-unclassified-idle-guard: "
            "instructions must forbid claiming 'nothing changed' while open issues "
            "remain unclassified in the current run"
        )
    if not found_prohibited_unverified_blocker:
        violations.append(
            f"{display}:1: missing-unverified-blocker-guard: "
            "instructions must forbid pausing on an unverified blocker"
        )
    if not re.search(
        r"before[^\n]{0,160}(?:idle|waiting)[^\n]{0,160}summary|"
        r"issue-state classification table[^\n]{0,220}(?:idle|waiting)",
        unfenced_body,
        re.IGNORECASE | re.DOTALL,
    ):
        violations.append(
            f"{display}:1: missing-table-before-summary-rule: "
            "instructions must require the issue-state classification table before "
            "any idle or waiting summary"
        )

    required_live_tokens = (
        ("open-issue", "open-issue count refresh requirement"),
        ("open-pr", "open-PR count refresh requirement"),
        ("gh issue list --state open", "`gh issue list --state open` live command"),
        ("gh pr list --state open", "`gh pr list --state open` live command"),
        ("gh api --paginate", "`gh api --paginate` saturated-limit pagination fallback"),
        ("tmux list-sessions", "`tmux list-sessions` live session refresh command"),
        ("git rev-parse", "`git rev-parse` live SHA refresh command"),
        ("--expect-open-issues", "`--expect-open-issues` write-time validator flag"),
        ("--active-sessions", "`--active-sessions` write-time validator flag"),
        ("--open-issues", "`--open-issues` write-time validator flag"),
    )
    for token, label in required_live_tokens:
        if token not in lowered_body:
            violations.append(f"{display}:1: missing-live-refresh-rule: missing {label}")

    heading_slugs = {
        _heading_slug(m.group(2)) for _ln, line in unfenced if (m := HEADING_RE.match(line))
    }
    for lineno, line in unfenced:
        for _label, target in MD_LINK_RE.findall(line):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                anchor = target[1:]
                if anchor and anchor not in heading_slugs:
                    violations.append(
                        f"{display}:{lineno}: broken-link: missing heading anchor `{target}`"
                    )
                continue
            rel_part = target.split("#", 1)[0]
            if not rel_part:
                continue
            candidate = (resolved.parent / rel_part).resolve()
            if not candidate.exists():
                violations.append(
                    f"{display}:{lineno}: broken-link: relative target `{target}` does not exist"
                )

    return violations


def _validate_section(
    path: str,
    section_lines: list[tuple[int, str]],
    *,
    expect_head: str | None,
    expect_base: str | None,
    expect_open_issues: int | None,
    expect_open_prs: int | None,
    expect_active_sessions: int | None,
    active_sessions: set[str] | None = None,
    open_issues: set[int] | None,
    max_age_minutes: int,
    valid_heading_slugs: frozenset[str] | None = None,
) -> list[str]:
    violations: list[str] = []
    if not section_lines:
        return violations

    resolved_slugs = (
        valid_heading_slugs
        if valid_heading_slugs is not None
        else frozenset(
            _heading_slug(m.group(2))
            for _ln, line in section_lines
            if (m := HEADING_RE.match(line))
        )
    )
    anchor_line = section_lines[0][0]
    tables = _parse_markdown_tables(section_lines)
    class_tables = _extract_classification_tables(tables, resolved_slugs)
    table_line_numbers: set[int] = set()
    for tbl in tables:
        table_line_numbers.update(range(tbl.header_line, tbl.end_line + 1))

    all_rows: list[IssueRow] = []
    invalid_state_rows: list[IssueRow] = []
    seen_issues: dict[int, int] = {}
    classified_by_num: dict[int, IssueRow] = {}

    for ctable in class_tables:
        for row in ctable.rows:
            all_rows.append(row)
            if row.issue_number is None:
                violations.append(
                    f"{path}:{row.lineno}: invalid-issue-id: "
                    f"expected `#<number>` in Issue column, got `{row.raw_issue}`"
                )
            elif row.issue_number in seen_issues:
                prev_line = seen_issues[row.issue_number]
                violations.append(
                    f"{path}:{row.lineno}: duplicate-issue-row: "
                    f"issue #{row.issue_number} already classified at line {prev_line}"
                )
            else:
                seen_issues[row.issue_number] = row.lineno
                classified_by_num[row.issue_number] = row

            for broken_anchor in row.broken_anchors:
                violations.append(
                    f"{path}:{row.lineno}: broken-blocker-anchor: "
                    f"blocker/evidence link anchor `{broken_anchor}` does not match any "
                    f"heading in {path}"
                )
            for mismatched_link in row.mismatched_links:
                violations.append(
                    f"{path}:{row.lineno}: mismatched-blocker-link: "
                    f"blocker/evidence Markdown link label `{mismatched_link}` does not match "
                    "its target URL or issue/PR reference"
                )

            if row.state not in REQUIRED_CATEGORIES:
                invalid_state_rows.append(row)
                violations.append(
                    f"{path}:{row.lineno}: invalid-classification-category: "
                    f"state `{row.state or '<empty>'}` must be one of "
                    f"{', '.join(REQUIRED_CATEGORIES)}"
                )
            elif row.state in LINK_REQUIRED_CATEGORIES and not row.has_valid_blocker_link:
                violations.append(
                    f"{path}:{row.lineno}: missing-blocker-link: "
                    f"`{row.state}` row for {row.raw_issue or 'issue'} requires a concrete "
                    "non-bare-self URL, verified Markdown link, `#issuecomment-` anchor, or "
                    "distinct `#<other>` issue/PR reference"
                )

    open_issue_decls: list[tuple[int, int]] = []
    open_pr_decls: list[tuple[int, int]] = []
    active_session_decls: list[tuple[int, int]] = []
    session_cap: int = DEFAULT_SESSION_CAP
    pr_drain_noted = False
    listed_session_tokens: list[str] = []
    has_non_issue_session_token = False
    inline_open_issue_nums: set[int] = set()
    explicit_unclassified_count = 0
    observed_utc: tuple[int, datetime] | None = None
    written_utc: tuple[int, datetime] | None = None
    sha_decls: dict[str, list[tuple[int, str]]] = {
        "head_sha": [],
        "origin_main_sha": [],
        "base_sha": [],
    }

    for lineno, line in section_lines:
        if lineno in table_line_numbers:
            continue
        kv_match = KV_LINE_RE.match(line)
        if not kv_match:
            continue
        norm_key = _strip_md_formatting(kv_match.group(1)).lower()
        raw_val = kv_match.group(2).strip()
        if not raw_val:
            continue
        clean_val = _strip_md_formatting(raw_val)

        if norm_key in {"open issues", "open-issue count", "open issue count"}:
            num_match = re.match(r"^(\d+)\b", clean_val)
            if num_match:
                open_issue_decls.append((lineno, int(num_match.group(1))))
                for rq, issue_num in _iter_issue_refs(raw_val):
                    if not rq:
                        inline_open_issue_nums.add(issue_num)
            else:
                violations.append(
                    f"{path}:{lineno}: invalid-count: `Open issues` must start with an integer"
                )
        elif norm_key in {"open issue list", "open issues list"}:
            for rq, issue_num in _iter_issue_refs(raw_val):
                if not rq:
                    inline_open_issue_nums.add(issue_num)
        elif norm_key in {"open prs", "open-pr count", "open pr count"}:
            num_match = re.match(r"^(\d+)\b", clean_val)
            if num_match:
                open_pr_decls.append((lineno, int(num_match.group(1))))
                if re.search(r"\bdrain(?:ing)?\b", raw_val, re.IGNORECASE):
                    pr_drain_noted = True
            else:
                violations.append(
                    f"{path}:{lineno}: invalid-count: `Open PRs` must start with an integer"
                )
        elif norm_key in {
            "active sessions",
            "active tmux sessions",
            "active session status",
        }:
            cap_match = re.match(
                r"^(?:none\s*\(\s*)?(\d+)(?:\s*/\s*(\d+))?", clean_val, re.IGNORECASE
            )
            if cap_match:
                active_session_decls.append((lineno, int(cap_match.group(1))))
                if cap_match.group(2):
                    session_cap = int(cap_match.group(2))
                for tok in BACKTICK_TOKEN_RE.findall(raw_val):
                    stripped_tok = tok.strip()
                    if not stripped_tok or stripped_tok.lower() == "none":
                        continue
                    listed_session_tokens.append(stripped_tok)
                    if not RPI_SESSION_RE.match(stripped_tok):
                        has_non_issue_session_token = True
            else:
                violations.append(
                    f"{path}:{lineno}: invalid-count: "
                    "`Active sessions` must start with an integer or `M/N`"
                )
        elif norm_key in {
            "unclassified issues",
            "unclassified open issues",
            "unassessed closure",
            "unassessed items",
        }:
            num_match = re.match(r"^(\d+)\b", clean_val)
            if num_match and int(num_match.group(1)) > 0:
                explicit_unclassified_count += int(num_match.group(1))
        elif norm_key in {"observed utc", "observed_at", "observed at", "snapshot utc"}:
            parsed_ts = _parse_iso_utc(raw_val)
            if parsed_ts is None:
                violations.append(
                    f"{path}:{lineno}: invalid-timestamp: invalid ISO-8601 `Observed UTC` value"
                )
            else:
                observed_utc = (lineno, parsed_ts)
        elif norm_key in {"written utc", "written_at", "written at", "handoff utc"}:
            parsed_ts = _parse_iso_utc(raw_val)
            if parsed_ts is None:
                violations.append(
                    f"{path}:{lineno}: invalid-timestamp: invalid ISO-8601 `Written UTC` value"
                )
            else:
                written_utc = (lineno, parsed_ts)
        elif norm_key in {"head sha", "head", "current head", "source sha"}:
            sha_tok = clean_val.split()[0].strip("`") if clean_val else ""
            sha_decls["head_sha"].append((lineno, sha_tok))
        elif norm_key in {"origin/main sha", "origin/main", "main sha"}:
            sha_tok = clean_val.split()[0].strip("`") if clean_val else ""
            sha_decls["origin_main_sha"].append((lineno, sha_tok))
        elif norm_key in {
            "target/base sha",
            "target sha",
            "base sha",
            "parent-topic sha",
            "target base sha",
        }:
            sha_tok = clean_val.split()[0].strip("`") if clean_val else ""
            sha_decls["base_sha"].append((lineno, sha_tok))

    section_text = "\n".join(line for _ln, line in section_lines)
    section_lower = section_text.lower()

    if not open_issue_decls:
        violations.append(
            f"{path}:{anchor_line}: stale-or-missing-counts: "
            "missing live-refreshed `Open issues` count"
        )
    if not open_pr_decls:
        violations.append(
            f"{path}:{anchor_line}: stale-or-missing-counts: "
            "missing live-refreshed `Open PRs` count"
        )
    if not active_session_decls:
        violations.append(
            f"{path}:{anchor_line}: stale-or-missing-counts: "
            "missing live-refreshed `Active sessions` status/count"
        )

    has_issue_provenance = "gh issue list" in section_lower or (
        "gh api" in section_lower and "--paginate" in section_lower and "/issues" in section_lower
    )
    has_pr_provenance = "gh pr list" in section_lower or (
        "gh api" in section_lower and "--paginate" in section_lower and "/pulls" in section_lower
    )

    if not has_issue_provenance:
        violations.append(
            f"{path}:{anchor_line}: missing-live-provenance: "
            "handoff/checkpoint must record live `gh issue list` (or `gh api --paginate .../issues`) "
            "command provenance"
        )
    if not has_pr_provenance:
        violations.append(
            f"{path}:{anchor_line}: missing-live-provenance: "
            "handoff/checkpoint must record live `gh pr list` (or `gh api --paginate .../pulls`) "
            "command provenance"
        )
    if "tmux list-sessions" not in section_lower and "tmux ls" not in section_lower:
        violations.append(
            f"{path}:{anchor_line}: missing-live-provenance: "
            "handoff/checkpoint must record live `tmux list-sessions` (or `tmux ls`) provenance"
        )

    for decl_name, decls in (
        ("Open issues", open_issue_decls),
        ("Open PRs", open_pr_decls),
        ("Active sessions", active_session_decls),
    ):
        distinct_vals = {val for _ln, val in decls}
        if len(distinct_vals) > 1:
            conflict_line = decls[-1][0]
            violations.append(
                f"{path}:{conflict_line}: stale-count-conflict: "
                f"conflicting `{decl_name}` counts in same handoff section: "
                f"{sorted(distinct_vals)}"
            )

    any_sha_recorded = any(bool(entries) for entries in sha_decls.values())
    if not any_sha_recorded:
        violations.append(
            f"{path}:{anchor_line}: missing-pinned-sha: "
            "handoff/checkpoint must record at least one live-resolved `HEAD SHA` or "
            "`Origin/main SHA`"
        )
    elif "git rev-parse" not in section_lower:
        violations.append(
            f"{path}:{anchor_line}: missing-live-provenance: "
            "pinned SHA block must record live `git rev-parse` provenance"
        )

    for sha_key, entries in sha_decls.items():
        valid_entries: list[tuple[int, str]] = []
        for lineno, sha_tok in entries:
            if not HEX_SHA_RE.match(sha_tok) or set(sha_tok) == {"0"}:
                violations.append(
                    f"{path}:{lineno}: invalid-or-placeholder-sha: "
                    f"`{sha_key}` value `{sha_tok or '<empty>'}` is not a valid resolved Git SHA"
                )
            else:
                valid_entries.append((lineno, sha_tok))
        for idx in range(1, len(valid_entries)):
            prev_sha = valid_entries[0][1]
            curr_line, curr_sha = valid_entries[idx]
            if not _shas_compatible(prev_sha, curr_sha):
                violations.append(
                    f"{path}:{curr_line}: stale-sha-conflict: "
                    f"conflicting `{sha_key}` values `{prev_sha}` vs `{curr_sha}` in same section"
                )

    if observed_utc is not None and written_utc is not None:
        obs_line, obs_dt = observed_utc
        wrt_line, wrt_dt = written_utc
        delta = wrt_dt - obs_dt
        if delta > timedelta(minutes=max_age_minutes):
            violations.append(
                f"{path}:{obs_line}: stale-snapshot-timestamp: "
                f"`Observed UTC` precedes `Written UTC` (line {wrt_line}) by "
                f"{int(delta.total_seconds() // 60)}m (> {max_age_minutes}m)"
            )
        elif delta < timedelta(0):
            violations.append(
                f"{path}:{obs_line}: invalid-snapshot-timestamp: "
                f"`Observed UTC` is later than `Written UTC` (line {wrt_line})"
            )

    declared_open_issues = open_issue_decls[-1][1] if open_issue_decls else None
    declared_open_prs = open_pr_decls[-1][1] if open_pr_decls else None
    declared_active_sessions = active_session_decls[-1][1] if active_session_decls else None

    if expect_open_issues is not None and declared_open_issues != expect_open_issues:
        line_ref = open_issue_decls[-1][0] if open_issue_decls else anchor_line
        violations.append(
            f"{path}:{line_ref}: stale-open-issues-count: "
            f"recorded `Open issues: {declared_open_issues}` != live expected {expect_open_issues}"
        )
    if expect_open_prs is not None and declared_open_prs != expect_open_prs:
        line_ref = open_pr_decls[-1][0] if open_pr_decls else anchor_line
        violations.append(
            f"{path}:{line_ref}: stale-open-prs-count: "
            f"recorded `Open PRs: {declared_open_prs}` != live expected {expect_open_prs}"
        )
    if expect_active_sessions is not None and declared_active_sessions != expect_active_sessions:
        line_ref = active_session_decls[-1][0] if active_session_decls else anchor_line
        violations.append(
            f"{path}:{line_ref}: stale-active-sessions-count: "
            f"recorded `Active sessions: {declared_active_sessions}` != "
            f"live expected {expect_active_sessions}"
        )

    if expect_head is not None:
        if not sha_decls["head_sha"]:
            violations.append(
                f"{path}:{anchor_line}: missing-head-sha: "
                f"expected `HEAD SHA` matching `{expect_head}`"
            )
        else:
            head_line, head_val = sha_decls["head_sha"][-1]
            if HEX_SHA_RE.match(head_val) and not _shas_compatible(head_val, expect_head):
                violations.append(
                    f"{path}:{head_line}: stale-head-sha: "
                    f"recorded `HEAD SHA` `{head_val}` does not match expected `{expect_head}`"
                )

    if expect_base is not None:
        base_candidates = sha_decls["base_sha"] or sha_decls["origin_main_sha"]
        if not base_candidates:
            violations.append(
                f"{path}:{anchor_line}: missing-base-sha: "
                f"expected `Target/base SHA` or `Origin/main SHA` matching `{expect_base}`"
            )
        else:
            base_line, base_val = base_candidates[-1]
            if HEX_SHA_RE.match(base_val) and not _shas_compatible(base_val, expect_base):
                violations.append(
                    f"{path}:{base_line}: stale-base-sha: "
                    f"recorded base SHA `{base_val}` does not match expected `{expect_base}`"
                )

    non_merged_rows = [r for r in all_rows if r.state in NON_MERGED_CATEGORIES]
    active_session_rows = [r for r in all_rows if r.state == "active session"]
    ready_rows = [r for r in all_rows if r.state == "ready to start"]

    unclassified_reasons: list[str] = []
    if invalid_state_rows:
        unclassified_reasons.append(
            f"{len(invalid_state_rows)} row(s) carry non-canonical or unknown state"
        )
    if explicit_unclassified_count > 0:
        unclassified_reasons.append(
            f"{explicit_unclassified_count} unclassified/unassessed item(s) declared"
        )

    if class_tables and declared_open_issues is not None:
        open_line = open_issue_decls[-1][0]
        if declared_open_issues > len(non_merged_rows):
            missing_n = declared_open_issues - len(non_merged_rows)
            unclassified_reasons.append(
                f"`Open issues: {declared_open_issues}` exceeds classified non-merged rows "
                f"({len(non_merged_rows)}) by {missing_n}"
            )
            violations.append(
                f"{path}:{open_line}: unclassified-open-issues: "
                f"`Open issues: {declared_open_issues}` has {missing_n} unclassified open issue(s) "
                f"missing from the classification table ({len(non_merged_rows)} non-merged row(s))"
            )
        elif len(non_merged_rows) > declared_open_issues:
            violations.append(
                f"{path}:{open_line}: stale-open-issues-count: "
                f"`Open issues: {declared_open_issues}` is smaller than {len(non_merged_rows)} "
                "non-merged open issue row(s) in the classification table"
            )

    expected_open_set: set[int] = set(inline_open_issue_nums)
    if open_issues is not None:
        expected_open_set.update(open_issues)

    for open_num in sorted(expected_open_set):
        matched_row = classified_by_num.get(open_num)
        if matched_row is None:
            unclassified_reasons.append(f"open issue #{open_num} is missing from the table")
            violations.append(
                f"{path}:{anchor_line}: unclassified-open-issue: "
                f"open issue #{open_num} is not classified in the issue-state table"
            )
        elif matched_row.state == "merged":
            unclassified_reasons.append(f"still-open issue #{open_num} is marked `merged`")
            violations.append(
                f"{path}:{matched_row.lineno}: open-issue-marked-merged: "
                f"still-open issue #{open_num} cannot be classified as `merged` before closing on "
                "`main` (use `dependency-blocked` with parent/CI PR link if awaiting integration)"
            )

    seen_session_mismatch: set[tuple[str, int]] = set()

    def _verify_sessions_against_table(
        session_tokens: set[str],
        *,
        fallback_line: int,
        require_active_rows_covered: bool,
    ) -> None:
        matched_session_issues: set[int] = set()
        custom_non_rpi_tokens: list[str] = []
        for sess_tok in sorted(session_tokens):
            sess_m = RPI_SESSION_RE.match(sess_tok)
            if not sess_m:
                custom_non_rpi_tokens.append(sess_tok)
                continue
            sess_issue = int(sess_m.group(1))
            matched_session_issues.add(sess_issue)
            sess_row = classified_by_num.get(sess_issue)
            if sess_row is None:
                if class_tables and ("missing", sess_issue) not in seen_session_mismatch:
                    seen_session_mismatch.add(("missing", sess_issue))
                    violations.append(
                        f"{path}:{fallback_line}: stale-session-classification: "
                        f"live tmux session `{sess_tok}` references #{sess_issue}, which is not "
                        "classified in the issue-state table"
                    )
            elif (
                sess_row.state != "active session"
                and ("state", sess_issue) not in seen_session_mismatch
            ):
                seen_session_mismatch.add(("state", sess_issue))
                violations.append(
                    f"{path}:{sess_row.lineno}: stale-session-classification: "
                    f"live tmux session `{sess_tok}` conflicts with #{sess_issue} state "
                    f"`{sess_row.state}`"
                )

        if not require_active_rows_covered or not class_tables:
            return
        custom_session_issue_nums: set[int] = {
            int(m.group(1))
            for custom_tok in custom_non_rpi_tokens
            for m in STANDALONE_ISSUE_NUM_RE.finditer(custom_tok)
        }
        for act_row in active_session_rows:
            if act_row.issue_number is None:
                continue
            row_num = act_row.issue_number
            if row_num in matched_session_issues or row_num in custom_session_issue_nums:
                continue
            if ("unbacked_active", row_num) not in seen_session_mismatch:
                seen_session_mismatch.add(("unbacked_active", row_num))
                violations.append(
                    f"{path}:{act_row.lineno}: stale-session-classification: "
                    f"issue #{row_num} is classified as `active session`, but no active tmux "
                    f"session matches #{row_num} ({sorted(session_tokens)})"
                )

    if class_tables and declared_active_sessions is not None:
        sess_line = active_session_decls[-1][0]
        if declared_active_sessions == 0 and len(active_session_rows) > 0:
            violations.append(
                f"{path}:{sess_line}: stale-active-sessions-count: "
                f"`Active sessions: 0` contradicts {len(active_session_rows)} `active session` "
                "row(s) in the classification table"
            )
        elif len(active_session_rows) > declared_active_sessions:
            violations.append(
                f"{path}:{sess_line}: stale-active-sessions-count: "
                f"{len(active_session_rows)} `active session` issue row(s) exceed declared "
                f"`Active sessions: {declared_active_sessions}`"
            )
        elif (
            declared_active_sessions > 0
            and len(active_session_rows) == 0
            and not has_non_issue_session_token
        ):
            violations.append(
                f"{path}:{sess_line}: stale-active-sessions-count: "
                f"`Active sessions: {declared_active_sessions}` declared with zero `active session`"
                " issue rows"
            )

        if listed_session_tokens:
            if len(listed_session_tokens) != declared_active_sessions:
                violations.append(
                    f"{path}:{sess_line}: stale-active-sessions-count: "
                    f"listed session count ({len(listed_session_tokens)}) != declared "
                    f"`Active sessions: {declared_active_sessions}`"
                )
            _verify_sessions_against_table(
                set(listed_session_tokens),
                fallback_line=sess_line,
                require_active_rows_covered=True,
            )

    if active_sessions is not None:
        live_sess_line = active_session_decls[-1][0] if active_session_decls else anchor_line
        if (
            expect_active_sessions is None
            and declared_active_sessions is not None
            and declared_active_sessions != len(active_sessions)
        ):
            violations.append(
                f"{path}:{live_sess_line}: stale-active-sessions-count: "
                f"recorded `Active sessions: {declared_active_sessions}` != "
                f"live tmux session count {len(active_sessions)}"
            )
        recorded_session_set = set(listed_session_tokens)
        if recorded_session_set != active_sessions:
            violations.append(
                f"{path}:{live_sess_line}: stale-active-session-identity: "
                f"recorded Active sessions {sorted(recorded_session_set)} != "
                f"live tmux sessions {sorted(active_sessions)}"
            )
        _verify_sessions_against_table(
            active_sessions,
            fallback_line=live_sess_line,
            require_active_rows_covered=True,
        )

    for tbl in tables:
        if (
            "pr" in tbl.headers
            and ("checks" in tbl.headers or "mergeability" in tbl.headers)
            and declared_open_prs is not None
            and len(tbl.rows) != declared_open_prs
        ):
            pr_line = open_pr_decls[-1][0]
            violations.append(
                f"{path}:{pr_line}: stale-open-prs-count: "
                f"`Open PRs: {declared_open_prs}` != {len(tbl.rows)} row(s) in open-PR table"
            )

    verified_blocker_evidence_refs: set[BlockerRef] = set()
    for row in all_rows:
        if row.state == "active session" or (
            row.state in LINK_REQUIRED_CATEGORIES and row.has_valid_blocker_link
        ):
            verified_blocker_evidence_refs.update(
                _extract_verified_evidence_refs(
                    row.issue_number,
                    row.blocker_cells,
                    row.broken_anchors,
                    resolved_slugs,
                )
            )

    ready_issue_nums = {r.issue_number for r in ready_rows if r.issue_number is not None}
    first_table_end = class_tables[0].end_line if class_tables else None
    last_table_end = max((tbl.end_line for tbl in class_tables), default=None)
    at_session_capacity = (
        declared_active_sessions is not None and declared_active_sessions >= session_cap
    )
    pr_drain_active = declared_open_prs is not None and (
        declared_open_prs > 20 or (declared_open_prs > 15 and pr_drain_noted)
    )
    at_capacity_or_draining = at_session_capacity or pr_drain_active
    session_slots = (
        max(0, session_cap - declared_active_sessions)
        if declared_active_sessions is not None
        else len(ready_issue_nums)
    )
    required_ready_launches = min(len(ready_issue_nums), session_slots)

    indexed_prose_blocks: list[tuple[int, str, ClauseIndex]] = []
    section_launched_ready: set[int] = set()
    for lineno, block_text in _iter_section_prose_blocks(section_lines, table_line_numbers):
        block_idx = _build_clause_index(block_text)
        indexed_prose_blocks.append((lineno, block_text, block_idx))
        if ready_issue_nums:
            section_launched_ready.update(
                _launched_ready_issues_in_current_tick(block_text, block_idx, ready_issue_nums)
            )

    def _format_blocker_ref(ref_repo: str, ref_val: int | str) -> str:
        if ref_repo in {"url", "anchor"}:
            return str(ref_val)
        if ref_repo:
            return f"{ref_repo}#{ref_val}"
        return f"#{ref_val}"

    for lineno, block_text, c_idx in indexed_prose_blocks:
        if any(
            not _is_claim_negated_at(c_idx, m.start()) for m in STALE_CARRY_RE.finditer(block_text)
        ):
            violations.append(
                f"{path}:{lineno}: stale-handoff-reference: "
                "unrefreshed or carried-over handoff text detected"
            )

        is_idle = any(
            not _is_claim_negated_at(c_idx, m.start()) for m in IDLE_CLAIM_RE.finditer(block_text)
        )
        is_waiting_or_pause = any(
            not _is_claim_negated_at(c_idx, m.start())
            for m in WAITING_OR_PAUSE_RE.finditer(block_text)
        )
        is_global_wait_or_pause = _has_global_wait_or_pause(block_text, c_idx)
        has_sufficient_ready_launches = len(section_launched_ready) >= required_ready_launches
        has_unverified_phrase = any(
            not _is_claim_negated_at(c_idx, m.start())
            for m in UNVERIFIED_BLOCKER_RE.finditer(block_text)
        )
        cited_blocker_refs, has_uncited_non_capacity_wait = _extract_wait_and_blocker_spans(
            block_text,
            c_idx,
            at_session_capacity=at_session_capacity,
            pr_drain_active=pr_drain_active,
        )
        has_blocker_or_wait_claim = (
            is_waiting_or_pause
            or bool(cited_blocker_refs)
            or has_uncited_non_capacity_wait
            or has_unverified_phrase
        )

        if has_unverified_phrase or has_uncited_non_capacity_wait:
            violations.append(
                f"{path}:{lineno}: unverified-blocker-pause: "
                "cannot pause or report waiting without citing a verified, linked blocker from "
                "the issue-state classification table"
            )

        if not (is_idle or has_blocker_or_wait_claim):
            continue

        if first_table_end is None or last_table_end is None:
            violations.append(
                f"{path}:{lineno}: missing-classification-table: "
                "explicit five-category issue-state classification table is required before any "
                "idle, waiting, 'nothing changed', or pause summary"
            )
            for ref_repo, ref_val in cited_blocker_refs:
                ref_label = _format_blocker_ref(ref_repo, ref_val)
                violations.append(
                    f"{path}:{lineno}: unverified-blocker-reference: "
                    f"summary cites {ref_label} as a wait/pause blocker, but {ref_label} is not "
                    "classified in an issue-state table"
                )
            continue

        if lineno <= last_table_end:
            violations.append(
                f"{path}:{lineno}: summary-before-classification-table: "
                "idle, waiting, 'nothing changed', or pause summary appears at line "
                f"{lineno} before classification table ending at line {last_table_end}"
            )

        if (is_idle or has_blocker_or_wait_claim) and unclassified_reasons:
            violations.append(
                f"{path}:{lineno}: unsupported-idle-unclassified: "
                "idle/waiting summary rejected while open issues remain unclassified "
                f"({'; '.join(unclassified_reasons)})"
            )

        if is_idle and ready_rows:
            ready_ids = ", ".join(r.raw_issue for r in ready_rows)
            violations.append(
                f"{path}:{lineno}: unsupported-idle-ready-work: "
                f"cannot claim idle or 'nothing changed' while actionable `ready to start` "
                f"issue(s) exist ({ready_ids})"
            )
        elif (
            has_blocker_or_wait_claim
            and ready_rows
            and not at_capacity_or_draining
            and (is_global_wait_or_pause or not has_sufficient_ready_launches)
        ):
            unstarted_ids = ", ".join(
                r.raw_issue
                for r in ready_rows
                if r.issue_number is None or r.issue_number not in section_launched_ready
            )
            target_ids = unstarted_ids or ", ".join(r.raw_issue for r in ready_rows)
            violations.append(
                f"{path}:{lineno}: unsupported-waiting-ready-work: "
                f"waiting/pause summary rejected while `ready to start` issue(s) ({target_ids}) "
                "have open session/PR admission capacity"
            )

        for ref_repo, ref_val in cited_blocker_refs:
            if ref_repo or not isinstance(ref_val, int):
                if (ref_repo, ref_val) not in verified_blocker_evidence_refs:
                    ref_label = _format_blocker_ref(ref_repo, ref_val)
                    violations.append(
                        f"{path}:{lineno}: unverified-blocker-reference: "
                        f"summary cites {ref_label} as a wait/pause blocker, but {ref_label} is "
                        "not recorded as verified blocker evidence in the issue-state table"
                    )
                continue

            ref_num = ref_val
            ref_row = classified_by_num.get(ref_num)
            if ref_row is None:
                if ("", ref_num) not in verified_blocker_evidence_refs:
                    violations.append(
                        f"{path}:{lineno}: unverified-blocker-reference: "
                        f"summary cites #{ref_num} as a wait/pause blocker, but #{ref_num} is not "
                        "classified or recorded as verified blocker evidence in the issue-state "
                        "table"
                    )
            elif ref_row.state not in {
                "active session",
                "human-blocked",
                "dependency-blocked",
            }:
                violations.append(
                    f"{path}:{lineno}: unverified-blocker-reference: "
                    f"summary cites #{ref_num} as a wait/pause blocker, but table classifies "
                    f"#{ref_num} as `{ref_row.state}`"
                )
            elif ref_row.state in LINK_REQUIRED_CATEGORIES and not ref_row.has_valid_blocker_link:
                violations.append(
                    f"{path}:{lineno}: unverified-blocker-reference: "
                    f"summary pauses/waits on #{ref_num} without a verified blocker link"
                )

    return violations


def check_handoff_text(
    path: str,
    text: str,
    *,
    expect_head: str | None = None,
    expect_base: str | None = None,
    expect_open_issues: int | None = None,
    expect_open_prs: int | None = None,
    expect_active_sessions: int | None = None,
    active_sessions: set[str] | None = None,
    open_issues: set[int] | None = None,
    max_age_minutes: int = 30,
) -> list[str]:
    """Validate coordinator handoff, check-status, or checkpoint Markdown content."""
    if not text.strip():
        return [f"{path}:1: empty-handoff: coordinator handoff artifact is empty"]
    unfenced = _iter_unfenced_lines(text)
    if not unfenced:
        return [f"{path}:1: empty-handoff: coordinator handoff has no unfenced content"]

    doc_heading_slugs = frozenset(
        _heading_slug(m.group(2)) for _ln, line in unfenced if (m := HEADING_RE.match(line))
    )
    sections = _split_handoff_sections(unfenced)
    violations: list[str] = []
    for idx, sec in enumerate(sections):
        is_latest = idx == len(sections) - 1
        violations.extend(
            _validate_section(
                path,
                sec,
                expect_head=expect_head if is_latest else None,
                expect_base=expect_base if is_latest else None,
                expect_open_issues=expect_open_issues if is_latest else None,
                expect_open_prs=expect_open_prs if is_latest else None,
                expect_active_sessions=expect_active_sessions if is_latest else None,
                active_sessions=active_sessions if is_latest else None,
                open_issues=open_issues if is_latest else None,
                max_age_minutes=max_age_minutes,
                valid_heading_slugs=doc_heading_slugs,
            )
        )
    return violations


def check_handoff_file(
    handoff_path: Path,
    *,
    root: Path | None = None,
    expect_head: str | None = None,
    expect_base: str | None = None,
    expect_open_issues: int | None = None,
    expect_open_prs: int | None = None,
    expect_active_sessions: int | None = None,
    active_sessions: set[str] | None = None,
    open_issues: set[int] | None = None,
    max_age_minutes: int = 30,
) -> list[str]:
    repo_root = (root or ROOT).resolve()
    resolved = handoff_path.resolve()
    try:
        display = resolved.relative_to(repo_root).as_posix()
    except ValueError:
        display = handoff_path.as_posix()

    if not resolved.is_file():
        return [f"{display}:1: missing-handoff-file: file does not exist"]
    text = resolved.read_text(encoding="utf-8")
    return check_handoff_text(
        display,
        text,
        expect_head=expect_head,
        expect_base=expect_base,
        expect_open_issues=expect_open_issues,
        expect_open_prs=expect_open_prs,
        expect_active_sessions=expect_active_sessions,
        active_sessions=active_sessions,
        open_issues=open_issues,
        max_age_minutes=max_age_minutes,
    )


def _resolve_git_head(repo_root: Path) -> str | None:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def _parse_open_issues_arg(raw: str | None) -> set[int] | None:
    if raw is None:
        return None
    if not raw.strip():
        return set()
    parsed: set[int] = set()
    for part in raw.split(","):
        tok = part.strip().lstrip("#")
        if not tok.isdigit():
            raise ValueError(f"invalid issue number `{part}` in --open-issues")
        parsed.add(int(tok))
    return parsed


def _parse_active_sessions_arg(raw: str | None) -> set[str] | None:
    if raw is None:
        return None
    if not raw.strip():
        return set()
    parsed: set[str] = set()
    for part in raw.split(","):
        tok = part.strip().strip("`")
        if not tok or tok.lower() == "none":
            continue
        if any(ch.isspace() for ch in tok):
            raise ValueError(f"invalid session name `{part}` in --active-sessions")
        parsed.add(tok)
    return parsed


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate coordinator agent instructions and coordinator handoff/status Markdown "
            "for five-category issue classification, supported idle/waiting summaries, and "
            "live-refreshed count/SHA blocks."
        )
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root directory (default: parent of tools/).",
    )
    parser.add_argument(
        "--agent",
        type=Path,
        default=None,
        help=f"Explicit coordinator agent path (default: <root>/{AGENT_RELATIVE_PATH.as_posix()}).",
    )
    parser.add_argument(
        "--no-agent",
        action="store_true",
        help="Skip validating the coordinator agent instructions file.",
    )
    parser.add_argument(
        "--handoff",
        type=Path,
        action="append",
        default=[],
        help="Coordinator handoff, check-status, or checkpoint Markdown file to validate.",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Validate coordinator handoff/status Markdown read from standard input.",
    )
    parser.add_argument(
        "--expect-head",
        default=None,
        help="Expected live HEAD SHA prefix to verify against handoff `HEAD SHA`.",
    )
    parser.add_argument(
        "--expect-base",
        default=None,
        help="Expected live base/origin-main SHA prefix to verify against handoff base SHA.",
    )
    parser.add_argument(
        "--check-git-head",
        action="store_true",
        help="Resolve live `git rev-parse HEAD` in --root and compare against handoff `HEAD SHA`.",
    )
    parser.add_argument(
        "--expect-open-issues",
        type=int,
        default=None,
        help="Expected live open-issue count to verify against handoff `Open issues`.",
    )
    parser.add_argument(
        "--expect-open-prs",
        type=int,
        default=None,
        help="Expected live open-PR count to verify against handoff `Open PRs`.",
    )
    parser.add_argument(
        "--expect-active-sessions",
        type=int,
        default=None,
        help="Expected live active tmux session count to verify against `Active sessions`.",
    )
    parser.add_argument(
        "--active-sessions",
        default=None,
        help=(
            "Comma-separated live active tmux session names (e.g. `rpi-1204,rpi-1310` or `none`) "
            "to verify against `Active sessions` tokens and table states."
        ),
    )
    parser.add_argument(
        "--open-issues",
        default=None,
        help="Comma-separated live open issue numbers (e.g. `1204,1288,1302`) to verify.",
    )
    parser.add_argument(
        "--max-age-minutes",
        type=int,
        default=30,
        help=(
            "Maximum allowed age in minutes between `Observed UTC` and `Written UTC` (default 30)."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    repo_root = args.root.resolve()

    try:
        open_issues = _parse_open_issues_arg(args.open_issues)
        active_sessions = _parse_active_sessions_arg(args.active_sessions)
    except ValueError as exc:
        print(f"argument-error: {exc}", file=sys.stderr)
        return 2

    expect_head: str | None = args.expect_head
    if expect_head is None and args.check_git_head:
        expect_head = _resolve_git_head(repo_root)
        if expect_head is None:
            print(f"argument-error: could not resolve git HEAD in {repo_root}", file=sys.stderr)
            return 2

    if args.no_agent and not args.handoff and not args.stdin:
        print(
            "argument-error: nothing to validate (--no-agent without --handoff/--stdin)",
            file=sys.stderr,
        )
        return 2

    violations: list[str] = []
    checked_targets = 0

    if not args.no_agent:
        agent_path = args.agent if args.agent is not None else repo_root / AGENT_RELATIVE_PATH
        violations.extend(check_agent_instructions(agent_path, root=repo_root))
        checked_targets += 1

    for handoff_path in args.handoff:
        violations.extend(
            check_handoff_file(
                handoff_path,
                root=repo_root,
                expect_head=expect_head,
                expect_base=args.expect_base,
                expect_open_issues=args.expect_open_issues,
                expect_open_prs=args.expect_open_prs,
                expect_active_sessions=args.expect_active_sessions,
                active_sessions=active_sessions,
                open_issues=open_issues,
                max_age_minutes=args.max_age_minutes,
            )
        )
        checked_targets += 1

    if args.stdin:
        violations.extend(
            check_handoff_text(
                "<stdin>",
                sys.stdin.read(),
                expect_head=expect_head,
                expect_base=args.expect_base,
                expect_open_issues=args.expect_open_issues,
                expect_open_prs=args.expect_open_prs,
                expect_active_sessions=args.expect_active_sessions,
                active_sessions=active_sessions,
                open_issues=open_issues,
                max_age_minutes=args.max_age_minutes,
            )
        )
        checked_targets += 1

    if violations:
        for violation in violations:
            print(violation)
        print(
            f"\nCoordinator handoff guard check failed with {len(violations)} violation(s) "
            f"across {checked_targets} target(s)."
        )
        return 1

    print(f"Coordinator handoff guard check passed ({checked_targets} target(s), 0 violations).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
