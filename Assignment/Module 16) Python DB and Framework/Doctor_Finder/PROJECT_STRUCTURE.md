# Doctor Finder - Django Project Structure
## Practical 4: Understanding Django Project Directory Structure

```
doctor_finder/               ← Root project directory
│
├── manage.py                ← Django CLI utility (runserver, migrate, etc.)
├── requirements.txt         ← All Python dependencies
├── setup_venv.sh            ← Practical 5: Virtual environment setup script
├── PROJECT_STRUCTURE.md     ← This file (Practical 4 explanation)
├── README.md                ← Quick start guide
├── DEPLOYMENT_GITHUB.md     ← Practical 17: Step-by-step GitHub deployment guide
├── DEPLOYMENT_PYTHONANYWHERE.md ← Practical 18: Step-by-step PythonAnywhere guide
├── .gitignore               ← Git ignore rules
│
├── doctor_finder/           ← Project configuration package
│   ├── __init__.py
│   ├── settings.py          ← All project settings (DB, apps, static, etc.)
│   ├── urls.py              ← Root URL configuration (Practical 9)
│   ├── asgi.py              ← Practical 4: ASGI entry point (async server support)
│   └── wsgi.py              ← Practical 4 & 18: WSGI entry point (PythonAnywhere)
│
├── doctor/                  ← Main app (Practical 6: app named 'doctor')
│   ├── __init__.py
│   ├── apps.py              ← App configuration
│   ├── models.py            ← Practical 7, 11, 12: Doctor, PatientProfile, Appointment models
│   ├── views.py             ← Practical 1,2,3,7,9,12,13,14,16,20: All views
│   ├── urls.py              ← Practical 9: URL patterns for all pages
│   ├── forms.py             ← Practical 10, 13: Django forms
│   ├── admin.py             ← Practical 8, 15: Admin panel customization
│   ├── signals.py           ← Practical 13: Auto-create PatientProfile
│   ├── migrations/          ← Database migration files
│   └── templatetags/        ← Practical 7: Custom template tags
│       └── doctor_tags.py
│
├── templates/               ← Practical 1, 7: HTML templates (MVT - Template layer)
│   ├── base.html            ← Base template with navbar & footer
│   ├── doctor/
│   │   ├── home.html        ← Practical 1: "Welcome to Doctor Finder"
│   │   ├── profile.html     ← Practical 2: Doctor profile with CSS
│   │   ├── doctor_list.html ← Practical 12: List all doctors (Read)
│   │   ├── contact.html     ← Practical 9: Contact page
│   │   ├── ajax_crud.html   ← Practical 14: AJAX CRUD operations
│   │   ├── book_appointment.html ← Appointment booking
│   │   ├── payment.html     ← Practical 16: Paytm payment
│   │   └── doctor_map.html  ← Practical 20: Google Maps
│   └── registration/
│       ├── register.html    ← Practical 3, 10, 13: Patient registration + JS validation
│       ├── login.html       ← Practical 13, 19: Login + Social auth
│       ├── profile.html     ← Practical 13: Profile update
│       └── change_password.html ← Practical 13: Password reset
│
├── static/                  ← Static files
│   ├── css/
│   │   └── style.css        ← Practical 2: Custom CSS stylesheet
│   └── js/
│       └── validation.js    ← Practical 3 & 10: JS form validation
│
└── media/                   ← Uploaded files (doctor/patient profile images)
```

## MVT Pattern (Practical 7)
- **Model**    → doctor/models.py (Doctor, PatientProfile, Appointment)
- **View**     → doctor/views.py (all view functions)
- **Template** → templates/ directory (all HTML files)

## How each Practical maps to files:
| Practical | File(s) |
|-----------|---------|
| 1. HTML in Python | templates/doctor/home.html, views.py:home() |
| 2. CSS in Python | static/css/style.css, templates/doctor/profile.html |
| 3. JS Form Validation | static/js/validation.js, templates/registration/register.html |
| 4. Django Intro | manage.py, doctor_finder/ package, this file |
| 5. Virtual Environment | setup_venv.sh, requirements.txt |
| 6. Project & App Creation | doctor/ app, doctor/apps.py |
| 7. MVT Pattern | models.py + views.py + templates/ |
| 8. Django Admin | doctor/admin.py |
| 9. URL Patterns | doctor/urls.py, doctor_finder/urls.py |
| 10. Form Validation JS | static/js/validation.js, forms.py |
| 11. Database Connectivity | settings.py DATABASES section |
| 12. ORM & QuerySets | doctor/models.py, views.py CRUD functions |
| 13. Forms & Authentication | forms.py, views.py auth views, registration/ templates |
| 14. CRUD with AJAX | views.py ajax_* functions, templates/doctor/ajax_crud.html |
| 15. Customizing Admin | doctor/admin.py custom fieldsets & actions |
| 16. Paytm Payment | views.py initiate_payment(), templates/doctor/payment.html |
| 17. GitHub Deployment | DEPLOYMENT_GITHUB.md (dedicated step-by-step guide) |
| 18. PythonAnywhere Deployment | DEPLOYMENT_PYTHONANYWHERE.md (dedicated step-by-step guide), wsgi.py, asgi.py |
| 19. Social Authentication | settings.py AUTHENTICATION_BACKENDS, login.html/register.html |
| 20. Google Maps API | views.py doctor_map(), templates/doctor/doctor_map.html |
