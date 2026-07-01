# Running Ride Share Locally

This guide explains how to set up and run the Ride Share Smart Route-Based Ride Sharing Platform on your local computer from scratch.

---

## Prerequisites

Ensure you have **Python 3.10 or later** installed on your system. You can verify this by running:
```bash
python --version
```

---

## Installation & Setup Steps

### 1. Navigate to the Backend Directory
Open your terminal/command prompt and change directory to the `backend` folder:
```bash
cd backend
```

### 2. Set Up a Python Virtual Environment
Creating a virtual environment ensures dependencies do not conflict with global Python installations.
- **On Windows (cmd/PowerShell):**
  ```powershell
  python -m venv venv
  ```
- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  ```

### 3. Activate the Virtual Environment
- **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **On Windows (Command Prompt):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
Once activated, you will see `(venv)` prepended to your command prompt line.

### 4. Install Dependencies
Install all required libraries specified in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Generate and Apply Database Migrations
Initialize the SQLite database schema by generating and running migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed Demo Data & Accounts
This project includes a seeding command that automatically configures demo accounts, driver vehicles, and mock rides for demonstration purposes. Run:
```bash
python manage.py seed_demo
```
This sets up the following accounts:
- **Admin**: `admin` / `admin123`
- **Driver**: `driver` / `driver123`
- **Passenger**: `passenger` / `pass123`

### 7. Run the Development Server
Start Django's built-in local development server:
```bash
python manage.py runserver
```
You can now access the application by opening your web browser and navigating to:
**[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## Troubleshooting Common Errors

### 1. Execution Policy Restrict (PowerShell Windows)
If you get a script execution policy restriction warning when activating the virtual environment in Windows PowerShell:
- **Fix:** Run this command in PowerShell to lift restrictions for the current session:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
  ```

### 2. Pillow Installation Fails (C++ Compiler Error)
Pillow requires a compiler if a binary wheel is unavailable for your specific OS/Python combination.
- **Fix:** Update pip first: `python -m pip install --upgrade pip` and retry.

### 3. Port Already in Use
If port 8000 is occupied by another process:
- **Fix:** Run the server on a different port:
  ```bash
  python manage.py runserver 8080
  ```
