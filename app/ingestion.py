import json
import re
import pymupdf
from dataclasses import dataclass
from datetime import date
from pathlib import Path


class IngestionError(ValueError):
    """An input document cannot be safely ingested."""


@dataclass(frozen=True)
class PolicyMetadata:
    document_id: str
    institution_id: str
    title: str
    version: str
    effective_date: date
    filename: str


def validate_metadata(record: dict) -> PolicyMetadata:
    """Validate one manifest record before opening its PDF."""
    if not isinstance(record, dict):
        raise IngestionError("Each document record must be an object.")

    required_fields = (
        "document_id",
        "institution_id",
        "title",
        "version",
        "effective_date",
        "filename",
    )

    values = {}

    for field in required_fields:
        value = record.get(field)

        if not isinstance(value, str) or not value.strip():
            raise IngestionError(
                f"'{field}' must be a non-empty string."
            )

        values[field] = value.strip()

    date_text = values["effective_date"]

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_text):
        raise IngestionError(
            "'effective_date' must use YYYY-MM-DD."
        )

    try:
        effective_date = date.fromisoformat(date_text)
    except ValueError as error:
        raise IngestionError(
            "'effective_date' must be a valid calendar date."
        ) from error

    filename = values["filename"]

    if (
        "/" in filename
        or "\\" in filename
        or not filename.lower().endswith(".pdf")
    ):
        raise IngestionError(
            "'filename' must be a PDF filename without directories."
        )

    return PolicyMetadata(
        document_id=values["document_id"],
        institution_id=values["institution_id"],
        title=values["title"],
        version=values["version"],
        effective_date=effective_date,
        filename=filename,
    )


def load_manifest(manifest_path: Path) -> list[PolicyMetadata]:
    """Load and validate all records before returning any."""
    try:
        content = manifest_path.read_text(encoding="utf-8")
        manifest = json.loads(content)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise IngestionError(
            "Manifest could not be read as valid JSON."
        ) from error

    if not isinstance(manifest, dict):
        raise IngestionError("Manifest must be a JSON object.")

    records = manifest.get("documents")

    if not isinstance(records, list) or not records:
        raise IngestionError(
            "Manifest must contain a non-empty 'documents' list."
        )

    documents = [validate_metadata(record) for record in records]

    identities = [
        (item.institution_id, item.document_id, item.version)
        for item in documents
    ]

    if len(identities) != len(set(identities)):
        raise IngestionError(
            "Manifest contains a duplicate institution/document/version."
        )

    return documents


@dataclass(frozen=True)
class PolicyPage:
    metadata: PolicyMetadata
    page_number: int
    text: str


def extract_policy_pdf(
    metadata: PolicyMetadata,
    source_directory: Path,
) -> list[PolicyPage]:
    """Return all extracted pages, or raise an ingestion error."""
    source_root = source_directory.resolve()
    pdf_path = (source_root / metadata.filename).resolve()

    # Also prevents a symbolic link from escaping the source directory.
    if not pdf_path.is_relative_to(source_root):
        raise IngestionError(
            "PDF must be located inside the source directory."
        )

    if not pdf_path.is_file():
        raise IngestionError(
            f"PDF file not found: {metadata.filename}"
        )

    pages = []

    try:
        with pymupdf.open(pdf_path) as document:
            if not document.is_pdf:
                raise IngestionError("Source file is not a PDF.")

            if document.needs_pass:
                raise IngestionError(
                    "Password-protected PDFs are not supported."
                )

            if document.is_repaired:
                raise IngestionError(
                    "PDF required repair; review or replace the source."
                )

            if document.page_count == 0:
                raise IngestionError("PDF contains no pages.")

            for page_number, page in enumerate(document, start=1):
                text = page.get_text("text", sort=True).strip()

                if not text:
                    raise IngestionError(
                        f"Page {page_number} has no extractable text. "
                        "Review the page; OCR may be required."
                    )

                pages.append(
                    PolicyPage(
                        metadata=metadata,
                        page_number=page_number,
                        text=text,
                    )
                )

    except IngestionError:
        raise
    except (OSError, RuntimeError, ValueError) as error:
        raise IngestionError(
            f"Could not extract PDF: {metadata.filename}"
        ) from error

    return pages