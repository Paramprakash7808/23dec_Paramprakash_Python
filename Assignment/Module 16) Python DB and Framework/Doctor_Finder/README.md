# Doctor Finder - Django Project
## Module 16: Python DB and Framework

A complete Django web application for finding doctors, booking appointments,
and managing doctor records — covering all 20 practicals from Module 16.

---

## Quick Start

```bash
# Practical 5: Set up virtual environment (automated script)
bash setup_venv.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows

pip install -r requirements.txt

# Practical 11: Database connectivity - run migrations
python manage.py makemigrations
python manage.py migrate

# Practical 8: Create admin superuser
python manage.py createsuperuser

# Practical 4: Run development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

Admin panel: **http://127.0.0.1:8000/admin/**

---

## Practicals Covered

| # | Practical | Key File(s) |
|---|-----------|-------------|
| 1 | HTML in Python | `templates/doctor/home.html`, `views.py:home()` |
| 2 | CSS in Python | `static/css/style.css`, `templates/doctor/profile.html` |
| 3 | JavaScript with Python | `static/js/validation.js`, `templates/registration/register.html` |
| 4 | Django Introduction | `manage.py`, `doctor_finder/` package, `asgi.py`, `wsgi.py` |
| 5 | Virtual Environment | `setup_venv.sh`, `requirements.txt` |
| 6 | Project & App Creation | `doctor/` app, `doctor/apps.py` |
| 7 | MVT Pattern | `models.py` + `views.py` + `templates/` |
| 8 | Django Admin Panel | `doctor/admin.py` |
| 9 | URL Patterns | `doctor/urls.py`, `doctor_finder/urls.py` |
| 10 | Form Validation (JS) | `static/js/validation.js`, `forms.py` |
| 11 | Database Connectivity | `settings.py` DATABASES, `migrations/0001_initial.py` |
| 12 | ORM & QuerySets | `doctor/models.py`, `views.py` CRUD functions |
| 13 | Forms & Authentication | `forms.py`, `views.py` auth views, `registration/` templates |
| 14 | CRUD with AJAX | `views.py` ajax_* functions, `templates/doctor/ajax_crud.html` |
| 15 | Customizing Admin | `doctor/admin.py` custom fieldsets & actions |
| 16 | Paytm Payment | `views.py:initiate_payment()`, `templates/doctor/payment.html` |
| 17 | GitHub Deployment | **`DEPLOYMENT_GITHUB.md`** (step-by-step guide) |
| 18 | PythonAnywhere | **`DEPLOYMENT_PYTHONANYWHERE.md`** (step-by-step guide), `wsgi.py` |
| 19 | Social Authentication | `settings.py` AUTHENTICATION_BACKENDS, `login.html`, `register.html` |
| 20 | Google Maps API | `views.py:doctor_map()`, `templates/doctor/doctor_map.html` |

---

## Configuration Notes

### Practical 11: Database
- **Default: SQLite** — works immediately, no extra setup needed
- **MySQL option**: Uncomment the MySQL DATABASES block in `settings.py`

### Practical 16: Paytm Payment
- `paytmchecksum` is included in `requirements.txt` and auto-installed
- Replace `PAYTM_MERCHANT_KEY` and `PAYTM_MERCHANT_ID` in `settings.py`
- Use staging URL for testing, production URL for live payments

### Practical 17: GitHub Deployment
See the dedicated guide → **`DEPLOYMENT_GITHUB.md`**

### Practical 18: PythonAnywhere Deployment
See the dedicated guide → **`DEPLOYMENT_PYTHONANYWHERE.md`**

### Practical 19: Social Authentication
- **Google**: Create OAuth2 credentials at https://console.developers.google.com
- **Facebook**: Create app at https://developers.facebook.com
- Add keys to `settings.py`: `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`, etc.

### Practical 20: Google Maps
- Get API key at https://console.cloud.google.com
- Enable **Maps JavaScript API**
- Set `GOOGLE_MAPS_API_KEY` in `settings.py`
- Add latitude/longitude to doctor records via the admin panel
