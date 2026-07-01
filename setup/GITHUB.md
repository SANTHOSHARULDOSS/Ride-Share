# GitHub Version Control Manual

This document details how to version control the Ride Share project, initialize Git, commit code changes, create a repository on GitHub, push updates, and clone files onto another system.

---

## 1. Initialize Git in Workspace

If Git is not yet configured in your local workspace:

1. Open a terminal in the root workspace folder:
   ```bash
   cd Ride-Share
   ```
2. Initialize repository:
   ```bash
   git init
   ```
3. Set your username and email (if not done globally):
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

---

## 2. Commit Files

Save your current changes to the local repository history:

1. Stage all files (respecting the `.gitignore` exclusions):
   ```bash
   git add .
   ```
2. Inspect what files are staged for commit:
   ```bash
   git status
   ```
3. Record changes with a clear message:
   ```bash
   git commit -m "Initialize Ride Share Smart Route Matching MVP with PWA support"
   ```

---

## 3. Create a Remote GitHub Repository

1. Go to [github.com](https://github.com/) and log in.
2. Click **New** under repositories.
3. Name your repository: `Ride-Share`
4. Set description: `Smart Route Based Ride Sharing Platform MVP`
5. Keep it public (or private, based on preference) and **do not** select Add README, .gitignore or license (since these are already in your workspace).
6. Click **Create repository**.

---

## 4. Link Local Repository and Push to GitHub

Link your local project history to the remote repository on GitHub:

1. Rename the default branch to main:
   ```bash
   git branch -M main
   ```
2. Add remote URL (replace username with your actual GitHub username):
   ```bash
   git remote add origin https://github.com/yourusername/Ride-Share.git
   ```
3. Upload your main branch to GitHub:
   ```bash
   git push -u origin main
   ```

---

## 5. Daily Git Workflow

### Push Local Edits
When you modify components:
```bash
git add .
git commit -m "Describe what feature changed"
git push origin main
```

### Pull Remote Edits
If you edit files on GitHub directly, or work from another machine, pull updates first:
```bash
git pull origin main
```

---

## 6. Clone Repository
To clone the repository onto another machine:
```bash
git clone https://github.com/yourusername/Ride-Share.git
cd Ride-Share
```
Follow the local setup instructions in [RUN_LOCALLY.md](file:///d:/Ride-Share/setup/RUN_LOCALLY.md) to launch the project.
