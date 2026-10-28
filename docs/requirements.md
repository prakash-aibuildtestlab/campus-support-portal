# Project 1 — Requirements and Acceptance Criteria

Status: Draft baseline. These criteria describe intended behaviour,
not completed or verified functionality.

| ID | Requirement | Acceptance criteria |
|---|---|---|
| REQ-01 | Authenticate users | Unauthenticated requests to protected chat, history, and document endpoints are rejected. Logging out invalidates the session. |
| REQ-02 | Enforce institutional and user boundaries | The backend derives access from authenticated identity. Changing a URL, request field, or prompt cannot expose another institution's documents or another user's history. |
| REQ-03 | Restrict policy administration | Only authorised administrators can manage policies for their institution. Resident attempts are rejected by the backend. |
| REQ-04 | Validate PDF uploads | Supported PDFs require document ID, institution, version, and effective date. Corrupt or unsupported files produce a clear failure and are not searchable. |
| REQ-05 | Preserve policy evidence | Ingestion preserves refund bands, conditions, and page references. Failed or incomplete ingestion does not publish a partially processed document. |
| REQ-06 | Retrieve applicable evidence | Retrieval uses authorised documents and appropriate policy applicability. Ambiguous applicability results in clarification or human review. |
| REQ-07 | Explain refund rules correctly | For eligible cases, responses preserve the policy's inclusive day boundaries, percentages, and check-in restrictions. Post-arrival and post-check-in cases require review. |
| REQ-08 | Calculate amounts correctly | Calculations use accommodation prepayment, Melbourne calendar dates, and the policy's rounding rule. Zero prepayment produces a zero refund estimate. |
| REQ-09 | Clarify missing facts | Personalised answers request necessary missing facts without inventing them. General policy questions can be answered without collecting unnecessary personal details. |
| REQ-10 | Provide supporting citations | Policy claims cite the correct document version and supporting page or section. Users can access only sources they are authorised to view. |
| REQ-11 | Handle insufficient evidence | Unsupported questions receive an explicit limitation and the defined staff review route. The assistant does not invent policy rules or contact details. |
| REQ-12 | Respect decision boundaries | Exception requests are referred for human review. Responses do not claim to approve exceptions, cancel bookings, or issue payments. |
| REQ-13 | Resist instruction attacks | Instructions inside prompts or retrieved PDFs cannot bypass permissions, expose credentials, or trigger unauthorised actions. Tests cover direct and document-based attacks. |
| REQ-14 | Support usable and honest interactions | The interface supports keyboard operation, loading and error states, and accessible citations. AI output is rendered safely. Failed requests are not displayed as successful answers. |
| REQ-15 | Support investigation | Requests have correlation identifiers and relevant model, prompt, and retrieval version information. Logs exclude credentials and restrict sensitive information. |
| REQ-16 | Capture feedback safely | Feedback is associated with the correct answer and request. Users cannot submit feedback against another user's private interaction. |

## Foundation milestone

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FND-01 | Expose application liveness | GET /health returns HTTP 200 and JSON {"status":"ok"} when the application is running. This does not assert database or AI readiness. |
| FND-02 | Serve the portal page | GET / returns HTTP 200 and displays the Campus Support Portal title. |
| FND-03 | Automate foundation verification | Automated tests verify the health endpoint and portal response. A failing assertion produces a failing test run. |

## Decisions still required

- Policy transitions for requests received before the policy effective date.
- Supported upload sizes, scanned PDFs, and document replacement behaviour.
- Response-time and cost targets under a defined workload.
- Data retention and approved monitoring fields.
- Evaluation rubrics and thresholds, based on calibration evidence.
- Detailed accessibility checks and staff escalation experience.

## Traceability

Tests will reference requirement IDs.
Risks and test results will be linked as the implementation grows.

Numerical AI evaluation thresholds are not approved merely by appearing
in a draft document.