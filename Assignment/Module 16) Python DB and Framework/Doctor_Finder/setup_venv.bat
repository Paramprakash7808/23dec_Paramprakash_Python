@echo off
REM ========================================
REM   Doctor Finder - Virtual Env Setup
REM   Practical 5: Virtual Environment
REM   Windows Version (.bat)
REM ========================================

echo.
echo ========================================
echo   Doctor Finder - Virtual Env Setup
echo   Practical 5: Virtual Environment
echo ========================================

REM Step 1: Create a virtual environment named 'venv'
echo.
echo [Step 1] Creating virtual environment 'venv'...
python -m venv venv

REM Step 2: Activate the virtual environment (Windows)
echo [Step 2] Activating virtual environment...
call venv\Scripts\activate

REM Step 3: Upgrade pip
echo [Step 3] Upgrading pip...
pip install --upgrade pip

REM Step 4: Install Django and all project dependencies
echo [Step 4] Installing Django and all dependencies from requirements.txt...
pip install -r requirements.txt

REM Step 5: Apply database migrations (Practical 11: Database Connectivity)
echo [Step 5] Running database migrations (Practical 11)...
python manage.py makemigrations
python manage.py migrate

REM Step 6: Seed sample doctor data (Practical 12: ORM CRUD)
echo [Step 6] Seeding sample doctor records (Practical 12)...
python manage.py seed_doctors

REM Step 7: Collect static files
echo [Step 7] Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Activate env :  venv\Scripts\activate
echo   2. Create admin :  python manage.py createsuperuser
echo   3. Run server   :  python manage.py runserver
echo   4. Open browser :  http://127.0.0.1:8000
echo.
pause
