# System Design Document

This document outlines the software design, system architectures, data flows, and module decompositions.

---

## 1. Modular Decomposition

The project uses a structured model-view-controller (MVC) architecture matching Django's standard layout.

```text
+--------------------------------------------------------------------------+
|                                  Django MVC                              |
|                                                                          |
|   [ Browser / PWA ] <=======> [ URLs Router ] <=====> [ Views / Forms ]  |
|                                                               ^          |
|                                                               |          |
|                                                               v          |
|   [ SQLite DB ]     <=======> [ Models Layer ] <=====> [ Match Algorithm]|
+--------------------------------------------------------------------------+
```

### 1.1 Components Layer Description
* **Models Layer (`core/models.py`):** Translates relational SQL records into Python entities.
* **Controller Views (`core/views.py`):** Handles session logins, templates logic, and database state transitions.
* **Form Layer (`core/forms.py`):** Performs data sanitization, verifying licensing formats and seat thresholds.
* **Route Matching Helper (`core/route_matching.py`):** Standalone engine performing geodetic calculations.
* **Service Worker (`templates/sw.js`):** Intercepts client-side HTTP calls to serve cached HTML/CSS/JS offline.
