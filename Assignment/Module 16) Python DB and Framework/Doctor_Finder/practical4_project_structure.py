"""
Practical 4: Create a Django project and understand its directory structure.

Run this script from the project root to print the full project structure
with explanations for every file and folder.

Usage:
    python practical4_project_structure.py
"""

import os

# ── Project structure with explanations ─────────────────────────
STRUCTURE = {
    "doctor_finder/                  (Django project package)": {
        "__init__.py":    "Marks this folder as a Python package",
        "settings.py":   "All project configuration: apps, database, static, auth, etc.",
        "urls.py":        "Root URL configuration — routes incoming requests",
        "wsgi.py":        "WSGI entry point for production deployment (e.g. PythonAnywhere)",
        "asgi.py":        "ASGI entry point for async-capable deployment",
    },
    "doctor/                         (Django app — Practical 6)": {
        "__init__.py":    "Marks this folder as a Python package",
        "models.py":      "Database models: Doctor, PatientProfile, Appointment (Practical 7, 11, 12)",
        "views.py":       "View functions — business logic for each URL (Practical 7, 9, 12-16, 20)",
        "urls.py":        "App-level URL patterns (Practical 9)",
        "admin.py":       "Admin panel configuration and customisation (Practical 8, 15)",
        "forms.py":       "Django Forms with server-side validation (Practical 10, 13)",
        "apps.py":        "App configuration — wires signals on startup (Practical 6, 13)",
        "signals.py":     "Auto-creates PatientProfile on User registration (Practical 13)",
        "migrations/":    "Auto-generated DB migration files (Practical 11)",
        "templatetags/":  "Custom template tags used in HTML templates (Practical 7)",
        "management/commands/seed_doctors.py":
                          "Custom management command for ORM CRUD demo (Practical 12)",
    },
    "templates/                      (All HTML templates — Practical 1, 7)": {
        "base.html":                          "Base layout with nav, CSS, JS includes",
        "doctor/home.html":                   "Home page — 'Welcome to Doctor Finder' (Practical 1)",
        "doctor/profile.html":                "Doctor profile with custom CSS (Practical 2)",
        "doctor/doctor_list.html":            "Doctor list with ORM QuerySet filter (Practical 12)",
        "doctor/contact.html":                "Contact page (Practical 9)",
        "doctor/ajax_crud.html":              "AJAX CRUD management page (Practical 14)",
        "doctor/payment.html":                "Paytm payment redirect page (Practical 16)",
        "doctor/doctor_map.html":             "Google Maps doctor locations (Practical 20)",
        "doctor/book_appointment.html":       "Appointment booking form",
        "registration/register.html":         "Patient registration with JS validation (Practical 3, 10, 13)",
        "registration/login.html":            "Login + Google/Facebook OAuth buttons (Practical 13, 19)",
        "registration/profile.html":          "Profile update form (Practical 13)",
        "registration/change_password.html":  "Password change form (Practical 13)",
        "registration/password_reset_form.html":    "Step 1: Enter email for reset (Practical 13)",
        "registration/password_reset_done.html":    "Step 2: Email sent confirmation",
        "registration/password_reset_email.html":   "Email body template",
        "registration/password_reset_subject.txt":  "Email subject line",
        "registration/password_reset_confirm.html": "Step 3: Enter new password",
        "registration/password_reset_complete.html":"Step 4: Reset success page",
    },
    "static/                         (CSS & JS — Practical 2, 3)": {
        "css/style.css":      "Custom CSS styling for doctor profile page (Practical 2)",
        "js/validation.js":   "JavaScript form validation for email, phone, password (Practical 3, 10)",
    },
    "media/                          (Uploaded files — doctor/patient images)": {},
    "Root files": {
        "manage.py":                   "Django management utility — runserver, migrate, etc. (Practical 4)",
        "requirements.txt":            "All Python dependencies — install with pip (Practical 5)",
        "setup_venv.sh":               "Linux/macOS virtual environment setup script (Practical 5)",
        "setup_venv.bat":              "Windows virtual environment setup script (Practical 5)",
        ".gitignore":                  "Files excluded from Git (Practical 17)",
        "DEPLOYMENT_GITHUB.md":        "Step-by-step GitHub deployment guide (Practical 17)",
        "DEPLOYMENT_PYTHONANYWHERE.md":"Step-by-step PythonAnywhere deployment guide (Practical 18)",
        "README.md":                   "Project overview and setup instructions",
        "PROJECT_STRUCTURE.md":        "Detailed project structure documentation",
    },
}


def print_structure():
    """Print the Django project directory structure with annotations."""
    line = "=" * 70
    print(f"\n{line}")
    print("  Practical 4: Doctor Finder — Django Project Directory Structure")
    print(f"{line}\n")

    for section, files in STRUCTURE.items():
        print(f"📁  {section}")
        if files:
            for filename, explanation in files.items():
                print(f"    ├── {filename}")
                print(f"    │       → {explanation}")
        print()

    print(f"{line}")
    print("  Key Django Concepts shown in this structure:")
    print(f"{line}")
    concepts = [
        ("MVT Pattern (Practical 7)", "models.py → views.py → templates/"),
        ("App Separation (Practical 6)", "doctor/ app inside doctor_finder/ project"),
        ("URL Routing (Practical 9)",   "doctor_finder/urls.py → doctor/urls.py → views.py"),
        ("Static Files (Practical 2,3)","static/css/ and static/js/ served by Django"),
        ("Database (Practical 11)",     "migrations/ auto-generated from models.py"),
        ("Admin (Practical 8,15)",      "admin.py registers models in /admin/ panel"),
        ("Auth (Practical 13)",         "registration/ templates for login, signup, reset"),
        ("Social Auth (Practical 19)",  "social_django handles Google & Facebook OAuth"),
        ("Deployment (Practical 17,18)","DEPLOYMENT_GITHUB.md + DEPLOYMENT_PYTHONANYWHERE.md"),
    ]
    for concept, detail in concepts:
        print(f"  ✔  {concept:<35}  {detail}")
    print(f"{line}\n")


if __name__ == '__main__':
    print_structure()

    # Also verify that expected files actually exist on disk
    print("Checking actual files on disk...\n")
    project_root = os.path.dirname(os.path.abspath(__file__))
    key_files = [
        'manage.py',
        'requirements.txt',
        'setup_venv.sh',
        'setup_venv.bat',
        '.gitignore',
        'doctor_finder/settings.py',
        'doctor_finder/urls.py',
        'doctor/models.py',
        'doctor/views.py',
        'doctor/urls.py',
        'doctor/admin.py',
        'doctor/forms.py',
        'doctor/apps.py',
        'doctor/signals.py',
        'doctor/management/commands/seed_doctors.py',
        'static/css/style.css',
        'static/js/validation.js',
        'templates/base.html',
        'templates/doctor/home.html',
        'templates/doctor/profile.html',
        'templates/doctor/ajax_crud.html',
        'templates/doctor/payment.html',
        'templates/doctor/doctor_map.html',
        'templates/registration/register.html',
        'templates/registration/login.html',
        'DEPLOYMENT_GITHUB.md',
        'DEPLOYMENT_PYTHONANYWHERE.md',
    ]

    all_ok = True
    for rel_path in key_files:
        full_path = os.path.join(project_root, rel_path)
        exists = os.path.exists(full_path)
        status = '✅' if exists else '❌ MISSING'
        print(f"  {status}  {rel_path}")
        if not exists:
            all_ok = False

    print()
    if all_ok:
        print("✅ All key project files are present!\n")
    else:
        print("❌ Some files are missing. Please check the project.\n")
