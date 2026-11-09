
from dataclasses import replace
from app.chunking import ChunkingError
from app.ingestion import PolicyPage
from pathlib import Path

import pytest

from app.chunking import chunk_policy_pages
from app.ingestion import extract_policy_pdf, load_manifest


@pytest.fixture
def policy_pages():
    source = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "source_documents"
    )
    policy = next(
        item for item in load_manifest(source / "policy_manifest.json")
        if item.document_id == "UAI-ACC-001"
    )
    return extract_policy_pdf(policy, source)


def test_policy_has_intro_and_nine_sections(policy_pages):
    chunks = chunk_policy_pages(policy_pages)

    assert [chunk.section_id for chunk in chunks] == [
        "intro", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]
    assert all(chunk.text.strip() for chunk in chunks)
    assert all(
        chunk.metadata == policy_pages[0].metadata
        for chunk in chunks
    )


def test_display_titles_do_not_extend_section_page_references(
    policy_pages,
):
    chunks = {
        chunk.section_id: chunk
        for chunk in chunk_policy_pages(policy_pages)
    }

    assert chunks["2"].page_numbers == (1,)
    assert chunks["5"].page_numbers == (2,)


def test_refund_rules_remain_in_one_chunk(policy_pages):
    refund = next(
        chunk for chunk in chunk_policy_pages(policy_pages)
        if chunk.section_id == "3"
    )
    text = " ".join(refund.text.split())

    assert refund.page_numbers == (2,)
    assert "21 or more calendar days 100%" in text
    assert "7 to 20 calendar days, inclusive 60%" in text
    assert "0 to 6 calendar days, inclusive 25%" in text
    assert "25% band only if the resident has not checked in." in text
    assert "half-up rounding" in text
    assert "No additional cancellation deduction" in text


def test_identical_inputs_produce_identical_chunk_ids(policy_pages):
    first = chunk_policy_pages(policy_pages)
    second = chunk_policy_pages(policy_pages)

    assert [chunk.chunk_id for chunk in first] == [
        chunk.chunk_id for chunk in second
    ]
    assert len({chunk.chunk_id for chunk in first}) == len(first)

def test_section_continuing_on_next_page_stays_together(policy_pages):
    """CHK-03: Preserve genuine cross-page section content."""
    metadata = policy_pages[0].metadata
    pages = [
        PolicyPage(
            metadata=metadata,
            page_number=1,
            text="1. Eligibility\n1.1 A confirmed booking is required.",
        ),
        PolicyPage(
            metadata=metadata,
            page_number=2,
            text=(
                "1.2 The resident must not have checked in.\n"
                "2. Review\n2.1 Contact Residential Services."
            ),
        ),
    ]

    chunks = chunk_policy_pages(pages)

    assert [chunk.section_id for chunk in chunks] == ["1", "2"]
    assert chunks[0].page_numbers == (1, 2)
    assert chunks[1].page_numbers == (2,)
    assert "1.1 A confirmed booking is required." in chunks[0].text
    assert "1.2 The resident must not have checked in." in chunks[0].text


def test_unrecognised_content_is_preserved(policy_pages):
    """CHK-06: Do not discard unfamiliar headings or notes."""
    metadata = policy_pages[0].metadata
    pages = [
        PolicyPage(
            metadata=metadata,
            page_number=1,
            text=(
                "Important introduction\n"
                "1. Eligibility\n"
                "Unnumbered policy note\n"
                "1.1 A confirmed booking is required.\n"
                "Additional explanation"
            ),
        )
    ]

    chunks = chunk_policy_pages(pages)

    assert chunks[0].section_id == "intro"
    assert chunks[0].text == "Important introduction"
    assert chunks[1].text == (
        "1. Eligibility\n"
        "Unnumbered policy note\n"
        "1.1 A confirmed booking is required.\n"
        "Additional explanation"
    )


@pytest.mark.parametrize(
    "changes",
    [
        {"institution_id": "OTHER"},
        {"document_id": "OTHER-001"},
        {"version": "2.0"},
    ],
)
def test_mixed_source_metadata_is_rejected(policy_pages, changes):
    """CHK-05: Never combine different source identities."""
    metadata = policy_pages[0].metadata
    pages = [
        PolicyPage(metadata, 1, "1. Eligibility\nOriginal evidence"),
        PolicyPage(
            replace(metadata, **changes),
            2,
            "2. Review\nDifferent source",
        ),
    ]

    with pytest.raises(ChunkingError, match="same document"):
        chunk_policy_pages(pages)


def test_oversized_section_is_rejected(policy_pages):
    """CHK-07: Reject rather than truncate."""
    pages = [
        PolicyPage(
            policy_pages[0].metadata,
            1,
            "1. Eligibility\n" + "Policy evidence " * 20,
        )
    ]

    with pytest.raises(ChunkingError, match="exceeds"):
        chunk_policy_pages(pages, max_chars=100)


def test_empty_input_is_rejected():
    with pytest.raises(ChunkingError, match="At least one"):
        chunk_policy_pages([])


def test_missing_page_is_rejected(policy_pages):
    pages = [policy_pages[0], policy_pages[2]]

    with pytest.raises(ChunkingError, match="complete, ordered"):
        chunk_policy_pages(pages)


def test_changed_content_changes_chunk_id(policy_pages):
    """CHK-04: Changed evidence must not reuse an old content ID."""
    metadata = policy_pages[0].metadata
    original = [PolicyPage(metadata, 1, "1. Rule\nOriginal evidence")]
    revised = [PolicyPage(metadata, 1, "1. Rule\nRevised evidence")]

    original_chunk = chunk_policy_pages(original)[0]
    revised_chunk = chunk_policy_pages(revised)[0]

    assert original_chunk.chunk_id != revised_chunk.chunk_id