# Policy Chunking — Test Results

Execution date: 10 November 2026
Environment: Local macOS, Python 3.12.10
Command: python -m pytest tests/ -v

## Results

54 passed, 7 warnings in 3.02 seconds.

- 41 existing foundation and ingestion cases passed.
- 13 chunking cases passed.

## Verified behaviour

- The UAI policy produces an introduction and nine numbered sections.
- Source metadata is retained.
- Recognised page display titles do not extend preceding sections'
  page references.
- The refund table and selected conditions remain in one chunk.
- Identical inputs produce identical chunk IDs.
- Changed content changes the chunk ID.
- A synthetic section spanning two pages stays together.
- Unrecognised text is preserved in the tested example.
- Mixed institutions, documents, or versions are rejected.
- Oversized sections, empty input, and missing pages are rejected.

## Limitations

- Numbered-heading parsing supports the reviewed policy layout.
- Content preservation is not exhaustively verified for all layouts.
- Duplicate headings and invalid size settings are not directly tested.
- The 12,000-character limit is provisional.
- Retrieval quality and AI answer quality have not been evaluated.
- Dependency deprecation warnings remain visible.
- GitHub CI verification is pending.