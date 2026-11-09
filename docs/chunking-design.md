# Policy Chunking — Initial Design

Status: Proposed baseline; not yet implemented or evaluated.

## Purpose

Create meaningful retrieval units from extracted policy pages,
preserving source identity and page references.

## Initial approach

Split by numbered top-level policy sections.

Keep subsections, tables, and associated conditions within their
parent section. For example, section 3 includes the refund table,
check-in restrictions, and calculation rules.

Support sections continuing across page boundaries.

Retain introductory document content separately.
Remove only recognised repeating page headers and footers.

Do not silently discard unrecognised content.

## Chunk metadata

Each chunk retains:
- Institution ID.
- Document ID and version.
- Effective date.
- Source filename.
- Section identifier and title.
- Source page numbers.
- Chunk identifier.
- Chunking strategy version.

## Acceptance criteria

| ID | Expected behaviour |
|---|---|
| CHK-01 | Each chunk contains non-empty text and source metadata |
| CHK-02 | Section 3 retains its refund table and all three subsections together |
| CHK-03 | Sections spanning pages retain their content and page references |
| CHK-04 | Chunk identifiers are repeatable for identical inputs and strategy |
| CHK-05 | Different institutions, documents, or versions are never merged |
| CHK-06 | Content is preserved except explicitly recognised repeating headers and footers |
| CHK-07 | Oversized sections produce an explicit error rather than silent truncation |

## Limits and evaluation

This parser initially supports our numbered policy layout.
It is not a universal PDF section detector.

Define a configurable size limit before implementation.
The initial limit is an engineering constraint, not an optimised
retrieval setting.

Cross-references still matter: section 3 depends on eligibility
in section 1 and receipt-date definitions in other sections.
Retrieving one section does not guarantee sufficient evidence.

Evaluate chunking using representative questions and labelled
supporting sections. Adjust boundaries or retrieval expansion
when evidence is incomplete.

## Recognised source layout rules

For UAI-ACC-001 version 1.0, remove the leading display titles
"Cancellation rules and requests" on page 2 and
"Exceptions and administration" on page 3.

These are page display headings, not numbered policy sections.
The rule applies only at the beginning of the cleaned page.

Other unnumbered content remains preserved.