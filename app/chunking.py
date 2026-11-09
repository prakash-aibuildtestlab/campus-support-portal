import hashlib
import json
import re
from dataclasses import asdict, dataclass

from app.ingestion import PolicyMetadata, PolicyPage


STRATEGY_VERSION = "numbered-sections-v1"
DEFAULT_MAX_CHARS = 12_000

SECTION_HEADING = re.compile(r"^([1-9]\d*)\.\s+(.+)$")
PAGE_HEADER = (
    "UNIVERSITY OF AI Residential Services | Fictional institution"
)


class ChunkingError(ValueError):
    """Source pages cannot be converted into valid chunks."""


@dataclass(frozen=True)
class PolicyChunk:
    chunk_id: str
    metadata: PolicyMetadata
    section_id: str
    section_title: str
    page_numbers: tuple[int, ...]
    text: str
    strategy_version: str


def clean_page_lines(page: PolicyPage) -> list[str]:
    """Remove only recognised header/footer lines at page boundaries."""
    lines = [
        line.strip()
        for line in page.text.splitlines()
        if line.strip()
    ]

    if lines and " ".join(lines[0].split()) == PAGE_HEADER:
        lines.pop(0)

            # Recognised display titles in this specific source layout.
    # Keep this rule scoped to the reviewed document version.
    if (
        page.metadata.document_id == "UAI-ACC-001"
        and page.metadata.version == "1.0"
    ):
        display_titles = {
            2: "Cancellation rules and requests",
            3: "Exceptions and administration",
        }
        expected_title = display_titles.get(page.page_number)

        if (
            expected_title
            and lines
            and " ".join(lines[0].split()) == expected_title
        ):
            lines.pop(0)

    footer = re.compile(
        rf"^{re.escape(page.metadata.document_id)}"
        rf"\s*\|\s*v{re.escape(page.metadata.version)}"
        rf"\s*\|\s*Effective .+"
        rf"\|\s*DEMONSTRATION ONLY\s+Page {page.page_number}$"
    )

    if lines and footer.fullmatch(" ".join(lines[-1].split())):
        lines.pop()

    return lines


def chunk_policy_pages(
    pages: list[PolicyPage],
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[PolicyChunk]:
    """Split one document into numbered sections without truncation."""
    if not pages:
        raise ChunkingError("At least one source page is required.")

    if (
        isinstance(max_chars, bool)
        or not isinstance(max_chars, int)
        or max_chars <= 0
    ):
        raise ChunkingError("max_chars must be a positive integer.")

    metadata = pages[0].metadata

    if any(page.metadata != metadata for page in pages):
        raise ChunkingError(
            "Pages must belong to the same document and version."
        )

    if [page.page_number for page in pages] != list(
        range(1, len(pages) + 1)
    ):
        raise ChunkingError(
            "Pages must be complete, ordered, and numbered from 1."
        )

    chunks = []
    section_id = "intro"
    section_title = "Document introduction"
    current_lines = []
    current_pages = []
    seen_sections = set()

    def finish_chunk():
        text = "\n".join(current_lines).strip()

        if not text:
            return

        if len(text) > max_chars:
            raise ChunkingError(
                f"Section '{section_id}' exceeds {max_chars} characters. "
                "Review the chunking design; content was not truncated."
            )

        identity = {
            "metadata": asdict(metadata),
            "section_id": section_id,
            "section_title": section_title,
            "page_numbers": current_pages,
            "text": text,
            "strategy_version": STRATEGY_VERSION,
            "max_chars": max_chars,
        }
        payload = json.dumps(
            identity,
            sort_keys=True,
            ensure_ascii=False,
            default=str,
        )
        chunk_id = hashlib.sha256(payload.encode("utf-8")).hexdigest()

        chunks.append(
            PolicyChunk(
                chunk_id=chunk_id,
                metadata=metadata,
                section_id=section_id,
                section_title=section_title,
                page_numbers=tuple(current_pages),
                text=text,
                strategy_version=STRATEGY_VERSION,
            )
        )

    for page in pages:
        lines = clean_page_lines(page)

        if not lines:
            raise ChunkingError(
                f"Page {page.page_number} has no remaining content."
            )

        for line in lines:
            heading = SECTION_HEADING.fullmatch(line)

            if heading:
                finish_chunk()

                section_id, section_title = heading.groups()

                if section_id in seen_sections:
                    raise ChunkingError(
                        f"Duplicate section heading: {section_id}"
                    )

                seen_sections.add(section_id)
                current_lines = []
                current_pages = []

            current_lines.append(line)

            if page.page_number not in current_pages:
                current_pages.append(page.page_number)

    finish_chunk()

    if not seen_sections:
        raise ChunkingError(
            "No numbered section headings found; review the layout."
        )

    return chunks