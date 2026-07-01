# Download & Run Instantly

A simplified guide for examiners, instructors, and evaluators to download and launch the Ride Share MVP project immediately.

---

## 1. Get the Codebase

### Option A: Download GitHub ZIP
1. Go to the project repository link on GitHub.
2. Click the green **Code** button and select **Download ZIP**.
3. Extract the downloaded `.zip` file on your system.

### Option B: Clone via Git
Run the following clone command in your terminal:
```bash
git clone https://github.com/yourusername/Ride-Share.git
```

---

## 2. Fast Launch Instructions (Windows / macOS / Linux)

Open your terminal, navigate inside the project directory, and run the following command sequence:

### Step 1: Open project directory
```bash
cd Ride-Share/backend
```

### Step 2: Set up virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Apply database structures & seed data
```bash
python manage.py migrate
python manage.py seed_demo
```

### Step 5: Start local server
```bash
python manage.py runserver
```

---

## 3. Log In to Demonstration Accounts

Open **[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)** in your web browser. 

You can use the **Quick Demo Login Buttons** at the bottom of the screen to sign in automatically, or enter the credentials manually:

| Account Role | Username | Password | Actions Available |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Control panel metrics, database reset & seeding, admin panel access |
| **Driver** | `driver` | `driver123` | Vehicle configuration, publish rides with waypoints, accept/reject requests, start/complete rides |
| **Passenger** | `passenger` | `pass123` | Search rides with geolocated matching, request bookings, simulated payments checkout |

---

## 4. Key Review Checkpoints

1. **Intelligent Waypoint Matching:** Search for rides between Delhi landmarks (e.g. Connaught Place to Airport). The system sorts matches by walk detours.
2. **PWA Installation:** If using Chrome, click the "Install App" button in the navbar to install it as a desktop application.
3. **Offline Demo Mode:** Disconnect your internet connection. Search autocomplete and map queries will transition to pre-loaded local coordinate databases.
4. **Live Movement Simulation:** Go to Ride details page (as Driver or Passenger) and click **Simulate Ride** to animate the driver car marker along the route.
5. **SOS alarm:** Click the **SOS Emergency** button on the active ride details page to trigger simulated audio warning sirens.
