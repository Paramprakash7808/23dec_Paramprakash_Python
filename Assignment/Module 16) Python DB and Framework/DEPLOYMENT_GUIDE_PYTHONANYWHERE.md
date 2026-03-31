# PythonAnywhere Deployment Guide

This guide explains how to deploy the Doctor Finder project to PythonAnywhere.

## 1. Hosting on PythonAnywhere
Sign up for a [PythonAnywhere](https://www.pythonanywhere.com/) account. Then, upload your project files via the Files tab or by cloning from GitHub within a PythonAnywhere bash console.

## 2. Set Up a Virtual Environment
In the Bash console, navigate to your project directory and run:
```bash
mkvirtualenv --python=/usr/bin/python3.11 myenv
pip install django django-allauth requests pillow cryptography PyJWT
```

## 3. Configure Static Files
Go to the Web tab in PythonAnywhere and add the following mapping:
- **Static URL:** `/static/`
- **Static path:** `/home/YOUR_USERNAME/doctor/staticfiles/`

## 4. Edit the WSGI Configuration
Open the WSGI configuration file listed on the Web tab and set the `path` and `os.environ`:
```python
import os
import sys

path = '/home/YOUR_USERNAME/doctor'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'doctor.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## 5. Migrate Your Database
In the Bash console, run:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 6. Access Your Site
Visit your personalized URL (e.g., `http://YOUR_USERNAME.pythonanywhere.com`) to see your project live!
