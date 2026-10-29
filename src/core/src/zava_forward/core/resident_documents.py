"""Resident-facing document facts only; receipt and scan results never approve evidence."""

from dataclasses import dataclass
from typing import Any


class DocumentFactsInvalid(ValueError):
    """Malformed own-case document data must not become an apparently empty checklist."""


@dataclass(frozen=True)
class DocumentRequest:
    id: str
    kind: str
    how_to_provide: str


@dataclass(frozen=True)
class DocumentIssue:
    severity: str
    message: str


@dataclass(frozen=True)
class PresentedDocument:
    id: str
    kind: str
    generated: bool
    scan_status: str | None
    issues: tuple[DocumentIssue, ...] | None


@dataclass(frozen=True)
class DocumentFacts:
    requests: tuple[DocumentRequest, ...] | None = None
    documents: tuple[PresentedDocument, ...] | None = None


def _text(value: Any, limit: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise DocumentFactsInvalid("document_text")
    return value


def _rows(value: Any, limit: int) -> list[dict[str, Any]] | None:
    if value is None:
        return None
    if (
        not isinstance(value, list)
        or len(value) > limit
        or any(not isinstance(item, dict) for item in value)
    ):
        raise DocumentFactsInvalid("document_list")
    return value


def parse_document_facts(raw: Any) -> DocumentFacts:
    """Parse the view's positive allowlist, preserving unknown versus known-empty."""
    if not isinstance(raw, dict) or set(raw) != {"requests", "documents"}:
        raise DocumentFactsInvalid("document_shape")
    requests = _rows(raw["requests"], 20)
    documents = _rows(raw["documents"], 40)
    parsed_requests = []
    for row in requests or []:
        if set(row) != {"id", "kind", "how_to_provide"}:
            raise DocumentFactsInvalid("document_request")
        parsed_requests.append(
            DocumentRequest(
                _text(row["id"], 64), _text(row["kind"], 80), _text(row["how_to_provide"], 500)
            )
        )
    parsed_documents = []
    for row in documents or []:
        if (
            set(row) != {"id", "kind", "generated", "scan_status", "issues", "source_valid"}
            or type(row["source_valid"]) is not int
            or row["source_valid"] != 1
            or type(row["generated"]) is not bool
        ):
            raise DocumentFactsInvalid("document_record")
        issues = _rows(row["issues"], 10)
        parsed_issues = []
        for issue in issues or []:
            if set(issue) != {"severity", "message"} or issue["severity"] not in (
                "warning",
                "error",
            ):
                raise DocumentFactsInvalid("document_issue")
            parsed_issues.append(DocumentIssue(issue["severity"], _text(issue["message"], 500)))
        parsed_documents.append(
            PresentedDocument(
                _text(row["id"], 64),
                _text(row["kind"], 80),
                row["generated"],
                None if row["scan_status"] is None else _text(row["scan_status"], 80),
                None if issues is None else tuple(parsed_issues),
            )
        )
    for group in (parsed_requests, parsed_documents):
        if len({item.id for item in group}) != len(group):
            raise DocumentFactsInvalid("document_duplicate")
    return DocumentFacts(
        None if requests is None else tuple(parsed_requests),
        None if documents is None else tuple(parsed_documents),
    )


SCAN_TEXT = {
    "pending": "Warning: the file check has not finished. Staff need to check it.",
    "infected": "Error: the recorded file check flagged possible malware. Ask staff for help.",
    "mismatch": (
        "Error: the recorded file check says the contents do not match the file type. "
        "Ask staff which format to provide."
    ),
    "clean": "The recorded file check says clean. This is not approval of the document.",
}


def document_answer(facts: DocumentFacts) -> tuple[str, tuple[str, ...]]:
    parts = []
    sources = []
    if facts.requests is None:
        parts.append(
            "This view does not show which documents have been requested for your case. "
            "It cannot tell you what to send."
        )
        sources.append("Your case: document requests not recorded")
    elif not facts.requests:
        parts.append("Your case has no document requests recorded in this view.")
        sources.append("Your case: recorded document request list")
    for request in facts.requests or ():
        if facts.documents is None:
            state = "Whether a document has been provided is unknown."
        elif any(d.kind == request.kind and not d.generated for d in facts.documents):
            state = "A presented document is recorded. Staff still need to check it."
        else:
            state = "Missing from the presented documents in this view."
        parts.append(
            f"Request {request.id}, {request.kind}: {state} "
            f'How to provide it (recorded instruction): "{request.how_to_provide}"'
        )
        sources.append(f"Your case: document request {request.id} ({request.kind})")
    if facts.documents is None:
        parts.append("Presented documents and their warnings or errors are not available here.")
        sources.append("Your case: presented document data not recorded")
    elif not facts.documents:
        parts.append("No presented documents are recorded in this view.")
        sources.append("Your case: recorded presented document list")
    for document in facts.documents or ():
        prefix = f"Document {document.id}, {document.kind}: "
        if document.generated:
            parts.append(prefix + "a generated placeholder, not a presented document.")
        else:
            parts.append(prefix + "recorded as presented, not accepted or approved.")
        parts.append(
            SCAN_TEXT.get(
                document.scan_status or "",
                "The file check result is unknown in this view. Ask staff to check it.",
            )
        )
        if document.issues is None:
            parts.append("The resident-facing warning and error list is not recorded.")
        elif not document.issues:
            parts.append("No resident-facing warnings or errors are recorded in this list.")
        for issue in document.issues or ():
            parts.append(
                f'{issue.severity.capitalize()} recorded for this document: "{issue.message}"'
            )
        sources.append(
            f"Your case: document {document.id} ({document.kind}), file check and issues"
        )
    parts.append(
        "These are recorded facts, not a decision that any document is acceptable or compliant. "
        "Ask your housing officer to explain each flag, confirm what is needed and the secure "
        "way to provide it. You cannot upload or send documents in this chat. "
        "Do not put passwords or bank details here."
    )
    return " ".join(parts), tuple(sources)
