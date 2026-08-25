# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering Lab  
**Problem Statement:** #13 — Patient Health Record Consent Management System  
**Domain:** Healthcare & Telemedicine  

## Overview

A patient-centric electronic health data gateway where patients explicitly manage granular,
time-bound consent permissions for clinics, diagnostic labs, and consulting doctors to access
their medical history.

**Actors:** Patient, Clinic Administrator

## Deliverables

| File | Description |
|---|---|
| `Requirements_Table.docx` | 5 Functional Requirements (FR-001–FR-005) + 2 Non-Functional Requirements (NFR-001, NFR-002) |
| `Use_Case_Diagram.pdf` | UML Use-Case Diagram with 2 actors, 7 use cases, «include» and «extend» relationships |
| `Use_Case_Flow.docx` | Use-Case Flow for UC-02 "Grant Consent to Clinic" — Main Success Scenario + 3 Alternate Flows |

## Requirements Summary

### Functional Requirements

| ID | Description | Priority |
|---|---|---|
| FR-001 | Grant time-bounded consent to clinic doctors | High |
| FR-002 | Revoke consent at any time before expiry | High |
| FR-003 | View full consent history (active/expired/revoked) | Medium |
| FR-004 | Clinic Admin can request record access | High |
| FR-005 | Automated expiry notification to patient | Medium |

### Non-Functional Requirements

| ID | Type | Description | Priority |
|---|---|---|---|
| NFR-001 | Security / Auditability | Append-only audit trail for all consent events | High |
| NFR-002 | Security / Encryption | TLS 1.3 in transit, AES-256 at rest | High |

## UML Use-Case Diagram Summary

- **Actors:** Patient, Clinic Administrator  
- **Use Cases:** UC-01 Grant Consent, UC-02 Revoke Consent, UC-03 View Consent Log, UC-04 Request Record Access, UC-05 View Patient Record, UC-06 Notify Patient, UC-07 Log Audit Event  
- **«include»:** Grant Consent → Log Audit Event; Revoke Consent → Log Audit Event; Request Access → Log Audit Event  
- **«extend»:** Notify Patient --extends--> Grant Consent; Notify Patient --extends--> Request Access  

## Use-Case Flow: Grant Consent to Clinic (UC-02)

**Preconditions:** Patient authenticated; Clinic Admin has submitted an access request  
**Postconditions:** Time-bounded consent token created; audit event logged; clinic notified  
**Alternate Flows:** Patient denies request; clinic attempts access after expiry; request expires before patient responds
