# Converting PWA to Android APK Guide

This guide explains how to convert the Ride Share Progressive Web App (PWA) into a downloadable Android Application Package (APK) that can be installed on Android devices or published to the Google Play Store.

---

## Technical Concept: Trusted Web Activity (TWA)

Converting a PWA to an APK is achieved using **Trusted Web Activity (TWA)**, a Google Play-compliant mechanism that runs your PWA inside a secure Chrome custom container without browser search bars. It requires your PWA to score high on lighthouse audits (have a valid manifest, HTTPS, and service worker).

---

## Method 1: Using PWABuilder (Simplest Method)

[PWABuilder](https://www.pwabuilder.com/) is a free tool maintained by Microsoft that automates PWA-to-APK packaging:

1. **Deploy your PWA:** Securely deploy your Ride Share application to a public HTTPS domain (e.g. Render, Railway, or Vercel).
2. **Enter URL:** Go to [pwabuilder.com](https://www.pwabuilder.com/), paste your deployed PWA URL, and click **Start**.
3. **Audit Check:** PWABuilder audits your PWA manifest, service worker, and security. Correct any issues reported.
4. **Generate Package:** Click **Generate APK / Package**.
5. **Configure Android Options:**
   - **Package ID:** e.g., `com.rideshare.mvp`
   - **App Name:** `Ride Share`
   - **Launcher theme colors:** Set to match your CSS colors.
6. **Download:** Download the generated zip file. Inside, you will find:
   - `app-release-unsigned.apk` or signed testing APK.
   - Assetlinks files (required for digital asset links signature verification).

---

## Method 2: Using Bubblewrap CLI (Advanced Command Line)

Bubblewrap is a command-line tool built by Google to package and sign TWAs locally using Node.js:

### 1. Prerequisites
Ensure you have the following installed on your machine:
- Node.js (v14+)
- Java Development Kit (JDK 11+)
- Android SDK

### 2. Install Bubblewrap CLI
Install the tool globally using npm:
```bash
npm install -g @bubblewrap/cli
```

### 3. Initialize the Project
Initialize Bubblewrap by pointing it to your deployed PWA's manifest:
```bash
bubblewrap init --manifest=https://your-deployed-domain.com/static/manifest.json
```
Bubblewrap will download the manifest and prompt you to configure Java paths and Android package values.

### 4. Build the APK
Generate the signed release APK by running:
```bash
bubblewrap build
```
This compile process generates:
- `app-release-signed.apk` (ready for installation).
- `assetlinks.json` file.

---

## 3. Verifying Digital Asset Links (Critical Step)

For the APK to launch without showing the Chrome browser address URL bar, you must establish trust between your web domain and the APK:

1. Copy the generated `assetlinks.json` file.
2. Upload it to your Django server so it is served at:
   `https://your-deployed-domain.com/.well-known/assetlinks.json`
3. Ensure the content type header is served as `application/json`.
4. Once verified by Android, the APK will launch in full-screen native mobile application appearance.
