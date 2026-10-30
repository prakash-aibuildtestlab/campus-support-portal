# Campus Support Portal

An educational web application for the fictional University of AI (UAI),
built to practise end-to-end AI quality engineering.

## Project goal

Build a working campus support application and demonstrate how to
define requirements, assess risks, test AI behaviour, automate regression
checks, and integrate quality checks into CI/CD.

## Planned AI capabilities

1. Policy Knowledge Assistant:
   Answer accommodation policy questions using PDF-based RAG,
   with supporting source citations.

2. Contextual Support Chatbot:
   Handle multi-turn support conversations, clarification,
   context changes, and escalation.

3. Tool-Using Support Agent:
   Perform bounded workflows, such as creating maintenance tickets,
   with permission checks and user confirmation.

## Initial scope: Policy Knowledge Assistant

- Answer questions using original fictional UAI policy PDFs.
- Retrieve relevant policy content and cite supporting sources.
- Ask for clarification when necessary facts are missing.
- Explain when available evidence cannot answer a question.
- Provide policy guidance without cancelling bookings,
  approving exceptions, or issuing refunds.

## Planned quality approach

Select checks from business requirements and assessed risks.

Combine deterministic tests, AI evaluations, human review,
API tests, and browser tests where appropriate.

Define evaluation thresholds using calibration evidence and
customer impact.

## Current status

## Current status

Implemented and verified locally:
- FastAPI application.
- GET /health endpoint.
- Portal landing page.
- Two automated foundation tests passing.

Project overview, requirements, acceptance criteria, and draft
test strategy are documented.

Authentication, PDF retrieval, AI answers, database integration,
deployment, and CI/CD are not yet implemented.

## Data

UAI is fictional. Policy documents are original demonstration
materials, not official university guidance.

## Project documentation

- [Test strategy](docs/test-strategy.md)
- [Foundation test results](docs/foundation-test-results.md)

- [Project overview](docs/project-overview.md)
- [Requirements and acceptance criteria](docs/requirements.md)

- [Policy ingestion test plan](docs/policy-ingestion-test-plan.md)
- [Policy ingestion test results](docs/policy-ingestion-test-results.md)