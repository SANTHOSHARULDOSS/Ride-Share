import os
import shutil
import glob

artifact_dir = r"C:\Users\santhosh\AppData\Local\Programs\Python\Python313\..\..\..\..\..\.gemini\antigravity-ide\brain\1bb55488-c82f-4f36-93b6-d48402c2b641"
# Fallback search if path is different (we can expand it)
if not os.path.exists(artifact_dir):
    # Search locally under AppData
    appdata = os.getenv("APPDATA")
    # C:\Users\santhosh\AppData\Roaming -> go to Local\.gemini
    local_gemini = os.path.join(os.path.dirname(appdata), "Local", ".gemini", "antigravity-ide", "brain", "1bb55488-c82f-4f36-93b6-d48402c2b641")
    if os.path.exists(local_gemini):
        artifact_dir = local_gemini

dest_dir = r"d:\Ride-Share\screenshots"
os.makedirs(dest_dir, exist_ok=True)

mappings = {
    "home_page*.png": "home_page.png",
    "login_page*.png": "login_page.png",
    "registration_page*.png": "registration_page.png",
    "passenger_dashboard*.png": "passenger_dashboard.png",
    "profile_page*.png": "profile_page.png",
    "ride_search*.png": "ride_search.png",
    "communities*.png": "communities.png",
    "notifications*.png": "notifications.png",
    "ai_chatbot*.png": "ai_chatbot.png",
    "ai_trip_planner*.png": "ai_trip_planner.png",
    "driver_dashboard*.png": "driver_dashboard.png",
    "admin_dashboard*.png": "admin_dashboard.png",
    "admin_system_logs*.png": "admin_system_logs.png",
    "error_page*.png": "error_page.png",
    "mobile_dashboard*.png": "mobile_dashboard.png"
}

print(f"Searching in: {artifact_dir}")
for pattern, target in mappings.items():
    search_path = os.path.join(artifact_dir, pattern)
    matches = glob.glob(search_path)
    if matches:
        # Get the latest one if multiple
        latest_match = max(matches, key=os.path.getmtime)
        dest_path = os.path.join(dest_dir, target)
        shutil.copy2(latest_match, dest_path)
        print(f"Copied {os.path.basename(latest_match)} -> {target}")
    else:
        print(f"No match for pattern: {pattern}")

print("Done copying screenshots!")
