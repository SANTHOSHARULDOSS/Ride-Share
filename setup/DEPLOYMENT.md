# Production Deployment Guide

Instructions for deploying the Ride Share Smart Route-Based Ride Sharing Platform on free cloud services like **Render**, **Railway**, **Fly.io**, or **PythonAnywhere**.

---

## 1. Preparing the Project for Deployment

Before deploying, ensure the following configurations are updated:

### Enable WhiteNoise for Static Files
For platforms like Render or Railway, Django needs to serve static assets efficiently without a dedicated Nginx server. We use **WhiteNoise**:
1. Install it (it's standard, but ensure it's in environment):
   ```bash
   pip install whitenoise
   ```
2. In `backend/config/settings.py`, add WhiteNoise to the top of `MIDDLEWARE` (immediately under `SecurityMiddleware`):
   ```python
   MIDDLEWARE = [
       'django.middleware.security.SecurityMiddleware',
       'whitenoise.middleware.WhiteNoiseMiddleware', # Add this line
       ...
   ]
```
3. Enable compression and caching at the bottom of `settings.py`:
   ```python
   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
   ```

### Configure Allowed Hosts & Production Env
1. In `backend/config/settings.py`:
   ```python
   ALLOWED_HOSTS = ['*']  # Update with your custom URL or use env variables
   ```
2. Ensure you have a dynamic configuration for production database engines. This project is configured to use standard SQLite which is ideal for MVP demonstrations. However, a persistent PostgreSQL adapter can easily replace this in the `DATABASES` settings dict if needed.

---

## 2. Deploying on Render (Recommended)

Render offers quick, free web service hosting from GitHub repositories:

1. **Create a Render Account:** Sign up at [render.com](https://render.com/).
2. **New Web Service:** Create a new Web Service and link your GitHub repository.
3. **Configure Service Details:**
   - **Name:** `ride-share-mvp`
   - **Environment:** `Python`
   - **Region:** Choose closest region.
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_demo
     ```
   - **Start Command:**
     ```bash
     gunicorn config.wsgi:application
     ```
4. **Environment Variables:**
   Under the "Environment" tab in Render, add:
   - `SECRET_KEY` = `your-custom-production-secret-key-here`
   - `DEBUG` = `False`
5. **Deploy:** Click **Create Web Service**.

> [!WARNING]
> Render's free tier filesystems are ephemeral. If your container restarts, the local SQLite database (`db.sqlite3`) resets. For production persistence, attach a Render Persistent Disk (e.g. at mount path `/data`) and update your `DATABASES` setting path to point inside `/data/db.sqlite3`.

---

## 3. Deploying on PythonAnywhere

PythonAnywhere is optimized specifically for Python WSGI hosting:

1. **Sign Up:** Go to [pythonanywhere.com](https://www.pythonanywhere.com/) and register.
2. **Upload Files:** Upload your project ZIP or clone it from GitHub in a console:
   ```bash
   git clone https://github.com/yourusername/Ride-Share.git
   ```
3. **Setup Virtualenv:** Open a bash console and run:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 rideshare-venv
   pip install -r requirements.txt
   ```
4. **Configure Web Tab:**
   - Create a new Web App with Manual Configuration.
   - Set the Virtualenv path to: `/home/yourusername/.virtualenvs/rideshare-venv`
   - Configure WSGI file: Edit the WSGI file to load the Django project module:
     ```python
     import os
     import sys
     path = '/home/yourusername/Ride-Share/backend'
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODEL'] = 'config.settings'
     os.environ['SECRET_KEY'] = 'some_secret'
     os.environ['DEBUG'] = 'False'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
5. **Collect Static Files:**
   Run `python manage.py collectstatic` and link the static files URL `/static/` to `/home/yourusername/Ride-Share/backend/staticfiles` in PythonAnywhere's static files section.

---

## 4. Deploying on Railway or Fly.io

Both platforms deploy using Dockerfiles or automatic buildpacks:
- Initialize configuration using `railway init` or `fly launch`.
- Specify port `8000` inside your startup configuration environment.
- Pass environment values for `SECRET_KEY` and `DEBUG`.
