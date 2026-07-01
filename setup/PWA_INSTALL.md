# PWA Installation Manual

This guide explains how to install the Ride Share Progressive Web App (PWA) on various operating systems. Once installed, it behaves like a lightweight native app, launching in a dedicated window without browser frames, and adding launcher icons to the home screen or app dock.

---

## 1. Prerequisites for Installation

Ensure you are accessing the application using a compatible browser:
- **Windows / macOS / Linux:** Google Chrome, Microsoft Edge, or Brave.
- **Android:** Google Chrome, Microsoft Edge, or Samsung Internet.
- **iOS (iPhone/iPad):** Safari.

---

## 2. Installation on Windows, macOS & Linux

When running the project locally or accessing a hosted web domain:

1. Open your browser and navigate to the application URL (e.g. `http://127.0.0.1:8000/`).
2. **Built-in Prompt Button:** Click the **Install App** button that automatically appears in the top navigation bar.
3. **Browser Address Bar Prompt:** Alternatively, look at the right end of the browser address bar. You will see an **Install Icon** (a monitor with a downward arrow).
4. Click the icon and confirm by clicking **Install** in the popup dialog.
5. The application will launch in its own standalone window, and a shortcut will be created on your Desktop and Start Menu/Dock.

---

## 3. Installation on Android (Mobile)

1. Open **Google Chrome** on your Android device and navigate to your application URL.
2. Wait a few seconds for the page to load. A banner saying **Add Ride Share to Home screen** will slide up from the bottom of the screen.
3. Tap the banner and confirm **Install**.
4. If the banner does not appear:
   - Tap the three dots (Menu Icon) in the top-right corner of Chrome.
   - Tap **Install app** (or **Add to Home screen**).
   - Confirm by tapping **Add / Install**.
5. You can now launch it from your app drawer.

---

## 4. Installation on iOS (iPhone/iPad)

Safari does not support automatic install prompts, but allows manual installation:

1. Open **Safari** on your iOS device and go to the application URL.
2. Tap the **Share** button (the square icon with an upward-pointing arrow) at the bottom toolbar.
3. Scroll down the sharing menu and tap **Add to Home Screen**.
4. Edit the name if desired (e.g. "RideShare") and tap **Add** in the top-right corner.
5. The icon will appear on your device's home screen.

---

## 5. Offline Capabilities once Installed

Once installed, the PWA utilizes the registered service worker (`sw.js`) to cache the design stylesheets, Leaflet map dependencies, and mock data templates. If you open the application offline:
- The app will not show browser "No Internet" Dino pages.
- It will load the UI cache and display the custom connection banner notifying you that the system has transitioned to **Local Offline Demo Mode**.
