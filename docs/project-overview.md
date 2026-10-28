# Campus Support Portal — Project Overview

## Purpose

Build a working campus support application and demonstrate end-to-end
quality engineering for AI-powered features.

The project uses a fictional institution, University of AI (UAI),
original policy PDFs, and synthetic users and booking data.

## Business problem

Residents need clear answers about accommodation policies.
Staff need answers to be accurate, supported by the applicable policy,
and clear about when human review is required.

Incorrect guidance can cause financial confusion, unnecessary support
requests, and loss of trust.

## Users

- Residents: ask questions and inspect supporting policy sources.
- Policy administrators: manage authorised institutional policy documents.
- Support staff: review questions the assistant cannot resolve.

These are planned roles. Authentication and permissions are not yet built.

## Three planned capabilities

1. Policy Knowledge Assistant:
   PDF-based retrieval-augmented generation (RAG), with citations.

2. Contextual Support Chatbot:
   Multi-turn conversations, clarification, context changes, and escalation.

3. Tool-Using Support Agent:
   Bounded actions, such as creating maintenance tickets, with permission
   checks, confirmation, and verification of the resulting system state.

## Project 1 scope

Build the Policy Knowledge Assistant first.

A resident asks a question through a web interface.
The backend retrieves relevant, authorised PDF content.
An LLM generates an answer using that evidence.
The interface displays the answer and its supporting sources.

Initial questions are independent. Durable conversational memory is
outside this first scope.

## Boundaries

The initial assistant provides policy guidance.

It cannot cancel bookings, approve exceptions, issue refunds,
or claim that any of those actions have occurred.

## Planned technical components

- Frontend: HTML, CSS, and JavaScript.
- Backend: Python and FastAPI.
- Policy ingestion: PDF extraction, chunking, and metadata validation.
- Retrieval: embeddings and Chroma vector storage.
- Generation: configurable LLM integration.
- Application data: PostgreSQL.
- Testing: Pytest, HTTPX, selected Playwright tests, and DeepEval.
- Delivery: GitHub Actions and a hosted demonstration environment.

Components will be added incrementally and documented as implemented.

## Current implementation

- Local Python environment and GitHub repository established.
- Application foundation in progress.
- Health endpoint being introduced.

RAG, authentication, database integration, deployment, and CI/CD
are not yet implemented.

## Success evidence

- A working browser-to-backend-to-retrieval-to-model user journey.
- Traceable requirements, risks, tests, and evaluation results.
- Evidence that important failure cases are handled.
- Repeatable automated regression checks.
- A hosted demo and documented limitations.