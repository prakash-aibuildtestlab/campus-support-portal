# Policy Ingestion — Test Results

Execution date: 30 October 2026
Environment: Local macOS, Python 3.12.10
Command: python -m pytest tests/ -v

## Results

41 passed, 7 warnings in 1.35 seconds.

| Area | Cases | Result |
|---|---:|---|
| Application foundation | 2 | PASS |
| Metadata and manifest validation | 21 | PASS |
| PDF extraction and source-content checks | 18 | PASS |

## Evidence

- Original UAI policy extracted into three numbered pages.
- Document metadata retained on each page.
- Tested missing, corrupt, and password-protected PDFs.
- Tested blank and image-only pages.
- A second-page failure raises an error instead of returning partial results.
- Symbolic links outside the source directory are rejected.
- Refund table rows retain the expected day-to-percentage relationships.
- Six selected eligibility and calculation conditions survive extraction.

## Warnings

Seven dependency deprecation warnings were reported during the run,
concerning SWIG types. A further swigvarlink warning appeared at
interpreter shutdown. These remain visible and require dependency
compatibility review.

## Limitations

- Selected source checks do not verify every sentence in the policy.
- The repaired-PDF rejection branch has not been directly tested.
- Metadata validation coverage is not exhaustive.
- OCR is not implemented.
- No retrieval-store publication is implemented or tested.
- Authentication, retrieval, generated answers, and deployment
  are outside this milestone's evidence.
- GitHub CI results are pending.