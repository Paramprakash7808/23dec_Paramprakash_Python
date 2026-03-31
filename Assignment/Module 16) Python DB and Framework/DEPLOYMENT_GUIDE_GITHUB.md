# GitHub Deployment Guide

This guide explains how to deploy the Doctor Finder project to GitHub for version control.

## 1. Initialize Git in the Project Directory
Navigate to your project root folder (e.g., `doctor`) and run:
```bash
git init
```

## 2. Create a .gitignore File
Ensure you don't track sensitive or unnecessary files like `venv/`, `__pycache__/`, and `db.sqlite3`.
```bash
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo "db.sqlite3" >> .gitignore
echo "media/" >> .gitignore
```

## 3. Add and Commit Your Files
Add all project files to the staging area and commit them:
```bash
git add .
git commit -m "Initial commit of Doctor Finder project"
```

## 4. Push to GitHub
Create a new repository on [GitHub](https://github.com/new). Then, link your local repository and push:
```bash
git remote add origin https://github.com/YOUR_USERNAME/doctor-finder.git
git branch -M main
git push -u origin main
```
