# Virtual Environment Setup Guide

This guide explains how to create and activate a virtual environment for the Doctor Finder project.

## 1. Create the Virtual Environment
Running the following command in your project root will create a folder named `venv` containing the isolated Python environment:

```powershell
python -m venv venv
```

## 2. Activate the Virtual Environment
Depending on your operating system and shell, use the following:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

## 3. Install Dependencies
Once activated, you can install all necessary packages:
```bash
pip install -r requirements.txt
```
*(Ensure you have created a requirements.txt file with: `pip freeze > requirements.txt`)*
