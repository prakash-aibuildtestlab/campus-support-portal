from datetime import date
from pathlib import Path

import pymupdf
import pytest

from app.ingestion import (
    IngestionError,
    PolicyMetadata,
    extract_policy_pdf,
    load_manifest,
)


@pytest.fixture
def metadata():
    return PolicyMetadata(
        document_id="TEST-001",
        institution_id="UAI",
        title="Test Policy",
        version="1.0",
        effective_date=date(2027, 1, 1),
        filename="policy.pdf",
    )


def create_pdf(path, page_texts):
    """Create real PDF fixtures inside temporary test folders."""
    with pymupdf.open() as document:
        for text in page_texts:
            page = document.new_page()
            if text:
                page.insert_text((72, 72), text)
        document.save(path)


def test_real_policy_preserves_pages_and_metadata():
    """ING-03: Extract the actual project PDF."""
    source = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "source_documents"
    )
    documents = load_manifest(source / "policy_manifest.json")
    policy = next(
        item for item in documents
        if item.document_id == "UAI-ACC-001"
    )

    pages = extract_policy_pdf(policy, source)

    assert len(pages) == 3
    assert [page.page_number for page in pages] == [1, 2, 3]
    assert all(page.text.strip() for page in pages)
    assert all(page.metadata == policy for page in pages)
    assert "Accommodation Cancellation" in pages[0].text


def test_valid_pdf_extracts_expected_text(tmp_path, metadata):
    create_pdf(
        tmp_path / metadata.filename,
        ["First page evidence", "Second page evidence"],
    )

    pages = extract_policy_pdf(metadata, tmp_path)

    assert len(pages) == 2
    assert "First page evidence" in pages[0].text
    assert "Second page evidence" in pages[1].text


def test_missing_pdf_is_rejected(tmp_path, metadata):
    """ING-02: A missing file must not appear successful."""
    with pytest.raises(IngestionError, match="not found"):
        extract_policy_pdf(metadata, tmp_path)


def test_corrupt_pdf_is_rejected(tmp_path, metadata):
    """ING-02: Invalid bytes must not produce extracted pages."""
    (tmp_path / metadata.filename).write_bytes(
        b"This is not a valid PDF."
    )

    with pytest.raises(IngestionError, match="Could not extract PDF"):
        extract_policy_pdf(metadata, tmp_path)


def test_password_protected_pdf_is_rejected(tmp_path, metadata):
    """ING-02: Password-protected sources need separate handling."""
    with pymupdf.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), "Protected policy")
        document.save(
            tmp_path / metadata.filename,
            encryption=pymupdf.PDF_ENCRYPT_AES_256,
            owner_pw="test-owner",
            user_pw="test-reader",
        )

    with pytest.raises(IngestionError, match="Password-protected"):
        extract_policy_pdf(metadata, tmp_path)


def test_blank_page_is_rejected(tmp_path, metadata):
    """ING-05: Do not silently omit a page without text."""
    create_pdf(tmp_path / metadata.filename, [""])

    with pytest.raises(IngestionError, match="Page 1"):
        extract_policy_pdf(metadata, tmp_path)


def test_later_page_failure_returns_no_partial_result(tmp_path, metadata):
    """ING-06: A valid first page cannot mask a failed second page."""
    create_pdf(
        tmp_path / metadata.filename,
        ["Valid first page", ""],
    )

    with pytest.raises(IngestionError, match="Page 2"):
        extract_policy_pdf(metadata, tmp_path)


def test_symlink_outside_source_directory_is_rejected(
    tmp_path, metadata
):
    source = tmp_path / "sources"
    source.mkdir()

    outside_pdf = tmp_path / "outside.pdf"
    create_pdf(outside_pdf, ["Outside document"])
    (source / metadata.filename).symlink_to(outside_pdf)

    with pytest.raises(IngestionError, match="inside the source"):
        extract_policy_pdf(metadata, source)


def test_image_only_page_is_rejected(tmp_path, metadata):
    """ING-05: Visible text in an image requires OCR."""
    # Render text into an image, as a scanner would.
    with pymupdf.open() as original:
        page = original.new_page()
        page.insert_text((72, 72), "Scanned accommodation policy")
        image_bytes = page.get_pixmap().tobytes("png")

    # Create a PDF containing only that image.
    pdf_path = tmp_path / metadata.filename

    with pymupdf.open() as scanned:
        page = scanned.new_page()
        page.insert_image(page.rect, stream=image_bytes)
        scanned.save(pdf_path)

    # Confirm this fixture has no searchable text.
    with pymupdf.open(pdf_path) as document:
        assert document[0].get_text().strip() == ""

    with pytest.raises(IngestionError, match="Page 1"):
        extract_policy_pdf(metadata, tmp_path)


@pytest.fixture
def policy_page_two_text():
    source = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "source_documents"
    )
    policy = next(
        item for item in load_manifest(source / "policy_manifest.json")
        if item.document_id == "UAI-ACC-001"
    )

    pages = extract_policy_pdf(policy, source)

    # Ignore layout whitespace while preserving wording and order.
    return " ".join(pages[1].text.split())


@pytest.mark.parametrize(
    "expected_row",
    [
        "21 or more calendar days 100%",
        "7 to 20 calendar days, inclusive 60%",
        "0 to 6 calendar days, inclusive 25%",
    ],
)
def test_refund_table_preserves_day_rate_relationship(
    policy_page_two_text, expected_row
):
    """ING-04: Each notice period retains its correct refund rate."""
    assert expected_row in policy_page_two_text


@pytest.mark.parametrize(
    "expected_condition",
    [
        (
            "Eligibility is determined by the receipt date in section 4, "
            "even if staff process the request later."
        ),
        (
            "25% band only if the resident has not checked in."
        ),
        (
            "A request received after that date, or after check-in, "
            "is referred for review under section 1.2."
        ),
        (
            "Calculate refund = accommodation prepayment multiplied "
            "by the applicable percentage."
        ),
        (
            "Round once to the nearest Australian cent using "
            "half-up rounding."
        ),
        (
            "If the accommodation prepayment is zero, the refund is zero."
        ),
    ],
)
def test_refund_conditions_survive_extraction(
    policy_page_two_text, expected_condition
):
    """ING-04: Preserve important eligibility and calculation conditions."""
    assert expected_condition in policy_page_two_text