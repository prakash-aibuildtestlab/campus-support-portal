# Policy Ingestion — Milestone Test Plan

Status: Planned; tests have not yet been executed.
Related requirements: REQ-04 and REQ-05.

## Scope

Validate the document manifest and extract text from a local,
administrator-controlled PDF while preserving source identity
and page numbers.

Web uploads, OCR, embeddings, and retrieval-store publication
are outside this implementation step.

## Acceptance criteria and planned tests

| ID | Scenario | Expected result |
|---|---|---|
| ING-01 | Missing, blank, or invalid required metadata | Reject before extraction with an identifiable validation error |
| ING-02 | Missing, corrupt, encrypted, or non-PDF file | Reject with a clear error |
| ING-03 | Valid policy PDF | Return non-empty page text with one-based page numbers and document identity |
| ING-04 | Extract the UAI policy | Preserve refund bands and associated conditions, checked against the source PDF |
| ING-05 | Page containing an image but no extractable text | Reject as requiring OCR; do not silently omit the page |
| ING-06 | Extraction fails after earlier pages succeed | Return an error rather than a partial successful document |

## Publication boundary

The extractor will not write to the retrieval store.
No partially extracted content can therefore be published by it.

Atomic publication will need separate integration tests when
retrieval storage is implemented.

## Data and evidence

- Use the original fictional UAI policy as the positive fixture.
- Generate invalid PDF fixtures in temporary test directories.
- Use explicit 2027 dates for policy-applicability scenarios.
- Record execution results after running the tests.