# Project 1 — Test Strategy

Status: Draft. Planned checks are not evidence of completed testing.

## 1. Objective

Verify that residents receive accurate, authorised, evidence-supported
accommodation policy guidance through the Campus Support Portal.

Evaluate the complete application: browser, API, permissions, PDF
ingestion, retrieval, generated answers, and failure handling.

## 2. Scope

Included:
- Foundation endpoints and web interface.
- Authentication and access boundaries.
- Policy upload, validation, extraction, and retrieval.
- Answer correctness, grounding, and citations.
- Clarification, insufficient evidence, and human review.
- Security, privacy, accessibility, reliability, latency, and cost.
- Regression testing and deployment verification.

Deferred:
- Durable multi-turn conversational memory.
- Booking cancellation, refund execution, and exception approval.
- Maintenance-ticket actions.

Deferred capabilities require their own requirements and tests
before being enabled.

## 3. Risk-based selection

Start with business requirements and architecture.

Assess applicable quality areas using the reusable AI quality
assessment template. Record why each area applies or is deferred.

Select tests and metrics that detect meaningful failures.
Do not add every available DeepEval metric by default.

Priority risks:

| Risk | Customer impact | Main checks |
|---|---|---|
| Unauthorised document or history access | Privacy breach | API permission tests and cross-user/institution cases |
| Incorrect refund guidance | Financial confusion | Exact business-rule checks and answer review |
| Missing policy conditions during ingestion | Misleading answers | PDF extraction and table-preservation checks |
| Wrong policy version or applicability | Incorrect guidance | Metadata, effective-date, and ambiguity tests |
| Unsupported claims or misleading citations | Loss of trust | Grounding, citation support, and abstention checks |
| Prompt injection | Disclosure or policy bypass | Direct and retrieved-document attack scenarios |
| Service failure presented as success | Customer confusion | Timeout, dependency failure, and browser recovery tests |

## 4. Test layers

| Layer | Purpose |
|---|---|
| Unit | Check deterministic calculations, dates, validation, and permissions logic |
| Ingestion | Verify extraction, metadata, page references, and publication behaviour |
| API integration | Verify request handling, authentication, persistence, and errors |
| Retrieval | Check whether necessary authorised evidence is retrieved |
| Answer evaluation | Assess correctness, grounding, completeness, and appropriate limitations |
| Browser | Verify important user journeys, source access, and error presentation |
| Non-functional | Assess security, privacy, accessibility, latency, cost, and recovery |
| Deployment | Verify the hosted build, configuration, and essential journeys |

Use focused lower-level checks for broad coverage and selected
browser journeys for end-to-end confidence.

## 5. Evaluation approach

Use deterministic assertions where expected behaviour is exact.

Examples:
- Refund percentage and amount.
- Required response fields.
- Access-control decisions.
- Citation document existence and access.
- HTTP status codes.

Use rubric-based evaluation for semantic behaviour.

Candidates:
- Business-rule correctness rubric.
- Faithfulness to supplied evidence.
- Appropriate clarification and abstention.
- Citation support and answer completeness.

DeepEval can support automated semantic evaluation.
Human review checks rubric interpretation and evaluator mistakes.

A grounded answer can still be wrong if retrieval supplied the
wrong policy. Evaluate retrieval and answers separately.

## 6. Test data

Use original fictional PDFs and synthetic users and bookings.

Include:
- Typical questions and paraphrases.
- Refund boundaries: 0, 6, 7, 20, and 21 notice days.
- Missing, conflicting, and ambiguous facts.
- Checked-in and post-arrival cases.
- Zero prepayment and rounding cases.
- Unsupported questions and exception requests.
- Different users, roles, institutions, and policy versions.
- Malicious instructions in questions and documents.

Use explicit dates in 2027 for cases governed by the initial policy.
Do not assume a future-effective policy applies to today's request.

Each evaluation case records:
- Case ID and linked requirement.
- Input, user context, and applicable document version.
- Expected facts, behaviour, and supporting evidence.
- Evaluation method and failure severity.

Separate development, calibration, and held-out evaluation cases.
Review synthetic cases against the source policy before use.

## 7. Threshold calibration

Do not adopt a universal threshold such as 0.7.

Prepare known acceptable and unacceptable outputs.
Review them using a written rubric.
Compare automated scores with those judgements.

Investigate false passes, false failures, and repeated-run variation.
Choose thresholds based on customer impact and observed separation.

Record evaluator model, rubric, configuration, and dataset versions.

For a solo portfolio, disclose that author review is not independent
domain-expert validation.

## 8. Automation and CI/CD

Local:
- Run focused tests during development.

Pull request:
- Run deterministic unit, ingestion, and API checks.
- Add selected browser checks once available.
- Introduce budgeted live AI checks after calibration.

Scheduled or pre-release:
- Run broader live AI and adversarial regression suites.
- Compare results with the previous baseline.
- Evaluate held-out cases before a release decision.

Deployment:
- Deploy a versioned build to staging.
- Run hosted smoke tests.
- Record the deployed version and rollback procedure.

Use separate test data and controlled credentials.
Required checks that error, skip unexpectedly, or do not run
must not be reported as passing.

## 9. Results and defect reporting

Record:
- Build, dataset, document, prompt, model, and evaluator versions.
- Test totals with pass, fail, error, and skip counts.
- Results by requirement, risk, and scenario group.
- AI score distributions and repeated-run variation.
- Latency and cost under the stated workload.
- Defects, reproduction evidence, and known limitations.

Use redacted traces and correlation IDs for investigation.

Overall averages must not hide critical failures such as
cross-user disclosure or materially incorrect refund guidance.

## 10. Release readiness

For each milestone:
- Applicable acceptance criteria have supporting evidence.
- Required checks have completed successfully.
- No unresolved critical or high-severity defects remain in scope.
- AI evaluation gates are calibrated before being enforced.
- Known limitations and deferred capabilities are documented.
- Hosted smoke checks pass when deployment is included.
- Recovery and rollback steps are documented and verified
  before claiming operational readiness.

Performance and cost gates remain pending until targets and
workloads are defined.

## 11. First milestone

Implement and verify:
- FND-01: GET /health.
- FND-02: Portal landing page.
- FND-03: Automated foundation tests.

This milestone does not demonstrate RAG or AI answer quality.