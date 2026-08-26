# SE-LABS-PES1UG24CS089
# Software Engineering Lab 1: Requirements Engineering & Use-Case Modelling
**Course:** UE24CS341A — Software Engineering  
**Student Name:** Ashritha Kamalakar Hegde  
**SRN:** PES1UG24CS089  
**Section:** B  
**Institution:** PES University  

---

## 📌 Problem Statement: Alumni Mentorship & Mock Interview Platform
The **Alumni Mentorship & Mock Interview Platform** connects students with alumni working in specialized technical domains. The platform provides intelligent mentor matching based on domain expertise, availability-based session booking, and structured post-interview scorecard recording.

---

## 👥 System Actors
* **Student Mentee:** Searches for suitable mentors, views available slots, books sessions, and reviews mock interview feedback.
* **Alumni Mentor:** Provides mentorship and mock interviews, manages personal calendar availability, and submits post-interview scorecards.
* **Platform Administrator:** Manages platform operations, user accounts, and system integrity.

---

## 📋 Requirements Engineering Specification

### 1. Functional Requirements (FR-001 to FR-005)

| Requirement ID | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **FR-001** | The system shall recommend alumni mentors to students based on domain matching and facilitate one-click session booking. | **High** | **Pass:** The system displays at least one eligible alumni mentor matching the selected domain and allows direct booking.<br>**Fail:** No matching mentor recommendation is displayed when an eligible mentor exists. | Core functionality for connecting students with suitable alumni mentors. |
| **FR-002** | The system shall allow students to view the available dates and time slots of an alumni mentor before booking a session. | **High** | **Pass:** Selecting an alumni mentor displays their available booking slots.<br>**Fail:** The system permits booking without displaying mentor availability. | Allows students to select a suitable time and prevents scheduling conflicts. |
| **FR-003** | The system shall allow a student to book an available mentorship or mock interview session with an alumni mentor. | **High** | **Pass:** Confirming an available slot adds the session to both calendars and generates a meeting link.<br>**Fail:** Booking is not recorded in both calendars or permits booking an occupied slot. | Provides the core scheduling functionality of the platform. |
| **FR-004** | The system shall allow the alumni mentor to record a structured scorecard containing feedback and performance ratings after a mock interview session. | **High** | **Pass:** Mentor can submit the scorecard after a completed interview, and feedback stores against the student session.<br>**Fail:** Mentor cannot submit or save the scorecard post-session. | Provides structured post-interview evaluation for the student. |
| **FR-005** | The system shall allow a student to view the feedback and scorecard associated with a completed mock interview. | **Medium** | **Pass:** Student can open a completed session and view its submitted scorecard/feedback.<br>**Fail:** System fails to display the scorecard after submission[cite: 3]. | Allows students to understand performance and identify areas for improvement[cite: 3]. |

---

### 2. Non-Functional Requirements (NFR-001 & NFR-002)

| Requirement ID | Description | Priority | Acceptance Criteria | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **NFR-001** | The system shall ensure that all user profile data and feedback scorecards adhere to privacy guidelines and support soft-deletion within 24 hours of a deletion request[cite: 3]. | **High**[cite: 3] | **Pass:** Compliance confirmed via testing; deletion request soft-deletes data within 24 hours[cite: 3].<br>**Fail:** User data remains active beyond 24 hours post-request[cite: 3]. | Protects sensitive student, alumni, profile, and feedback information[cite: 3]. |
| **NFR-002** | The system shall display mentor recommendations and available booking slots within 3 seconds under normal operating conditions[cite: 3]. | **High**[cite: 3] | **Pass:** At least 95% of recommendation and availability requests complete within 3 seconds under normal load[cite: 3].<br>**Fail:** More than 5% of requests exceed 3 seconds[cite: 3]. | Provides a responsive user experience when searching for mentors and scheduling sessions[cite: 3]. |

---

## 📐 UML Use-Case Diagram

```mermaid
graph LR
    subgraph Alumni Mentorship & Mock Interview Platform
        UC1([UC-01 Find / Recommend Mentor])
        UC2([UC-02 View Mentor Availability])
        UC3([UC-03 Book Mentorship Session])
        UC4([UC-04 Conduct Mock Interview])
        UC5([UC-05 Submit Interview Scorecard])
        UC6([UC-06 View Interview Feedback])
        UC7([UC-07 Manage User Accounts])
    end

    Student([Student Mentee])
    Mentor([Alumni Mentor])
    Admin([Platform Administrator])

    Student --> UC1
    Student --> UC2
    Student --> UC3
    Student --> UC6

    Mentor --> UC2
    Mentor --> UC4
    Mentor --> UC5

    Admin --> UC7

    UC3 -. "<<include>>" .-> UC2
    UC5 -. "<<extend>>" .-> UC4
