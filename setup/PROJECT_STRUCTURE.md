# Project Structure

An overview of the folder hierarchy and core files comprising the Ride Share Smart Route-Based Ride Sharing Platform.

---

```text
Ride-Share/
├── assets/                     # Graphic design resources and banners (empty by default)
├── backend/                    # Core Django Project Directory
│   ├── config/                 # Base Django Configuration
│   │   ├── settings.py         # App databases, time zones, static definitions
│   │   ├── urls.py             # Root URL router mapping /sw.js and /admin/
│   │   ├── wsgi.py / asgi.py   # WSGI and ASGI server hooks
│   ├── core/                   # Main Django Business Logic App
│   │   ├── management/         # Seeding commands directory
│   │   │   └── commands/
│   │   │       └── seed_demo.py# Seed script for mock users and coordinate paths
│   │   ├── migrations/         # DB table version records
│   │   ├── admin.py            # Model configuration panels for Admin Dashboard
│   │   ├── forms.py            # Forms validation (profiles, vehicle details)
│   │   ├── models.py           # DB Schema (User, Vehicle, Ride, Waypoint, Booking)
│   │   ├── route_matching.py   # Haversine distance sequencer matching algorithm
│   │   ├── tests.py            # Automated Unit test cases
│   │   └── views.py            # Response controller views and simulators
│   ├── static/                 # Served Client-Side Assets
│   │   ├── css/
│   │   │   └── style.css       # Layouts, light/dark custom properties, micro-animations
│   │   ├── js/
│   │   │   └── app.js          # Service worker, connection banner, simulated SOS alarm
│   │   ├── images/
│   │   │   └── icons/          # PWA PNG launchers (192px and 512px)
│   │   └── manifest.json       # PWA Application Metadata
│   ├── templates/              # HTML layout engines
│   │   ├── base.html           # Master parent wrapper, CSS/JS links, PWA button
│   │   ├── landing.html        # Landing page with About, Features, Help FAQ
│   │   ├── login.html          # Standard login and demo auto-login buttons
│   │   ├── dashboard_*.html    # Role-based panels (Passenger, Driver, Admin)
│   │   ├── ride_*.html         # Details tracking map and publish map
│   │   ├── profile.html        # Profile fields and vehicle forms
│   │   ├── payment.html        # Simulated invoice checking page
│   │   ├── offline.html        # PWA network offline alert fallback
│   │   └── sw.js               # Service Worker script
│   ├── db.sqlite3              # Active SQLite database file
│   ├── manage.py               # Django CLI management entry point
│   ├── requirements.txt        # Backend dependencies
│   └── .env                    # Environment secrets
├── docs/                       # Project report outlines and presentations (.docx)
└── setup/                      # Setup instruction manuals
    ├── RUN_LOCALLY.md          # Local boot manual
    ├── PROJECT_STRUCTURE.md    # Repository layout description (This file)
    ├── DEPLOYMENT.md           # Production deployment procedures
    ├── GITHUB.md               # Git version commands
    ├── DOWNLOAD_AND_RUN.md     # Quick installation summary
    ├── PWA_INSTALL.md          # Installing as a PWA
    └── APK_GUIDE.md            # Bundling into Android APK
```

---

## Technical Component Details

### 1. Route Waypoint Matching (`core/route_matching.py`)
Encapsulates a custom python script using the Haversine formula to compute great-circle distance. It maps and checks if a driver's active route sequence matches the passenger's pickup and drop coordinates in order, sorting recommendations by distance proximity detour scores.

### 2. Service Worker (`templates/sw.js`)
Lives at the root template directory to gain root-scope authorization, managing cached style stylesheets, maps assets, and routing navigate prompts to `offline.html` if the host drops internet connection.

### 3. PWA Icons (`static/images/icons/`)
Self-contained high-resolution mock icons drawn programmatically with Pillow, supporting full install capability compliance on chromium-based modern browsers.
