# Practical 17: GitHub Project Deployment
## Step-by-step guide to deploying the Doctor Finder project to GitHub

This guide walks you through every step needed to push the **Doctor Finder**
Django project to GitHub for version control and collaboration.

---

## Prerequisites

- Git installed on your computer (`git --version` to verify)
- A GitHub account at https://github.com
- Your Doctor Finder project folder ready

---

## Step 1: Initialize a Git Repository

Open a terminal inside the `doctor_finder/` project root and run:

```bash
git init
```

This creates a hidden `.git/` directory that tracks all changes.

---

## Step 2: Verify the .gitignore File

A `.gitignore` is already included in this project. It prevents sensitive and
unnecessary files from being uploaded to GitHub. Confirm it contains:

```
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
db.sqlite3
media/
staticfiles/
.env
*.log
*.sqlite3
.DS_Store
```

---

## Step 3: Add All Project Files to Staging

```bash
git add .
```

Check what will be committed:

```bash
git status
```

---

## Step 4: Make the First Commit

```bash
git commit -m "Initial commit: Doctor Finder Django project"
```

---

## Step 5: Create a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `doctor-finder`
3. Description: `Django Doctor Finder Project - Module 16`
4. Visibility: **Public** (or Private)
5. **Do NOT** initialize with README (we already have one)
6. Click **Create repository**

---

## Step 6: Connect Your Local Repository to GitHub

Copy the HTTPS URL shown on GitHub (e.g. `https://github.com/YOUR_USERNAME/doctor-finder.git`)
then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/doctor-finder.git
```

Verify the remote was added:

```bash
git remote -v
```

---

## Step 7: Rename Branch to 'main' (if needed)

```bash
git branch -M main
```

---

## Step 8: Push to GitHub

```bash
git push -u origin main
```

Enter your GitHub username and Personal Access Token (PAT) when prompted.
To create a PAT: GitHub → Settings → Developer settings → Personal access tokens → Generate new token.

---

## Step 9: Verify on GitHub

Open `https://github.com/YOUR_USERNAME/doctor-finder` in your browser.
You should see all your project files listed there.

---

## For Subsequent Updates

Whenever you make changes to the project:

```bash
# Stage changed files
git add .

# Commit with a descriptive message
git commit -m "Add AJAX CRUD for doctor profiles"

# Push to GitHub
git push
```

---

## Useful Git Commands

| Command | Purpose |
|---------|---------|
| `git status` | See which files are changed |
| `git log --oneline` | View commit history |
| `git diff` | See unstaged changes |
| `git branch` | List all branches |
| `git pull` | Fetch and merge remote changes |
| `git clone <url>` | Clone a repository locally |

---

## Working with Branches (Best Practice)

```bash
# Create and switch to a new feature branch
git checkout -b feature/payment-integration

# Work on your feature, then commit
git add .
git commit -m "Add Paytm payment integration"

# Push the branch to GitHub
git push origin feature/payment-integration

# On GitHub, open a Pull Request to merge into main
```

---

## Summary

After completing these steps, your Doctor Finder project is:
- Tracked with Git version control
- Hosted on GitHub for backup and collaboration
- Ready to be cloned and deployed anywhere, including PythonAnywhere (Practical 18)
