# Software Requirement Specifications (SRS)

**Project Name:** AI-Based Smart Route Ride-Sharing System  
**Product Version:** MVP 1.0 (Production-Inspired)

---

## 1. System Scope & Boundaries
The Ride Share system is a web-based Progressive Web Application (PWA) facilitating path-sequence carpooling matches. It manages user logins, vehicle listings, ride offers with sequential stops, geodetic route matching queries, and simulated payments/notifications.

```text
+--------------------------------------------------------------+
|                    Ride Share MVP Boundary                   |
|                                                              |
|   +------------+         +------------------+                |
|   | Driver UI  | <-----> |   Django 6 MVC   | <--> [Maps API]|
|   +------------+         |  (Route Match)   |                |
|                          +------------------+                |
|   +------------+                  ^                          |
|   |Passenger UI| <----------------|                          |
|   +------------+                  v                          |
|                          +------------------+                |
|                          |  SQLite Database |                |
|                          +------------------+                |
+--------------------------------------------------------------+
```

---

## 2. Key Use Cases

1. **UC-1: Register Vehicle:** Driver enters car model, plate number, and seating capacity.
2. **UC-2: Publish Ride:** Driver selects route waypoints on map, enters date/time, and submits offer.
3. **UC-3: Find Ride Match:** Passenger inputs starting and ending addresses and finds compatible driver paths.
4. **UC-4: Request Booking:** Passenger selects ride, goes through simulated checkout, and submits request.
5. **UC-5: Approve Booking:** Driver reviews incoming passenger requests and approves or rejects them.
6. **UC-6: Update Trip Status:** Driver starts and completes trips, changing ride state.
7. **UC-7: Trigger SOS:** User alerts local emergency services (simulated siren and logs).
