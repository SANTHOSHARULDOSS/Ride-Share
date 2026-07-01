# Ride Share - Smart Route-Based Ride Sharing Platform MVP

Ride Share is a Progressive Web Application (PWA) MVP built using Django 6, SQLite, Bootstrap 5, and Leaflet.js. Designed as an academic showcase prototype, it demonstrates software engineering principles, clean architecture, geodetic route waypoint matching, simulated payment flows, and offline-first capabilities.

[![Deploy to Render](https://render.com/images/deploy-to-render.svg)](https://render.com/deploy?repo=https://github.com/SANTHOSHARULDOSS/Ride-Share)

---

## Key Features

1. **Intelligent Waypoint Route Matching:** Custom mathematical matching engine built using the Haversine formula. Filters active rides and searches sequential waypoint indexes to guarantee optimal matches without expensive API charges.
2. **Progressive Web App (PWA):** Fully installable on Windows, macOS, Linux, and Android. Includes manifest metadata, service worker assets pre-caching, and automatic redirection to an offline dashboard.
3. **Interactive Route Editor:** Built using Leaflet.js and OpenStreetMap. Drivers can sequence routes visually on the map.
4. **Mock Tracking & SOS Alerts:** Simulated vehicle movement tracking and telemetry displays alongside a sounding SOS alarm panic system.
5. **Quick-Access Demo Accounts:** Single-click login portals for Administrator, Driver, and Passenger profiles.
6. **Robust Seeding:** A custom CLI database seeder (`python manage.py seed_demo`) that prepares the SQLite database instantly.

---

## Technology Stack

- **Backend:** Python, Django 6.0 (SQLite Database Engine)
- **Frontend:** HTML5, Vanilla CSS3, Bootstrap 5, JavaScript (ES6)
- **Maps API:** Leaflet.js (OpenStreetMap Tiles, Nominatim geocoder, OSRM router)
- **Offline PWA:** Service Workers cache policies

---

## Quick Start (Running Locally)

To set up and run the web application locally:

1. Open your terminal and navigate inside the backend folder:
   ```bash
   cd backend
   ```
2. Set up and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations and seed data:
   ```bash
   python manage.py migrate
   python manage.py seed_demo
   ```
5. Run development server:
   ```bash
   python manage.py runserver
   ```
   Access the local site at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**.

---

## Detailed Manuals Directory

Refer to the documents inside the `setup/` folder for comprehensive configurations:
- [Local Launch Details](file:///d:/Ride-Share/setup/RUN_LOCALLY.md)
- [Folder and File Structure Layout](file:///d:/Ride-Share/setup/PROJECT_STRUCTURE.md)
- [Production Cloud Deployment](file:///d:/Ride-Share/setup/DEPLOYMENT.md)
- [Git & GitHub Commands Guide](file:///d:/Ride-Share/setup/GITHUB.md)
- [Evaluator Download & Launch Summary](file:///d:/Ride-Share/setup/DOWNLOAD_AND_RUN.md)
- [PWA Desktop & Mobile Installation](file:///d:/Ride-Share/setup/PWA_INSTALL.md)
- [Bundling PWA into Android APK](file:///d:/Ride-Share/setup/APK_GUIDE.md)
