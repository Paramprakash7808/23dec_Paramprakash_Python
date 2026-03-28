#!/bin/bash
# Practical 5: Create and activate a virtual environment, then install Django.
# Run this script once to set up your development environment.

echo "========================================"
echo "  Doctor Finder - Virtual Env Setup"
echo "  Practical 5: Virtual Environment"
echo "========================================"

# Step 1: Create a virtual environment named 'venv'
echo ""
echo "[Step 1] Creating virtual environment 'venv'..."
python3 -m venv venv

# Step 2: Activate the virtual environment
echo "[Step 2] Activating virtual environment..."
# On Linux/macOS:
source venv/bin/activate
# On Windows use: venv\Scripts\activate

# Step 3: Upgrade pip to latest version
echo "[Step 3] Upgrading pip..."
pip install --upgrade pip

# Step 4: Install Django and all project dependencies
echo "[Step 4] Installing Django and all dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 5: Apply database migrations (Practical 11: Database Connectivity)
echo "[Step 5] Running database migrations (Practical 11)..."
python manage.py makemigrations
python manage.py migrate

# Step 6: Seed sample doctor data (Practical 12: ORM CRUD Demo)
echo "[Step 6] Seeding sample doctor records (Practical 12)..."
python manage.py seed_doctors

# Step 7: Collect static files
echo "[Step 7] Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Activate env :  source venv/bin/activate"
echo "  2. Create admin :  python manage.py createsuperuser"
echo "  3. Run server   :  python manage.py runserver"
echo "  4. Open browser :  http://127.0.0.1:8000"
echo ""
echo "To activate the virtual environment later:"
echo "  Linux/macOS : source venv/bin/activate"
echo "  Windows     : venv\\Scripts\\activate"
