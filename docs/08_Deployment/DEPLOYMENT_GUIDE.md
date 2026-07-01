# Production Deployment Configuration

Guidelines for deploying the application to cloud environments.

---

## 1. Static Asset Optimization (WhiteNoise)

Django does not serve static files efficiently in production. The project is pre-configured to use **WhiteNoise** to compress and cache assets:

* Middleware added to `settings.py` directly under `SecurityMiddleware`.
* Storage engine configured to compress:
  `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`

---

## 2. Serverless & Render Ephemeral DB Caveats

### SQLite Database Storage
* Because platforms like Render use ephemeral filesystems, the local SQLite database resets on container restarts.
* The application handles this in `settings.py` by checking for the persistent directory `/data` (Render disk mount). If it exists, the database is saved at `/data/db.sqlite3`.

### Vercel Serverless Architecture
* The `vercel.json` file routes requests through `@vercel/python`.
* For persistent storage on Vercel, link the application to a cloud Postgres instance (like Neon.tech) in `settings.py`.
