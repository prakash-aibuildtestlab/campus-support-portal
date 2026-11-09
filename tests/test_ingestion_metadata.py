import json
from datetime import date

import pytest

from app.ingestion import (
    IngestionError,
    load_manifest,
    validate_metadata,
)


@pytest.fixture
def valid_record():
    """Synthetic metadata used independently by each test."""
    return {
        "document_id": "UAI-ACC-001",
        "institution_id": "UAI",
        "title": "Accommodation Cancellation and Refund Policy",
        "version": "1.0",
        "effective_date": "2027-01-01",
        "filename": "policy.pdf",
    }


def test_valid_metadata_is_accepted(valid_record):
    metadata = validate_metadata(valid_record)

    assert metadata.document_id == "UAI-ACC-001"
    assert metadata.institution_id == "UAI"
    assert metadata.version == "1.0"
    assert metadata.effective_date == date(2027, 1, 1)
    assert metadata.filename == "policy.pdf"


@pytest.mark.parametrize(
    "field",
    [
        "document_id",
        "institution_id",
        "title",
        "version",
        "effective_date",
        "filename",
    ],
)
def test_missing_required_field_is_rejected(valid_record, field):
    del valid_record[field]

    with pytest.raises(IngestionError, match=field):
        validate_metadata(valid_record)


@pytest.mark.parametrize("value", ["", "   ", None, 123])
def test_invalid_field_value_is_rejected(valid_record, value):
    valid_record["institution_id"] = value

    with pytest.raises(IngestionError, match="institution_id"):
        validate_metadata(valid_record)


@pytest.mark.parametrize(
    "value",
    ["01/01/2027", "2027-1-1", "2027-02-30"],
)
def test_invalid_effective_date_is_rejected(valid_record, value):
    valid_record["effective_date"] = value

    with pytest.raises(IngestionError, match="effective_date"):
        validate_metadata(valid_record)


@pytest.mark.parametrize(
    "filename",
    ["../policy.pdf", "/tmp/policy.pdf", r"folder\policy.pdf", "policy.txt"],
)
def test_invalid_filename_is_rejected(valid_record, filename):
    valid_record["filename"] = filename

    with pytest.raises(IngestionError, match="filename"):
        validate_metadata(valid_record)


def test_duplicate_policy_version_is_rejected(tmp_path, valid_record):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"documents": [valid_record, valid_record]}),
        encoding="utf-8",
    )

    with pytest.raises(IngestionError, match="duplicate"):
        load_manifest(manifest_path)


def test_malformed_manifest_is_rejected(tmp_path):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text('{"documents":', encoding="utf-8")

    with pytest.raises(IngestionError, match="valid JSON"):
        load_manifest(manifest_path)


def test_valid_manifest_loads(tmp_path, valid_record):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(
        json.dumps({"documents": [valid_record]}),
        encoding="utf-8",
    )

    documents = load_manifest(manifest_path)

    assert len(documents) == 1
    assert documents[0].document_id == "UAI-ACC-001"