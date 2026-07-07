# Software Requirements Specification (SRS)

**Project Name:** AI-Based Smart Route Ride-Sharing System  
**Product Version:** 1.0.0 (Production-Inspired MVP)  
**Date:** July 7, 2026  
**Document Status:** Approved for Implementation  
**Prepared By:** === FILLED BY USER ===  
**Organization:** === FILLED BY USER ===  
**Client:** === FILLED BY USER ===  
**Confidentiality Statement:** === FILLED BY USER ===  
**Document Classification:** === FILLED BY USER ===  

---

## Document Control

### Revision History
| Ver. | Date | Author | Reviewer(s) | Description of Change |
|---|---|---|---|---|
| 0.1.0 | 2026-07-01 | === FILLED BY USER === | === FILLED BY USER === | Initial draft outline & requirements gathering. |
| 1.0.0 | 2026-07-07 | === FILLED BY USER === | === FILLED BY USER === | Baseline release mapping fully to source models and features. |

### Approvals
| Name | Role | Signature | Date |
|---|---|---|---|
| === FILLED BY USER === | === FILLED BY USER === | === FILLED BY USER === | === FILLED BY USER === |

### Distribution List
| Name / Group | Organization / Role | Date Shared |
|---|---|---|
| === FILLED BY USER === | === FILLED BY USER === | === FILLED BY USER === |

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Overall Description](#2-overall-description)
- [3. Stakeholders](#3-stakeholders)
- [4. Functional Requirements](#4-functional-requirements)
- [5. Non-Functional Requirements](#5-non-functional-requirements)
- [6. User Roles & Permissions Matrix](#6-user-roles--permissions-matrix)
- [7. User Journey Maps](#7-user-journey-maps)
- [8. Complete System Modules](#8-complete-system-modules)
- [9. Use Cases](#9-use-cases)
- [10. User Stories](#10-user-stories)
- [11. Workflows (ASCII Diagrams)](#11-workflows-ascii-diagrams)
- [12. Database Design](#12-database-design)
- [13. API Documentation](#13-api-documentation)
- [14. AI Module Specifications](#14-ai-module-specifications)
- [15. Email System](#15-email-system)
- [16. Security Infrastructure](#16-security-infrastructure)
- [17. UI/UX Design System](#17-ui/ux-design-system)
- [18. External Integrations](#18-external-integrations)
- [19. Deployment Guide](#19-deployment-guide)
- [20. Testing & Verification](#20-testing--verification)
- [21. Risks Assessment](#21-risks-assessment)
- [22. Future Enhancements](#22-future-enhancements)
- [23. Maintenance Strategy](#23-maintenance-strategy)
- [24. Project Timeline](#24-project-timeline)
- [25. Budget & Cost Breakdown](#25-budget--cost-breakdown)
- [26. Legal & Compliance](#26-legal--compliance)
- [27. Appendices](#27-appendices)

---

## 1. Introduction

This document defines the Software Requirements Specification (SRS) for the AI-Based Smart Route Ride-Sharing System (herein referred to as 'Ride-Share'). It lays out the comprehensive functional, non-functional, security, and architectural specifications that govern the implementation and verification of the platform's production MVP.

**1.1 Purpose: ** The primary objective of this document is to establish a rigorous, industry-grade baseline requirements specification. This serves as the ground truth for developers, quality assurance engineers, administrators, and university/organizational compliance evaluators. A software development team can directly initiate database schema setups, API routing, frontend interface coding, and system testing from this document.

**1.2 Scope: ** The Ride-Share system is an offline-capable Progressive Web Application (PWA) facilitating path-sequence carpooling matches. Rather than basic start-to-end taxi matches, Ride-Share incorporates geodetic route waypoint sequences (via Leaflet.js maps) to identify drivers and passengers traveling on overlapping routes. It handles secure role-based registration, vehicle verification, automated match rankings based on mathematical proximity detours and trust relationships (shared corporate/college organizations, friendships, event attendance), real-time instant messaging with attachment handling, simulated checkout and payments, a SOS panic telemetry system, and an AI-driven automated support framework.

**1.3 Intended Audience: ** This document is targeted at backend/frontend engineers, QA test practitioners, DevOps deployment teams, evaluators, and system managers. Reading this document requires intermediate knowledge of Django MVC architectures, REST APIs, databases, geodetic route sequencing, and Web App service caching systems.

**1.4 Definitions: ** Terms used in this document are defined as follows:

* **Driver: ** A registered traveler who owns a vehicle, publishes carpooling offers with sequential geographic stop waypoints, and charges passenger fares to offset transit expenses.
* **Passenger: ** A traveler who searches for ride listings matching their sequential pickup/drop points, requests bookings, and performs simulated payments.
* **Waypoint: ** An ordered set of GPS coordinates (latitude, longitude) along a driver's route representing stops or pick-up/drop-off intervals.
* **Detour Proximity: ** The total deviation distance in kilometers that a driver must execute to accommodate a passenger's pickup and drop-off points.
* **Social Affiliation: ** Shared context metrics (common employer, college, friends) used to calculate safety and trust ratings.
**1.5 Acronyms: ** The following acronyms are used throughout this document:

* SRS: Software Requirements Specification
* PWA: Progressive Web Application
* API: Application Programming Interface
* OSM: OpenStreetMap
* OSRM: Open Source Routing Machine
* JWT: JSON Web Token
* CSRF: Cross-Site Request Forgery
* XSS: Cross-Site Scripting
* CORS: Cross-Origin Resource Sharing
* GDPR: General Data Protection Regulation
* SMTP: Simple Mail Transfer Protocol
**1.6 Abbreviations: ** The following abbreviations are utilized: 'Ver.' (Version), 'Temp.' (Template), 'Notif.' (Notification), 'Org' (Organization), 'DB' (Database), 'Sec.' (Section), 'Req.' (Requirement).

**1.7 References: ** Key reference documents and standards include:

* IEEE Std 830-1998: Recommended Practice for Software Requirements Specifications.
* ISO/IEC/IEEE 29148:2018: Systems and software engineering - Lifecycle processes - Requirements engineering.
* Django 6.0 Web Framework Documentation (https://docs.djangoproject.com/)
* Leaflet.js Mapping Library API (https://leafletjs.com/)
* Google Gemini API Documentation (https://ai.google.dev/)
* Ride-Share Active Database models (core/models.py) and view logic (core/views.py, core/views_extended.py).
**1.8 Business Context: ** Urban centers face massive traffic congestions, escalating vehicle ownership costs, and carbon footprints. Conventional commercial taxi aggregators charge steep surge fares while taking large commissions. A community-based peer-to-peer carpooling platform enables commuters to offset fuel costs while helping passengers commute affordably in a secure, trust-validated circle.

**1.9 Background: ** The project was designed as a high-fidelity academic prototype showing clean software engineering principles. It integrates geodetic calculations, web caching, maps, and AI modules into a single lightweight Django package to prove technical capability without high infrastructure billing overheads.

**1.10 Project Vision: ** To deliver a seamless, offline-first, geodetically intelligent carpooling platform that eliminates search friction, minimizes detours, maximizes personal safety, and handles inquiries through advanced AI integrations.

**1.11 Objectives: ** 1. Provide sequential route matching calculations with low latencies. 2. Enable installable, offline-first dashboards to handle connectivity interruptions. 3. Establish a trust network combining identity document vetting and social circle metrics. 4. Offer an AI helper chatbot and travel itinerary builder.

**1.12 Success Criteria: ** 1. All unit tests execute successfully. 2. 100% database seeding via custom commands. 3. Offline dashboard renders when network is lost. 4. Geodetic matching yields correct sequence outputs.


## 2. Overall Description

**2.1 Product Perspective: ** Ride-Share is a standalone Progressive Web Application running a Django 6 backend and HTML5/Bootstrap client interface. It integrates with OpenStreetMap API via Leaflet.js to sequence route coordinates, utilizes the local database (SQLite/PostgreSQL) for persistence, and interacts with Google's Gemini-1.5-flash LLM model to offer conversational customer helpdesk support and route itinerary suggestions.

**2.2 Product Positioning: ** Positions itself as a private, high-trust, cost-sharing carpooling solution for universities, corporations, and structured communities, bridging the gap between informal messaging group arrangements and commercial taxi services.

**2.3 Business Goals: ** Reduce daily commuting expenses by dividing vehicle fuel costs equally among passengers, and decrease the number of single-occupancy vehicles on key arterial corridors.

**2.4 Product Features: ** The primary capabilities include: 1. Sequential Waypoint Matching Engine. 2. Leaflet Map Editor. 3. Mock Real-time Vehicle Tracking. 4. SOS Emergency Alarms. 5. Social Communities (College, Org, Friends). 6. Event RSVPs. 7. Real-Time Chat with File Upload. 8. Verification & Reputation. 9. AI Assistants (Chatbot, Trip Planner, support reply auto-classifier). 10. Service Worker PWA Offline mode.

**2.5 User Classes: ** The system identifies three primary user categories: Passengers, Drivers, and Administrators.

**2.6 User Characteristics: ** Users are assumed to be daily commuters (students or office workers) possessing a mobile device or laptop with an internet browser. Users require zero training to navigate the interface due to intuitive, standard web UI structures.

**2.7 Operating Environment: ** Client-side: Any modern web browser (Chrome, Safari, Firefox, Edge). Can be installed as a PWA locally. Server-side: Hosted on standard Python 3.10+ runtimes on Windows or Linux, using SQLite for development/testing and PostgreSQL for production environments.

**2.8 Development Environment: ** Local Windows/OSX/Linux machine, Python virtual environment, Visual Studio Code / Cursor IDE, git version control, and django CLI tools.

**2.9 Technology Stack: ** The platform is constructed on: Backend: Django 6.0, Django Channels (WebSockets). Frontend: HTML5, CSS3 Custom Properties (Light/Dark themes), Bootstrap 5, JavaScript (ES6). Maps: Leaflet.js with OpenStreetMap tiles, Nominatim API, OSRM. Database: SQLite (local file) / PostgreSQL. AI: Google Gemini-1.5-flash API via Google Generative AI SDK.

**2.10 Design Constraints: ** Must run on low-bandwidth connections. The route-matching algorithm must not use external paid APIs (e.g. Google Maps API) and must perform calculations locally. Service worker caching must adhere to PWA standards. Database writes must occur safely in SQLite without concurrency deadlocks.

**2.11 Assumptions: ** 1. **Assumption:** The host browser supports ES6 and Service Workers. 2. **Assumption:** The network allows HTTPS connections to external OpenStreetMap servers. 3. **Assumption:** Seeding coordinates resemble genuine roadways to ensure math logic succeeds.

**2.12 Dependencies: ** Availability of OSM mapping server layers, OSRM router server for path calculation, and internet connectivity to communicate with Google's Gemini LLM API.

## 3. Stakeholders

The stakeholders involved in the life-cycle and operation of the Ride-Share platform are classified below:

| Stakeholder | Description / Role | Primary Concerns / Requirements |
| --- | --- | --- |
| Project Owner | === FILLED BY USER === | Ensures project timelines are met, budget compliance, and overall business value. |
| Client | === FILLED BY USER === | Acceptance testing, deployment validation, and core feature alignment. |
| End Users - Passenger | Commuters seeking affordable transit. | Accurate search matches, low fare costs, verification trust, and emergency SOS alerts. |
| End Users - Driver | Vehicle owners seeking cost offset. | Simple route publishing, seating capacity control, passenger verification, and safe navigation. |
| Administrators | Operational managers and monitors. | User verification approval, system metrics monitoring, and handling safety reports/support tickets. |
| Developers | Software engineering team. | Clean codebase, fast local seeding, standard API paths, and robust testing frameworks. |
| Testers | Quality Assurance team. | Comprehensive unit/integration testing, security vulnerabilities checks, and cross-browser testing. |
| Support Team | Customer helpdesk staff. | Access to support tickets list, AI-assisted auto replies, and dashboard controls. |
| Management | === FILLED BY USER === | Strategic decisions, marketing, and scaling plans. |
| External Services | Leaflet, OSM, Gemini APIs. | API stability, rate-limiting quotas, response times, and connection security. |
| Third-party Providers | === FILLED BY USER === | Hosting servers (Render, Vercel), email SMTP relays, and domain name registrars. |

## 4. Functional Requirements

This section details the primary functional requirements of the Ride-Share platform. All features are categorized with unique tracking IDs, input/output paths, priorities, and acceptance criteria.

**FR-001: Account Registration** 

* **Description: ** Allows a user to create a new profile as a Passenger or Driver.
* **Priority: ** High
* **Inputs: ** Username, email, password, role choice (Driver/Passenger), phone number.
* **Outputs: ** Database user record, email verification token, redirection to login page.
* **Preconditions: ** The username must be unique; email must not already exist in DB.
* **Postconditions: ** A User record is saved with verified flags set to False. An activation email is logged/simulated.
* **Acceptance Criteria: ** The system validates password strength, triggers checking of username uniqueness via AJAX helper, and stores the user role choice correctly.
* **Dependencies: ** Database engine, Email verification system.
**FR-002: User Authentication (Login / Logout)** 

* **Description: ** Authenticates returning users, issues secure session cookies, and records login history (UserSession model).
* **Priority: ** High
* **Inputs: ** Username or Email, Password.
* **Outputs: ** Session ID, UserSession record in DB, redirection to role-specific dashboard.
* **Preconditions: ** User must possess an active, registered account. Verification of email is recommended but not blocking for MVP login.
* **Postconditions: ** User is authenticated; a UserSession model registers IP address, user agent, and device type.
* **Acceptance Criteria: ** Invalid credentials prompt error messages. Successful login creates a session cookie. Redirection lands on Passenger, Driver, or Admin panel depending on User.role.
* **Dependencies: ** Django Auth framework, Database engine.
**FR-003: Vehicle Details Management** 

* **Description: ** Allows a Driver to register and update their vehicle properties.
* **Priority: ** High
* **Inputs: ** Make, model, license plate, seating capacity, color.
* **Outputs: ** Vehicle record associated with the Driver's profile in DB.
* **Preconditions: ** Authenticated user must have the role of 'DRIVER'.
* **Postconditions: ** Vehicle record is created; verified status set to False until admin review.
* **Acceptance Criteria: ** The license plate must be unique. Seating capacity must be a positive integer. Vehicle details are accessible on profile fields.
* **Dependencies: ** FR-002, DB Engine.
**FR-004: Publish Ride Offer** 

* **Description: ** Enables a Driver to schedule a carpooling offer, selecting route waypoints on an interactive map editor.
* **Priority: ** High
* **Inputs: ** Vehicle selection, start location address, end location address, departure time, seat price, available seats, cost sharing terms, luggage details, emergency contact, list of ordered map waypoint coordinates.
* **Outputs: ** Ride record, sequential RouteWaypoint records linked via ForeignKey, redirection to active list.
* **Preconditions: ** Driver is logged in and has at least one registered vehicle in the system.
* **Postconditions: ** Ride record is saved with status 'ACTIVE' (or 'DRAFT'). RouteWaypoint coordinates sequence is indexed into DB.
* **Acceptance Criteria: ** Waypoints are sequenced on the Leaflet map and stored in sequence_order. Available seats must be less than or equal to the selected vehicle's capacity. Price must be positive.
* **Dependencies: ** FR-003, Leaflet/OSM map scripts.
**FR-005: Intelligent Geodetic Route Waypoint Matching Search** 

* **Description: ** Allows passengers to query routes. The backend computes matches by scanning sequential waypoints and calculating detour distances using the Haversine formula, returning ranked recommendations with social trust boosts.
* **Priority: ** High
* **Inputs: ** Pickup location coordinates, dropoff location coordinates, seats needed, maximum walk distance (km).
* **Outputs: ** Ordered JSON list of matching Ride models, pickup/dropoff walk distances, base scores, trust boosts, match reasons, and final recommendation scores.
* **Preconditions: ** Passenger is logged in. Active rides must exist in the database with departure time >= current time.
* **Postconditions: ** No data is modified. Read-only recommendation scoring list is returned to user interface.
* **Acceptance Criteria: ** Matches are filtered to ensure pickup waypoint sequence index is less than dropoff waypoint sequence index (guarantees heading in the same direction). Matches are sorted with recommendation score descending (Base Proximity + Trust boosts). Walk distance must be <= maximum walk detour constraint.
* **Dependencies: ** route_matching.py logic, SQLite spatial decimals.
**FR-006: Create Ride Booking** 

* **Description: ** Enables a Passenger to book seats on a matched ride route.
* **Priority: ** High
* **Inputs: ** Ride ID, pickup location, dropoff location, pickup lat/lng, dropoff lat/lng, seats requested.
* **Outputs: ** Booking record in DB with status 'PENDING', fare estimation total, notification to driver.
* **Preconditions: ** Passenger is logged in. Selected ride has available seats >= requested seats.
* **Postconditions: ** Booking is registered in DB; driver is sent a Notification model alert (type 'TRIP_REQUEST').
* **Acceptance Criteria: ** The total price is calculated as (seats_requested * ride.price_per_seat). System validates that driver is not booking their own ride.
* **Dependencies: ** FR-004, Notification model.
**FR-007: Booking Approval Lifecycle** 

* **Description: ** Allows a Driver to accept or reject pending bookings, modifying seats availability.
* **Priority: ** High
* **Inputs: ** Booking ID, Action choice (Accept / Reject).
* **Outputs: ** Updated Booking record status, Notification model alert to passenger, modified Ride available_seats count.
* **Preconditions: ** The logged-in user must be the Driver who published the corresponding Ride.
* **Postconditions: ** Booking status transitions to 'ACCEPTED' or 'REJECTED'. If accepted, Ride.available_seats decrements by Booking.seats_requested.
* **Acceptance Criteria: ** Declining a booking releases seats. Accepting a booking automatically checks if seats capacity is exceeded, updating DB transactionally. Redirection logs confirmation.
* **Dependencies: ** FR-006, Notification module.
**FR-008: Real-Time Chat & File Attachment** 

* **Description: ** Provides chat rooms for rides, communities, or direct users, allowing file attachment uploads.
* **Priority: ** Medium
* **Inputs: ** Room type (RIDE/COMMUNITY/DIRECT), Room ID, text content, optional file payload.
* **Outputs: ** Message record in DB, live message broadcast (Django Channels Websocket or polling fallback).
* **Preconditions: ** User is a member of the community, active passenger/driver in the ride, or verified friend of direct contact.
* **Postconditions: ** Message model is stored; notification of unread message is flagged for recipient.
* **Acceptance Criteria: ** Attachments are checked for safety. File size limit is 5MB. Messages are rendered in chronological order. HTML tag sanitization is applied.
* **Dependencies: ** Message model, media upload directory.
**FR-009: Social Communities Creation & Member Moderation** 

* **Description: ** Allows users to create groups based on domains (college or employer) to filter ride circles.
* **Priority: ** Medium
* **Inputs: ** Community name, category, description, type (Public/Private), avatar/banner graphics, joining rules.
* **Outputs: ** Community record, CommunityMember record with role 'ADMIN' for the creator.
* **Preconditions: ** Creator is an authenticated user with verified credentials (if creating private/domain groups).
* **Postconditions: ** Community model added. Members can query and join.
* **Acceptance Criteria: ** Domain emails match domain rules. Joining request status defaults to 'PENDING' for private groups, requiring Community Admin approval action.
* **Dependencies: ** Community, CommunityMember models.
**FR-010: Event Scheduling & RSVPs** 

* **Description: ** Provides events creation inside communities, enabling carpooling planning to a common venue (e.g. hackathons, trek meetups).
* **Priority: ** Medium
* **Inputs: ** Title, description, location, date, event type, community selection.
* **Outputs: ** Event record, EventAttendee record with status 'GOING' for creator.
* **Preconditions: ** User is a member of the chosen community.
* **Postconditions: ** Event details listed; community members can post RSVP status choice (GOING/INTERESTED).
* **Acceptance Criteria: ** RSVPs update attendee records instantly. Users attending the same event receive a +10 trust boost in route search.
* **Dependencies: ** Event, EventAttendee models.
**FR-011: Simulated SOS Emergency Alerts** 

* **Description: ** Enables a passenger or driver in danger to trigger an alarm, generating live telemetry and sounding a local warning siren.
* **Priority: ** High
* **Inputs: ** Ride ID, current coordinates (latitude, longitude).
* **Outputs: ** SOSAlert record in DB, active status notification, audible sound activation on frontend client, admin logs alert.
* **Preconditions: ** The user is an active passenger or driver on a trip with status 'ACTIVE'.
* **Postconditions: ** An active SOSAlert record is stored. Emergency contact fields in Ride are logged for escalation.
* **Acceptance Criteria: ** Audible alert triggers immediately. Latency to save the SOSAlert record must be under 50ms. Admin panel displays active alarms in flashing red.
* **Dependencies: ** SOSAlert model, Frontend JS audio element.
**FR-012: ID and Domain Email Verification** 

* **Description: ** Validates user trust levels using ID image uploads and corporate/college email verification tokens.
* **Priority: ** Medium
* **Inputs: ** File upload (Gov ID card) or domain email input (e.g. student@college.edu).
* **Outputs: ** Database verification token, profile status changes, email verification log.
* **Preconditions: ** Authenticated user is logged in.
* **Postconditions: ** is_email_verified or is_gov_id_verified set to True upon token entry or admin review.
* **Acceptance Criteria: ** Vetting token expires in 24 hours. Verification email is simulated with a custom link containing the token parameter. Correct token entry updates status.
* **Dependencies: ** EmailVerificationToken model, Email dispatch framework.
**FR-013: AI Support Chatbot Help Desk** 

* **Description: ** Integrates a 24/7 support assistant powered by Gemini-1.5-flash to reply to platform FAQs, safety procedures, and community questions.
* **Priority: ** Medium
* **Inputs: ** User question, chat history text.
* **Outputs: ** AI response string, AILog record in database.
* **Preconditions: ** User is authenticated and logged in.
* **Postconditions: ** Question and reply are written to the AILog table with log_type set to 'CHATBOT'.
* **Acceptance Criteria: ** If Gemini API key is missing, system falls back to predefined string matching (e.g. if 'sos' is queried, returns standard emergency instructions). Responses are formatted in markdown.
* **Dependencies: ** Gemini API, AILog model, ai_services.py.
**FR-014: AI Travel Itinerary Planner** 

* **Description: ** Uses Gemini to construct travel itineraries between source and destination endpoints, detailing route advice, local stops, weather forecasts, and packing lists.
* **Priority: ** Medium
* **Inputs: ** Source address, destination address, travel preferences description.
* **Outputs: ** Markdown-formatted itinerary page, AILog entry.
* **Preconditions: ** User is authenticated.
* **Postconditions: ** Generates AILog entry with type 'TRAVEL_ASSISTANT'.
* **Acceptance Criteria: ** If API fails, a formatted high-quality mock response containing NH route details is rendered. Formatted chapters match the standard output headings (Estimated Route, Hotels, Weather, packing checklists).
* **Dependencies: ** Gemini API, AILog model.
**FR-015: Support Ticket Creation & AI Auto-Reply Classifier** 

* **Description: ** Allows visitors to submit support tickets. The backend processes the email contents through Gemini to detect the category, draft an auto-response, and determine if admin escalation is required.
* **Priority: ** Medium
* **Inputs: ** Name, email, subject, message body.
* **Outputs: ** SupportTicket record, AI classification parameters, AILog, notification email details.
* **Preconditions: ** None (Accessible on public contact view).
* **Postconditions: ** A SupportTicket record is stored. Ticket status set to 'OPEN'. Needs_escalation boolean is saved. AI draft auto-reply is saved in ticket fields.
* **Acceptance Criteria: ** The ticket is assigned a unique alphanumeric ticket number (e.g. RS-XXXXX). Emails containing safety threats or abuse trigger needs_escalation=True automatically. Admin dashboard shows classified tickets sorted by status and urgency.
* **Dependencies: ** SupportTicket model, Gemini API classifier, ai_services.py.

## 5. Non-Functional Requirements

This section outlines the non-functional requirements (NFRs) that specify the system's operational standards, security baselines, and quality attributes.

* **Performance: ** The route-matching algorithm (Haversine sequential checks) must compute matches in less than 100ms for database sizes up to 10,000 active rides. Main dashboard pages must render in under 1.5 seconds under ordinary network latencies.
* **Availability: ** Target system availability is 99.9% uptime (excluding scheduled maintenance windows, which must occur during off-peak hours 2:00 AM - 4:00 AM UTC).
* **Reliability: ** The Mean Time Between Failures (MTBF) must be greater than 500 operating hours. Data corruption rate must remain at 0% by executing atomic transactions on database bookings.
* **Scalability: ** The application architecture separates static assets (served via Whitenoise or CDN) from computational routes. For production, the database engine must transition from SQLite to PostgreSQL to support connection pooling and up to 5,000 concurrent user sessions.
* **Maintainability: ** The backend must strictly adhere to Django MVC architecture and PEP-8 coding style guidelines. Code changes must achieve a minimum of 80% unit test coverage before deployment approval.
* **Security: ** All user passwords must be hashed using PBKDF2 with SHA-256. Cross-Site Request Forgery (CSRF) tokens must be validated on all POST/PUT requests. Rate limiting (django-ratelimit) must restrict brute-force login attempts to a maximum of 5 tries per IP within 5 minutes (django-axes).
* **Privacy: ** Personally Identifiable Information (PII) including phone numbers, government ID documents, and geolocations must be encrypted at rest. Users must be able to delete their account, executing cascading deletion of all personal profiles in compliance with GDPR guidelines.
* **Accessibility: ** All HTML user interface elements must conform to Web Content Accessibility Guidelines (WCAG) 2.1 Level AA, including contrast ratios of 4.5:1, semantic page structures, and keyboard navigation capability.
* **Compatibility: ** Must run seamlessly across different devices and operating systems. Supported browsers: Google Chrome (version 90+), Apple Safari (version 14+), Mozilla Firefox (version 88+), and Microsoft Edge (version 90+).
* **Localization: ** The system's primary interface language is English. Code structure must wrap all user-facing strings in translation hooks (Django ugettext) to support seamless future localization. UTC is used as the database timezone, converting to client local timezone in front-end views.
* **Portability: ** The system must run inside standard Docker containers to facilitate quick deployment to cloud service providers (Render, AWS, GCP, Heroku).
* **Logging: ** Every API transaction, authentication lifecycle event, error trace, email dispatch, and AI prompt request must be logged. AI calls are persisted in the AILog table; emails are logged in the EmailLog table. General application errors are written to rotating files on the server (max 10MB per file).
* **Monitoring: ** A public health check endpoint (/offline/ or /admin/status/) must return system status metrics. System monitoring tools (e.g. Sentry or Prometheus) must alert admins of elevated 5xx error responses within 60 seconds.
* **Backup: ** Daily automated backups of the SQLite file / PostgreSQL DB must be archived to secure cloud storage (e.g. AWS S3) with a retention policy of 30 days.
* **Disaster Recovery: ** In the event of database failure or server corruption, the Recovery Time Objective (RTO) must be less than 4 hours, and the Recovery Point Objective (RPO) must be less than 24 hours.
* **Fault Tolerance: ** If external services (Leaflet tiles, Gemini API, or SMTP server) fail, the core system must continue operating. Map pages must show warning banners, Gemini requests must fallback to local mock logic, and failed emails must queue for retry instead of throwing 500 errors to the client.
* **Compliance: ** The platform must adhere to local transport regulations regarding non-commercial carpooling (fares must only offset vehicle operating costs and not generate commercial profits).
* **Browser Support: ** Must test and verify layout alignment and Javascript responsiveness on Chrome, Safari, Firefox, and Edge desktop versions.
* **Mobile Support: ** Must support installable PWA manifest structures on Android (Chrome PWA launcher) and iOS (Add to Home Screen Safari shortcut) with responsive layouts adapting down to 320px viewport widths.

## 6. User Roles & Permissions Matrix

The system enforces rigid role-based access control (RBAC). The following matrix defines the exact actions permitted for each user category:

| Feature Area | Passenger | Driver | Administrator |
| --- | --- | --- | --- |
| Register & Profile Edit | Allowed | Allowed | Allowed |
| Register Vehicle | Denied | Allowed | Allowed |
| Publish Ride Offer | Denied | Allowed | Allowed |
| Search Ride Matches | Allowed | Allowed (as passenger) | Allowed |
| Create Booking Request | Allowed | Allowed (as passenger) | Allowed |
| Approve/Reject Booking | Denied | Allowed (own ride) | Allowed (all) |
| Trigger SOS Alarm | Allowed (during trip) | Allowed (during trip) | Allowed |
| Create Community | Allowed | Allowed | Allowed |
| Approve Community Member | Denied | Denied (unless admin) | Allowed (all) |
| Post in Community Feed | Allowed | Allowed | Allowed |
| Real-time Chat Rooms | Allowed (own rides/comms) | Allowed (own rides/comms) | Allowed (all) |
| Send Friend Request | Allowed | Allowed | Allowed |
| Submit Safety Report | Allowed | Allowed | Allowed |
| Use AI Chatbot / Planner | Allowed | Allowed | Allowed |
| Access System Logs | Denied | Denied | Allowed |
| Reset System Data | Denied | Denied | Allowed |
| Vetting ID Uploads | Denied | Denied | Allowed |

## 7. User Journey Maps

This section traces the chronological user journey maps across the lifecycle of the application interfaces:

* **Registration: ** 1. User lands on landing page. 2. Clicks 'Register'. 3. Fills registration fields. 4. Submits form. 5. System checks username uniqueness via AJAX. 6. DB stores inactive record. 7. Activation token generated and simulated. 8. Redirected to email verification page.
![Figure 7.1: User Registration Form View](file:///d:/Ride-Share/screenshots/registration_page.png)
*Figure 7.1: User Registration Form View*

* **Login: ** 1. User visits /login/. 2. Enters credentials or clicks single-click quick-access demo profile buttons (Admin, Passenger, Driver). 3. System checks PBKDF2 hash. 4. Records UserSession metadata. 5. Redirects to dashboard.
![Figure 7.2: User Authentication Form View](file:///d:/Ride-Share/screenshots/login_page.png)
*Figure 7.2: User Authentication Form View*

* **Forgot Password: ** 1. User clicks 'Forgot Password' on login page. 2. Enters registered email. 3. System saves PasswordResetToken (expires in 1 hour). 4. Simulates email dispatch. 5. User clicks link. 6. Enters new password on reset form. 7. Password hashes and updates in DB. 8. Session tokens expire.
* **Dashboard Access: ** 1. Logs in. 2. Role check executes. 3. Passenger dashboard displays active bookings, search bars, and community feeds. 4. Driver dashboard displays vehicle status, active ride offers, pending booking requests list, and trip stats. 5. Admin dashboard lists audit logs, safety reports, and AI usage summaries.
* **Feature Access (Ride Booking): ** 1. Passenger inputs source and destination. 2. Filters matches by distance detour. 3. Views recommendation scores. 4. Clicks 'Book Ride'. 5. Selects seat quantity. 6. Confirm Booking. 7. System forwards trip request to Driver. 8. Driver clicks 'Approve'. 9. Passenger status changes to accepted, prompting payment checkout page.
* **Notifications: ** 1. User receives instant popup or dashboard badge. 2. Navigates to notifications view. 3. Reviews list of request events. 4. Clicks 'Mark Read' or 'Mark All Read'. 5. DB updates is_read flag. 6. UI badge count resets.
* **Profile Management: ** 1. User navigates to /profile/. 2. Updates bio, skills, interests, and profile pictures. 3. If Driver, registers car model, capacity, and plate. 4. Submits organizational email. 5. User gets college/corporate verification token to verify domain affiliation. 6. Submits ID card scan for admin review.
* **Logout: ** 1. User clicks 'Logout' in header. 2. Django backend destroys session. 3. UserSession.is_active set to False. 4. Client clear session caches. 5. Redirected to landing page with connection status shown.
* **Account Deletion: ** 1. User selects 'Delete Account' in profile settings. 2. Confirms password verification challenge. 3. System performs cascade deletes of User, vehicles, bookings, friendships, and messages. 4. Logs out user. 5. Audits account removal.

## 8. Complete System Modules

The architecture is split into separate modules that govern specific operations within the Django MVC environment:

* **Authentication & Authorization Modules: ** Extends AbstractUser to custom User model. Handles registration form validation, email token checks, session token tracking, quick-login seeding, and Google OAuth bindings. Provides route protection decorators (@login_required, custom role verification middleware) to block unauthorized operations.
* **Dashboard Module: ** Serves three specialized HTML views: Passenger UI, Driver UI, and Admin UI. Coordinates metrics, listings, and workflows dynamically.
![Figure 8.1: Passenger Portal Dashboard Interface](file:///d:/Ride-Share/screenshots/passenger_dashboard.png)
*Figure 8.1: Passenger Portal Dashboard Interface*

![Figure 8.2: Driver Commute Portal Dashboard View](file:///d:/Ride-Share/screenshots/driver_dashboard.png)
*Figure 8.2: Driver Commute Portal Dashboard View*

![Figure 8.3: Administrator Analytics Dashboard View](file:///d:/Ride-Share/screenshots/admin_dashboard.png)
*Figure 8.3: Administrator Analytics Dashboard View*

* **Profile & Settings Module: ** Manages bio descriptions, skill tags, languages, travel rules (smoking, pets), and vehicle models using custom forms validated in backend core/forms.py.
![Figure 8.4: User Profile Customization and Validation Page](file:///d:/Ride-Share/screenshots/profile_page.png)
*Figure 8.4: User Profile Customization and Validation Page*

* **Search Module: ** Funnels pickup and dropoff coordinates to the geodetic route sequencer, returning compatible rides ranked by distance detour scores.
![Figure 8.5: Geodetic Waypoint Routing Matching Search Results](file:///d:/Ride-Share/screenshots/ride_search.png)
*Figure 8.5: Geodetic Waypoint Routing Matching Search Results*

* **Community Module: ** Manages user community circles, private group invites, approval loops, posts, comments, announcements, and feed likes.
![Figure 8.6: Community Circles Directory View](file:///d:/Ride-Share/screenshots/communities.png)
*Figure 8.6: Community Circles Directory View*

* **Notifications Module: ** Implements the Notification model. Dispatches real-time alerts upon booking approvals, friend request events, and community invitations.
![Figure 8.7: Notifications Alerts Center Console](file:///d:/Ride-Share/screenshots/notifications.png)
*Figure 8.7: Notifications Alerts Center Console*

* **Logging & Audit Module: ** Captures system actions. Persists all generative AI prompts/responses in AILog, and outgoing emails in EmailLog tables.
![Figure 8.8: Admin System Security & Session Log Registry](file:///d:/Ride-Share/screenshots/admin_system_logs.png)
*Figure 8.8: Admin System Security & Session Log Registry*


## 9. Use Cases

The core use cases detailing system workflows are defined below:

**Use Case ID: UC-01: Publish Route-Based Ride Offer** 

* **Actor: ** Driver
* **Description: ** Driver outlines their commute path on Leaflet, schedules the ride details, and publishes the offer to the matching pool.
* **Preconditions: ** Driver is authenticated, holds verified vehicle details in DB, and has active status.
* **Main Flow: ** 1. Driver navigates to 'Publish Ride'. 2. Driver selects their vehicle. 3. Map interface loads. 4. Driver enters Start and End locations. 5. Driver clicks on intermediate streets to pin waypoint coordinates. 6. Enters date, departure time, seats capacity, cost terms, luggage rules. 7. Submits form. 8. System validates inputs. 9. Saves Ride and RouteWaypoint models. 10. Redirects to dashboard with success message.
* **Alternative Flow (Empty Waypoints): ** At Step 5, if no intermediate waypoints are pinned, system calculates standard straight path sequence containing start and end coordinates as waypoints, then proceeds.
* **Exception Flow (Outdated Departure): ** At Step 6, if departure time is in the past, system throws validation error on form, highlighting time field, and prompts corrected entry.
* **Postconditions: ** Ride record created with status set to ACTIVE. Waypoint coordinates are sequenced in DB.
* **Business Rules: ** Fare charges cannot exceed maximum local cost-sharing guidelines. Vehicle capacity constraint must match registration.
* **Acceptance Criteria: ** Published ride is searchable by pickup/drop locations. Map displays route waypoints correctly in order.
**Use Case ID: UC-02: Search & Book Overlapping Route** 

* **Actor: ** Passenger
* **Description: ** Passenger enters pickup and drop points, runs geodetic proximity scan, views recommendation scoring, and requests seats booking.
* **Preconditions: ** Passenger is authenticated, has active status, and is not the driver of matching rides.
* **Main Flow: ** 1. Passenger navigates to 'Search Rides'. 2. Enters pickup address and dropoff address. 3. System geocodes addresses to coordinates. 4. Runs haversine distance matching query on active routes waypoints list. 5. Backend ranks matching rides based on detour walk distance and social trust affiliations. 6. Passenger reviews recommended ride card. 7. Clicks 'Book Ride'. 8. Enters seats count. 9. Confirms. 10. Booking created with status 'PENDING'. 11. Redirection logs confirmation.
* **Alternative Flow (No Direct Matches): ** At Step 5, if detour walk distance exceeds max limit (e.g. 5km), system reports 'No rides found', suggests increasing walk threshold or modifying search locations.
* **Exception Flow (Seats Exceeded): ** At Step 8, if seats requested exceeds available_seats on Ride, system raises error, block submission, and prompts user to reduce quantity.
* **Postconditions: ** Booking record is added. Notification model registers alert for Driver.
* **Business Rules: ** Passengers cannot book seats on expired rides. Maximum detour walking distance defaults to 5.0 km.
* **Acceptance Criteria: ** Matching calculations correctly identify route sequences (pickup waypoint index must be chronologically prior to dropoff waypoint index along driver route).
**Use Case ID: UC-03: Trigger SOS Emergency Alarm** 

* **Actor: ** Passenger or Driver
* **Description: ** Triggers local warning siren and updates database telemetry alerts for administrator escalation.
* **Preconditions: ** User is active driver or passenger on a ride with status 'ACTIVE'.
* **Main Flow: ** 1. User navigates to tracking page. 2. Clicks red 'SOS' button. 3. System prompts 'Confirm Emergency?'. 4. User clicks confirm. 5. Frontend JS triggers audible warning sound loop on client browser. 6. Transmits current GPS coordinate parameters. 7. Backend saves SOSAlert record. 8. Admin log shows flash red alarm. 9. Simulated emergency contact alert triggers.
* **Alternative Flow (No GPS Coordinates): ** At Step 6, if browser GPS permission is denied, system reads last known waypoint coordinates of ride record, saves alert, and proceeds.
* **Exception Flow (Expired Ride): ** At Step 1, if trip is already status 'COMPLETED', SOS button is disabled on UI, blocking trigger.
* **Postconditions: ** SOSAlert record is stored as is_active=True. Administrative alarms active.
* **Business Rules: ** SOS triggers must bypass ordinary API rate limiting constraints.
* **Acceptance Criteria: ** Siren audio plays locally. SOS logs are saved successfully in database. Admin dashboard displays emergency state immediately.
**Use Case ID: UC-04: Auto-Reply Support Ticket** 

* **Actor: ** Visitor / Customer
* **Description: ** Processes incoming customer emails, classifies issue types with Gemini AI, saves auto-reply draft, and flags escalations.
* **Preconditions: ** None (Accessible publicly on contact view).
* **Main Flow: ** 1. User visits contact page. 2. Fills Name, Email, Subject, and Message. 3. Clicks 'Submit Ticket'. 4. System creates SupportTicket record. 5. Backend forwards text parameters to reply_support_email function. 6. Gemini parses text, returning JSON classification structure. 7. System updates ticket category, records AI reply suggestions, sets needs_escalation flag. 8. Returns submission confirmation to user.
* **Alternative Flow (API Key Missing): ** At Step 5, if GEMINI_API_KEY is not defined, system triggers local regex filter, detects terms (like 'abuse', 'hack'), saves category, sets standard mock reply text, and completes.
* **Exception Flow (Corrupt JSON Payload): ** At Step 6, if Gemini returns invalid format, system logs JSON parse exception, sets category to 'General Inquiry', sets escalation to True (defaulting to safe review), and continues.
* **Postconditions: ** SupportTicket is added. EmailLog persists simulated auto-reply dispatch details.
* **Business Rules: ** Tickets marked with needs_escalation=True must appear at the top of the Admin support inbox queue.
* **Acceptance Criteria: ** Support tickets are generated with unique alphanumeric codes (RS-XXXXX). AI auto-reply drafts map to issue categories (e.g. Account Issue, abuse).

## 10. User Stories

The software development team must test and deliver against the following agile user stories:

**User Story US-001: Passenger Booking Search** 

* **Story: ** As a daily Passenger commuter, I want to search for rides by entering my pickup and drop addresses, so that I can find drivers who are already traveling on overlapping routes and avoid paying commercial taxi fares.
* **Acceptance Criteria 1: ** Search results must display matching rides where my pickup point is located before my dropoff point along the driver's route sequence.
* **Acceptance Criteria 2: ** Rides must display a detailed walkthrough of calculated walk distances and recommendation scores.
* **Acceptance Criteria 3: ** Inactive or full rides must be automatically filtered out of search listings.
**User Story US-002: Driver Waypoints Map Editor** 

* **Story: ** As a commuting Driver, I want to pins intermediate waypoints on a map when publishing my ride, so that passengers at intermediate locations along my journey can match and join my carpool.
* **Acceptance Criteria 1: ** The UI must load an interactive Leaflet.js map with geocoding searches to easily set start and end points.
* **Acceptance Criteria 2: ** Driver clicks on map must append sequential waypoint coordinate values to a hidden array form field.
* **Acceptance Criteria 3: ** The route line must visually update to show the waypoint sequence connection on the map canvas.
**User Story US-003: Safety Emergency SOS** 

* **Story: ** As a Passenger on a ride, I want to trigger a panic alarm with a single click in case of emergency, so that my driver is warned, local sirens alert bystanders, and safety admins log my exact coordinates for escalation.
* **Acceptance Criteria 1: ** The tracking dashboard must display a prominent, flashing Red 'SOS' button during active trips.
* **Acceptance Criteria 2: ** Clicking the button must play an audible warning siren loop on the device speaker immediately.
* **Acceptance Criteria 3: ** Backend must save the SOS alert with coordinates and set status to active within 50ms.
**User Story US-004: Trust Badges Vetting** 

* **Story: ** As a User concerned with safety, I want to verify my corporate or university email address, so that I can unlock organization trust badges and find safe ride matches from my own institution.
* **Acceptance Criteria 1: ** Profile page must offer domain email submission fields.
* **Acceptance Criteria 2: ** Entering a domain email triggers a verification token code sent to that address.
* **Acceptance Criteria 3: ** Entering the correct token updates profile variables, displaying verified trust badges next to username.

## 11. Workflows (ASCII Diagrams)

The operational sequence and activity workflows are diagrammed in ASCII formatting below:

**1. User Registration & Email Verification Lifecycle:** 

```

[User Client]                      [Django App Backend]                [Email Log/SMTP]
      |                                     |                                 |
      |--- 1. Submit Registration Form ---->|                                 |
      |    (User, Email, Password, Role)    |                                 |
      |                                     |--- 2. Hash Password (PBKDF2) -->|
      |                                     |--- 3. Create Inactive User ---->|
      |                                     |--- 4. Save Verification Token ->|
      |                                     |                                 |
      |<-- 5. Redirect to Verification -----|                                 |
      |                                     |--- 6. Dispatch simulated mail ->|
      |                                     |      (Contains Token link)      |
      |                                     |                                 |
      |--- 7. Click Token link (or input) ->|                                 |
      |                                     |--- 8. Validate Token expiry ----|
      |                                     |--- 9. Set is_email_verified=True|
      |<-- 10. Render Verified Profile -----|                                 |
        
```

**2. Ride Publishing, Waypoint Matching, and Booking Lifecycle:** 

```

[Driver Client]             [Maps API/OSRM]          [App Database]          [Passenger Client]
       |                           |                       |                          |
       |--- 1. Select Route ------>|                       |                          |
       |    (Pin Waypoints)        |                       |                          |
       |<-- 2. Draw Route Path ----|                       |                          |
       |                                                   |                          |
       |--- 3. Publish Ride (Time, Fare, Waypoints) ------>|                          |
       |                                                   |                          |
       |                                                   |--- 4. Search overlapping |
       |                                                   |      waypoints (pickup,  |
       |                                                   |      dropoff sequential) |
       |                                                   |                          |
       |                                                   |<-- 5. Match score list --|
       |                                                   |                          |
       |                                                   |<- 6. Submit Book request-|
       |<-- 7. Receive Pending Request Notification -------|                          |
       |                                                   |                          |
       |--- 8. Accept Booking Request -------------------->|                          |
       |                                                   |--- 9. Decrement seats ---|
       |                                                   |                          |
       |                                                   |<-- 10. Redirect checkout-|
       |                                                   |<-- 11. Simulate checkout-|
       |<-- 12. Trip Starts & Telemetry Tracks ------------|<-- 12. Trip Starts ------|
        
```

**3. SOS Panic Trigger Emergency Alert:** 

```

[User Tracking UI]               [Web API Client]               [Backend DB]           [Admin Panel]
        |                               |                            |                       |
        |--- 1. Clicks 'SOS Button' --->|                            |                       |
        |                               |--- 2. Get Geolocation ---->|                       |
        |--- 3. Siren sound loop (on) ->|                            |                       |
        |                               |--- 4. Dispatch Alert ----->|                       |
        |                               |      (Ride ID, Lat/Lng)    |                       |
        |                               |                            |--- 5. Save Alert ---->|
        |                               |                            |   (is_active=True)    |
        |                               |                            |                       |
        |                               |<-- 6. Trigger Admin alarm -|---------------------->|
        |                               |                            |                       | (Flash Red)
        |                               |<-- 7. Dispatch Contact list|                       |
        
```

**4. Automated Help Desk & Email Classifier (AI):** 

```

[Contact Page Visitor]           [Backend core]            [Gemini API Model]          [Admin Tickets]
         |                              |                           |                         |
         |--- 1. Submit Ticket ------->|                           |                         |
         |    (Name, Email, Message)    |                           |                         |
         |                              |--- 2. Forward contents -->|                         |
         |                              |      (Prompt Template)    |                         |
         |                              |                           |--- 3. Classify Category |
         |                              |                           |--- 4. Draft Auto-Reply  |
         |                              |                           |--- 5. Flag Escalation   |
         |                              |                           |                         |
         |                              |<-- 6. JSON payload -------|                         |
         |                              |                           |                         |
         |                              |--- 7. Save SupportTicket -|------------------------>|
         |<-- 8. Simulated Auto-Reply --|                           |                         | (Urgent Alert
                                                                                                 |  if escalated)
        
```

## 12. Database Design

**12.1 Entity Relationship Diagram (ASCII Layout):** 

```

  +------------------+                   +------------------+
  |       User       |1 ------------ N   |     Vehicle      |
  |------------------|                   |------------------|
  | PK: id           |                   | PK: id           |
  | username, role   |                   | FK: driver_id    |
  | reputation_points|                   | make, capacity   |
  +------------------+                   +------------------+
        |1        |1                              |1
        |         +---------------------+         |
        |                               v         v
        |                            +------------------+
        |                            |       Ride       |1 ----------+
        |                            |------------------|            |
        |                            | PK: id           |            |
        |                            | FK: driver_id    |            |
        |                            | FK: vehicle_id   |            |
        |                            | start_location   |            |
        |                            +------------------+            |
        |1                                 |1                        |N
        |                                  v                         v
        |                            +------------------+   +------------------+
        |                            |     Booking      |   |  RouteWaypoint   |
        |                            |------------------|   |------------------|
        |                            | PK: id           |   | PK: id           |
        |                            | FK: ride_id      |   | FK: ride_id      |
        +--------------------------->| FK: passenger_id |   | sequence_order   |
                                    | seats_requested  |   | latitude, name   |
                                    +------------------+   +------------------+
        
```

**12.2 Database Schema Tables:** The tables derived from django models.py are detailed below:

| Table Name | Columns (Field Name, Type, Constraints) | Indexes & Relations |
| --- | --- | --- |
| core_user | id (INT AUTO_INCREMENT PK), username (VARCHAR UNIQUE), password (VARCHAR), email (VARCHAR), role (VARCHAR), reputation_points (INT), is_email_verified (BOOL), phone_number (VARCHAR) | Index on username. Base user settings storage. |
| core_vehicle | id (INT PK), driver_id (INT FK ref core_user.id), make (VARCHAR), model (VARCHAR), license_plate (VARCHAR UNIQUE), capacity (INT), color (VARCHAR), verified (BOOL) | Index on license_plate. FK driver_id Cascade. |
| core_ride | id (INT PK), driver_id (INT FK ref core_user.id), vehicle_id (INT FK ref core_vehicle.id), start_location (VARCHAR), end_location (VARCHAR), departure_time (DATETIME), price_per_seat (DECIMAL), available_seats (INT), status (VARCHAR), route_map (TEXT) | Index on status. FK driver_id Cascade, FK vehicle_id Protect. |
| core_routewaypoint | id (INT PK), ride_id (INT FK ref core_ride.id), sequence_order (INT), name (VARCHAR), latitude (DECIMAL), longitude (DECIMAL), estimated_arrival (DATETIME) | Index on (ride_id, sequence_order) UNIQUE. Sequential route map coordinates storage. |
| core_booking | id (INT PK), ride_id (INT FK ref core_ride.id), passenger_id (INT FK ref core_user.id), pickup_location (VARCHAR), pickup_lat (DECIMAL), dropoff_location (VARCHAR), dropoff_lat (DECIMAL), seats_requested (INT), total_price (DECIMAL), status (VARCHAR) | FK ride_id Cascade, FK passenger_id Cascade. Booking transaction records. |
| core_community | id (INT PK), name (VARCHAR UNIQUE), description (TEXT), category (VARCHAR), community_type (VARCHAR), invite_link (VARCHAR UNIQUE), created_by_id (INT FK ref core_user.id) | Index on name. Circles list. |
| core_communitymember | id (INT PK), community_id (INT FK ref core_community.id), user_id (INT FK ref core_user.id), role (VARCHAR), status (VARCHAR) | Index on (community_id, user_id) UNIQUE. Handles circle authorization. |
| core_friendship | id (INT PK), user_id (INT FK ref core_user.id), friend_id (INT FK ref core_user.id), status (VARCHAR) | Index on (user_id, friend_id) UNIQUE. Direct friend maps. |
| core_message | id (INT PK), sender_id (INT FK ref core_user.id), recipient_id (INT FK ref core_user.id NULL), community_id (INT FK ref core_community.id NULL), ride_id (INT FK ref core_ride.id NULL), content (TEXT), file_attachment (VARCHAR), is_read (BOOL) | FK sender_id Cascade. Messaging room buffers. |
| core_notification | id (INT PK), recipient_id (INT FK ref core_user.id), sender_id (INT FK ref core_user.id NULL), notification_type (VARCHAR), content (TEXT), link (VARCHAR), is_read (BOOL) | FK recipient_id Cascade. Real-time alert triggers. |
| core_event | id (INT PK), title (VARCHAR), location (VARCHAR), date (DATETIME), event_type (VARCHAR), creator_id (INT FK ref core_user.id), community_id (INT FK ref core_community.id NULL) | FK creator_id Cascade. Event scheduling data. |
| core_eventattendee | id (INT PK), event_id (INT FK ref core_event.id), user_id (INT FK ref core_user.id), status (VARCHAR) | Index on (event_id, user_id) UNIQUE. Attending registries. |
| core_report | id (INT PK), reporter_id (INT FK ref core_user.id), reported_user_id (INT FK ref core_user.id NULL), reported_ride_id (INT FK ref core_ride.id NULL), reported_community_id (INT FK ref core_community.id NULL), reason (TEXT), status (VARCHAR) | FK reporter_id Cascade. Safety monitoring logs. |
| core_sosalert | id (INT PK), ride_id (INT FK ref core_ride.id), user_id (INT FK ref core_user.id), latitude (DECIMAL NULL), longitude (DECIMAL NULL), is_active (BOOL) | FK ride_id Cascade. Emergency tracking alarms. |
| core_rating | id (INT PK), reviewer_id (INT FK ref core_user.id), reviewee_id (INT FK ref core_user.id), ride_id (INT FK ref core_ride.id NULL), rating (INT), comment (TEXT) | Index on (reviewer_id, reviewee_id, ride_id) UNIQUE. User review ratings. |
| core_emaillog | id (INT PK), recipient (VARCHAR), subject (VARCHAR), content (TEXT), email_type (VARCHAR) | Read-only logs audit email simulations. |
| core_ailog | id (INT PK), prompt (TEXT), response (TEXT), log_type (VARCHAR) | Logs prompts/replies details of Gemini integrations. |
| core_emailverificationtoken | id (INT PK), user_id (INT FK ref core_user.id), token (VARCHAR UNIQUE), expires_at (DATETIME), is_used (BOOL) | FK user_id Cascade. Holds 24h validation strings. |
| core_passwordresettoken | id (INT PK), user_id (INT FK ref core_user.id), token (VARCHAR UNIQUE), expires_at (DATETIME), is_used (BOOL) | FK user_id Cascade. 1-hour reset tokens database. |
| core_communitypost | id (INT PK), community_id (INT FK ref core_community.id), author_id (INT FK ref core_user.id), content (TEXT), image (VARCHAR NULL), is_announcement (BOOL), likes_count (INT) | FK community_id Cascade. Feed wall database. |
| core_supportticket | id (INT PK), ticket_number (VARCHAR UNIQUE), name (VARCHAR), email (VARCHAR), subject (VARCHAR), message (TEXT), ai_suggested_reply (TEXT), admin_reply (TEXT), status (VARCHAR), assigned_to_id (INT FK ref core_user.id NULL) | Index on ticket_number. Help center tickets database. |

**12.3 Normalization Standard: ** The database design complies with Third Normal Form (3NF). Repeating groups (like waypoint coordinates) are isolated into the RouteWaypoint table. Transitive dependencies are removed by creating dedicated Vehicle and Booking tables, ensuring that a change in vehicle details does not introduce anomalies in active ride records.

## 13. API Documentation

This section details the primary backend API routes. All endpoints enforce CSRF checks in session requests and return JSON or HTML redirects as defined:

| Endpoint | Method | Auth | Body/Parameters | Status Code & Response |
| --- | --- | --- | --- | --- |
| /login/ | POST | None | username, password | 302 Redirect to /dashboard/ upon success; 400 Bad Request if fields invalid. |
| /register/ | POST | None | username, email, password, role, phone_number | 302 Redirect to verification page. Checks username uniqueness. |
| /api/check-username/ | GET | None | ?username=text | 200 OK. JSON: {'available': boolean} (uniqueness checker). |
| /ride/publish/ | POST | Driver Session | vehicle, start_location, end_location, departure_time, price_per_seat, available_seats, waypoints (JSON array string) | 302 Redirect to dashboard. RouteWaypoints populated, Ride status set to ACTIVE. |
| /ride/search/ | GET | Passenger Session | ?pickup_lat=decimal&pickup_lng=decimal&dropoff_lat=decimal&dropoff_lng=decimal&seats_needed=int | 200 OK HTML. Renders matched rides sorted by recommendation score (Detour + Trust). |
| /booking/create/<ride_id>/ | POST | Passenger Session | seats_requested, pickup_location, dropoff_location | 302 Redirect to payment simulation view. Booking status set to PENDING. |
| /booking/<booking_id>/action/ | POST | Driver Session | action ('accept' / 'reject') | 200 OK JSON: {'status': 'success'}. Modifies seats capacity, alerts passenger. |
| /safety/sos/ | POST | Session (Active Trip) | ride_id, latitude, longitude | 200 OK JSON: {'status': 'alert_logged'}. SOSAlert stored, triggers admin alerts. |
| /support/chatbot/ | POST | Session | question, history (text) | 200 OK JSON: {'answer': text}. Contacts Gemini API support Bot. |
| /api/admin/stats/ | GET | Admin Session | None | 200 OK JSON. Returns user roles counts, active rides, email volumes, AI log statistics. |

## 14. AI Module Specifications

**14.1 Purpose: ** To automate customer care, analyze message safety, categorize incoming service tickets, and compile travel itineraries for carpoolers using Generative AI models.

**14.2 Architecture: ** The Django core application communicates with the Google Gemini API using the google-generativeai SDK. If keys are missing, the ai_services.py module intercepts calls and provides high-fidelity simulated response fallbacks.

**14.3 Model: ** Gemini-1.5-flash is configured as the default model. Temperature settings vary: 0.2 for strict classifications (e.g. support emails, toxicity analyses), and 0.7 for creative text generations (travel itineraries).

**14.4 Prompt Flow: ** 1. User inputs text. 2. Backend formats request using prompt templates. 3. System checks toxicity. 4. Executes Gemini API call. 5. Logs request and response parameters in AILog table. 6. Validates format. 7. Renders to user.

![Figure 14.1: Helpdesk Automated Support Chatbot Session](file:///d:/Ride-Share/screenshots/ai_chatbot.png)
*Figure 14.1: Helpdesk Automated Support Chatbot Session*

![Figure 14.2: AI-Generated Travel Route Itinerary Assistant](file:///d:/Ride-Share/screenshots/ai_trip_planner.png)
*Figure 14.2: AI-Generated Travel Route Itinerary Assistant*

**14.5 Fallback, Safety, & Token Limits: ** A custom toxicity check flags harassment. If text contains scam words, is_toxic=True is saved, and content is blocked. Caching is simulated, and Google's free-tier rate limits (15 Requests Per Minute) are handled with a fallback mechanism that switches to local regex templates if limits are breached. Error handling logs API issues in standard Django files without throwing 500 errors to the client.

**14.6 Prompt Templates in Code:** The exact prompts defined in core/ai_services.py are:

```

# Template 1: AI Support Chatbot Context
Context: You are a helpful 24/7 Support Assistant for "Ride-Share", a real-time carpooling and community travel platform.
Chat History: {chat_history}
User Question: {user_question}
Answer the user's question clearly, concisely, and professionally. Explain the rules, platform features (like communities, SOS alarms, payment sharing), and support channels if they need user verification.

# Template 2: Support Ticket & Email Auto-Reply Classifier
Read the following support email:
Sender: {sender_email}
Subject: {subject}
Body: {content}
Perform intent detection, classify the request, and draft a professional reply.
Return ONLY a JSON object with the following keys:
1. "category": Choose from (Account Issue, Login Problem, Verification Issue, Travel Question, Report Abuse, Community Support, Payment Query, Feature Request).
2. "needs_escalation": boolean (True if it involves safety reports, billing fraud, or technical bugs).
3. "reply_content": Markdown text of your drafted reply to the user.
        
```

## 15. Email System

The platform requires robust automated emails to manage password security and account verification:

* **SMTP Configuration: ** Configured in settings.py using EMAIL_BACKEND. In production, connects to secure hosts (SendGrid, Mailgun) using SSL/TLS via port 465. In development, writes outputs directly to DB logs (EmailLog model) to prevent unsolicited spam transmissions.
* **Verification Flow: ** Upon registration, a 64-character token is saved (expires in 24 hours). The simulated verification link routes to /verify-email/?token=value. Entering the token changes User.is_email_verified to True.
* **Password Reset: ** Password recovery triggers PasswordResetToken creation (expires in 1 hour). The link routes to /reset-password/?token=value, verifying expiration before updating password hashes.
* **AI Auto-Reply Simulation: ** Admins can process incoming support emails. The system calls Gemini to classify details, draft responses, and queue them in EmailLog logs automatically.
* **Spam Protection: ** Rate limits email verification triggers to a maximum of 3 resends per hour per email address to defend against SMTP pool depletion.

## 16. Security Infrastructure

Security is built into the Django backend using secure defaults and custom rate-limit modules:

* **Authentication & Session Management: ** Standard sessions are maintained via signed cookies. Session identifiers are rotated upon login to defend against session fixation vulnerabilities. AJAX queries utilize CSRF token verification flags.
* **Authorization controls: ** Access checks are enforced at database and view layer. Routes verify ownership before executing edits (e.g. a driver cannot delete another driver's ride).
* **Password Hashing: ** Uses Django's default PBKDF2 algorithm with SHA-256 and 800,000 iterations to protect passwords in the database.
* **Injection Protections: ** Django's ORM parameters query building automatically protects database calls from SQL Injection. Front-end HTML templates use engine escaping constraints to protect against Cross-Site Scripting (XSS).
* **Rate Limiting: ** django-ratelimit handles rate limits on search queries. Login views utilize django-axes to lock profiles after 5 consecutive authentication failures from a single IP within 5 minutes.
* **Secrets Management: ** Secrets (Gemini API keys, database credentials, Django SECRET_KEY) are loaded from .env file configurations using python-decouple. Hardcoded credentials in source control are strictly prohibited.

## 17. UI/UX Design System

The front-end user experience emphasizes visual clarity, accessibility compliance, and mobile responsive controls:

* **Design Principles: ** Clean grid alignment, high typography hierarchies, visual icons cues (Bootstrap Icons), and clear interactive states.
![Figure 17.1: Desktop Landing/Home Page Canvas](file:///d:/Ride-Share/screenshots/home_page.png)
*Figure 17.1: Desktop Landing/Home Page Canvas*

* **Color System: ** Defined in static/css/style.css using CSS Custom Properties for seamless Light/Dark mode toggling. Primary brand color: Deep Navy Blue (#003366). Secondary accents: Soft Gray (#E0E0E0), Success state: Forest Green (#28A745), Warning alarm: Crimson Red (#DC3545).
* **Typography: ** Google Font 'Outfit' or 'Inter' is loaded as the primary font family. System fallbacks include sans-serif. Heading weights are bold (700); body paragraphs are regular (400).
* **Responsive Design: ** Adapts to desktop, tablet, and mobile displays using Bootstrap 5 fluid grid containers. Key CSS breakpoints: Mobile (<576px), Tablet (<768px), Desktop (>=992px).
![Figure 17.2: Mobile Responsive Passenger Dashboard Interface Layout (375x812 View)](file:///d:/Ride-Share/screenshots/mobile_dashboard.png)
*Figure 17.2: Mobile Responsive Passenger Dashboard Interface Layout (375x812 View)*

* **Micro-Animations & Visuals: ** Includes smooth hover transitions (0.2s ease-in-out) on dashboard cards and form submit buttons, alongside a pulsing animation on the active red SOS button.
![Figure 17.3: Custom 404 URL Not Found Error State](file:///d:/Ride-Share/screenshots/error_page.png)
*Figure 17.3: Custom 404 URL Not Found Error State*


## 18. External Integrations

The platform relies on several key external integrations to function:

| External Service | Purpose | Authentication | Limits & Quotas | Fallback Strategy |
| --- | --- | --- | --- | --- |
| Leaflet.js / OSM | Loads interactive maps and plots sequential waypoint route markers. | None (Free OpenStreetMap Tile layers). | Unlimited tile loading requests. | Displays warning banner; map reverts to standard inputs form fields. |
| Nominatim API | Geocodes address strings into GPS coordinates (latitude, longitude). | None (Relies on User Agent identifiers). | Max 1 request per second. | Displays address lookup errors; requests users coordinate inputs manually. |
| OSRM API | Calculates route distances and sequential waypoints routing paths. | None (Public routing endpoint). | Rate limits on shared servers. | Plots straight geodetic routes based on mathematical Haversine sequence. |
| Google Gemini API | Powers helpdesk support chatbot, support email classifiers, and travel itinerary builders. | Bearer API Key (GEMINI_API_KEY env). | 15 Requests Per Minute (RPM) on free tier. | Intercepts requests in ai_services.py, fallback to local regex drafts and mock templates. |
| SMTP Relay Gate | Dispatches password recovery and account verification notifications. | Credentials Login (Host, Port, User, Password). | Varies by provider (SendGrid free: 100/day). | Logs email body in DB (EmailLog) for manual operator recovery. |

## 19. Deployment Guide

Deployment environments and configuration requirements are defined as follows:

* **Environments: ** Development: Runs Django debug local server (127.0.0.1:8000), using SQLite database db.sqlite3. Production: Runs in Docker containers on Render, connected to PostgreSQL instances with debug turned off (DEBUG=False).
* **CI/CD Pipeline: ** GitHub Actions automatically execute on all push requests to main branch. The pipeline boots python venv, installs requirements.txt, runs migrations checks, executes unit test suites, and alerts of build failures.
* **Git Workflow: ** Follows standard GitFlow practices. Features are developed in separate feature/ branches and merged into master/main via verified pull requests.
* **Server Config (Render/Vercel): ** Renders configuration via render.yaml (packages ASGI daphne/gunicorn processes). Vercel handles static assets deployments via vercel.json configurations. SSL certs are auto-renewed via Let's Encrypt.
* **Environment Variables: ** The .env file must store SECRET_KEY, GEMINI_API_KEY, DB_URL, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD. Static files are collected using collectstatic and served via Whitenoise.

## 20. Testing & Verification

The quality assurance framework verifies that all functional and security requirements are met:

* **Unit Testing: ** Written in backend/core/tests.py using Django's TestCase. The suite covers: User creation, geodetic waypoint matching validations, booking status updates, vehicle capacity validations, and API logins.
* **Integration Testing: ** Verifies interactions between route matching and booking creations (e.g. Booking seat allocation updates active ride listings).
* **System & UAT Testing: ** Manual verification checklists run inside staging environments, simulating passengers booking rides, drivers reviewing lists, and clicking the red SOS panic alarm system.
* **Performance testing: ** Simulates up to 10,000 active routes in database seeding, verifying that page load times and search latencies remain within NFR targets.
* **Test Cases Checklist:** 
| Test ID | Description | Inputs | Expected Outcome |
| --- | --- | --- | --- |
| TC-001 | Verify new passenger account registration. | Username='testuser', Role='PASSENGER' | User record created, inactive state. Verification token saved in DB. |
| TC-002 | Check password recovery token validation. | Valid email address. | PasswordResetToken generated, expires in 1 hour. Email log recorded. |
| TC-003 | Intelligent Geodetic Sequential Matching Check. | Pickup coordinates matching active ride sequential waypoints. | Ride returned. Walk distance <= maximum walk distance. Ranks by recommendation score. |
| TC-004 | Prevent reverse sequence route bookings. | Pickup point located after dropoff point along driver route. | Route matching filters ride out of recommendation list (Pickup Index > Dropoff Index). |
| TC-005 | Trigger SOS Panic Alert. | Active trip user triggers SOS. | SOSAlert stored in DB as active. Siren audio element plays on client UI. |
| TC-006 | Check toxicity content filter. | Hate speech message text content. | AI filter flags toxicity. returns is_toxic=True, blocks message from feeds. |


## 21. Risks Assessment

Key operational, legal, and technical risks are defined below:

* **Technical: ** SQLite database concurrency bottlenecks. Mitigation: Migrate to PostgreSQL in production environments.
* **Business: ** Lack of driver liquidity or low passenger density. Mitigation: Target specific corporate campuses and colleges to establish high-density routes first.
* **Legal: ** Compliance liabilities with local commercial transport regulators. Mitigation: Set strict limits on seat pricing to ensure drivers only offset fuel costs without making profit.
* **Security: ** Threat of harassment or fake user accounts. Mitigation: Require government identity uploads and corporate/college email verification badges.
* **AI Risks: ** Gemini API rate limiting or hallucinations in FAQ support answers. Mitigation: Set temperature to 0.2, implement fallback mock answers, and allow ticket escalation for human review.
* **Deployment: ** Server hosting outages (Render/Vercel). Mitigation: Run redundant mirrors and host PWA service workers caching policies for offline-first dashboard accessibility.

## 22. Future Enhancements

The roadmap for releases after MVP 1.0 includes the following improvements:

* **1. Live GPS tracking: ** Integrate real-time geolocation tracking using HTML5 Geolocation API, WebSockets (Django Channels), and background device services.
* **2. Production Payment Gateway: ** Transition from simulated checkout to a live payment gateway integration (Stripe, Razorpay, or PayPal API).
* **3. Native Mobile Compilation: ** Package the PWA codebase into native Android and iOS wrappers using Capacitor or Apache Cordova frameworks to publish to official App Stores.
* **4. Multi-Modal Travel Matching: ** Expand recommendation engine to combine public transit data (bus, subway routes) with carpooling legs for long-distance commutes.

## 23. Maintenance Strategy

System maintenance procedures are defined to guarantee long-term operational health:

* **Bug Fixes & Patching: ** Urgent security patches (e.g. Django security updates) are deployed within 24 hours of release. Minor bugs are compiled into monthly release packages.
* **Updates: ** Dependencies in requirements.txt are reviewed quarterly. Minor and patch updates are automated using package managers (e.g. Dependabot).
* **Versioning: ** Strict adherence to Semantic Versioning (SemVer) guidelines: MAJOR.MINOR.PATCH. Pre-releases are tagged as -beta or -rc.
* **Incident Response: ** If a server crash or database outage occurs, automated pager alerts trigger. The on-call DevOps engineer initiates rollback scripts, verifies logs, and reports root-cause analyses (RCA) in support archives.

## 24. Project Timeline

The timeline spans a 24-week lifecycle from initial requirements gathering to final production release:

```

Phases & Weeks Tracker:
  W1-W4   : Planning & SRS Documentation [Completed]
  W5-W8   : Database Setup & Geodetic Logic Coding [Completed]
  W9-W14  : Frontend Integration, Map Editor & Chat Rooms [Completed]
  W15-W18 : AI Helper bots & Email Systems Integration [Completed]
  W19-W20 : QA Testing & Security Audits [In Progress]
  W21-W22 : Staging deploy, UAT Vetting [Upcoming]
  W23-W24 : Production Release & Post-deployment reviews [Upcoming]
        
```

| Milestone | Target Week | Deliverables | Status |
| --- | --- | --- | --- |
| M1: Specification Approval | Week 4 | Software Requirements Specification (SRS) Document. | Completed |
| M2: Backend Baseline | Week 8 | Django app models structure, database seeding, unit tests. | Completed |
| M3: UI Integration | Week 14 | Leaflet waypoint sequencing interface, responsive dashboard templates. | Completed |
| M4: System Completion | Week 18 | Gemini Support bots, simulated SMTP logs, chat uploads, offline cache. | Completed |
| M5: Production Release | Week 24 | Render hosting deploy, production DB migrations, security checks. | Upcoming |

## 25. Budget & Cost Breakdown

Project financial projections and operational billing costs are defined as follow:

* **Development Cost: ** === FILLED BY USER ===
* **Hosting Servers (Render/AWS): ** === FILLED BY USER ===
* **Database Cloud Instance: ** === FILLED BY USER ===
* **Domain Name Registration: ** === FILLED BY USER ===
* **Email Provider API (SendGrid): ** === FILLED BY USER ===
* **Google Gemini API Usage: ** === FILLED BY USER ===
* **Licensing Fees: ** === FILLED BY USER === (System utilizes free MIT/BSD open source libraries, resulting in ₹0 licensing fees).
* **Monthly Maintenance Billing: ** === FILLED BY USER ===

## 26. Legal & Compliance

To satisfy university standards, startup governance, or industrial deployments, the system must address regulatory requirements:

* **Privacy Policy: ** === FILLED BY USER ===. The policy must cover user data retention, coordinates logging histories, and ID vetting storage policies.
* **Terms of Service: ** === FILLED BY USER ===. Must declare that Ride-Share is a peer-to-peer cost-sharing platform and is not a commercial taxi aggregation network.
* **Cookie Policy: ** === FILLED BY USER ===. Session and CSRF cookies are strictly essential for core authentication operations; no marketing cookies are utilized.
* **GDPR Compliance: ** Allows users to execute 'Right to be Forgotten' commands in profile settings, executing cascading deletion of usernames, credentials, and location records from DB storage.
* **Applicable Jurisdiction Laws: ** === FILLED BY USER ===
* **Copyright Ownership: ** Copyright 2026 Ride-Share Development Team. All rights reserved. Intellectual property rights belong to === FILLED BY USER ===.

## 27. Appendices

**Glossary of terms: ** 1. Haversine: An equation giving great-circle distances between two pairs of coordinates on a sphere. 2. Leaflet.js: A lightweight, mobile-friendly Javascript mapping library. 3. SQLite: A lightweight serverless SQL database engine. 4. PWA: Progressive Web App capability installable on client OS layers.

**System Configuration Template (settings.py environment variables):** 

```

# .env File Configuration Blueprint
SECRET_KEY=django-insecure-mock-key-development-only
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*.render.com
DATABASE_URL=sqlite:///db.sqlite3
GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SendGridApiPasswordGoesHere
        
```

**Deployment Checklist: ** 1. Set DEBUG=False. 2. Collect static files (python manage.py collectstatic). 3. Run migrations checks. 4. Setup SSL/TLS Let's Encrypt certificates. 5. Populate environment keys in Render. 6. Verify Service Worker sw.js matches route patterns.

**Release Checklist: ** 1. Run full unit testing suites. 2. Verify PWA install icon sizes (192px/512px). 3. Verify clean seeding (python manage.py seed_demo). 4. Perform accessibility audit scans.

**Support Contact Directory: ** Technical lead: support@yourdomain.com. System Admin emergency helpline: === FILLED BY USER ===.

