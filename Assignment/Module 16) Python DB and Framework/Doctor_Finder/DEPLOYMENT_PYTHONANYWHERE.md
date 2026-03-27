# Practical 18: Live Project Deployment on PythonAnywhere
## Deploy Doctor Finder Django project on PythonAnywhere (accessible online)

This guide walks you through every step to make the Doctor Finder project
live on the internet using PythonAnywhere's free hosting.

---

## Prerequisites

- Doctor Finder project pushed to GitHub (see DEPLOYMENT_GITHUB.md - Practical 17)
- A PythonAnywhere account (free at https://www.pythonanywhere.com)

---

## Step 1: Create a PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Click **Start running Python online in less than a minute!**
3. Choose **Create a Beginner account** (free)
4. Fill in username, email, password
5. Verify your email and log in

Your live URL will be: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Step 2: Open a Bash Console

From the PythonAnywhere Dashboard:

1. Click the **Consoles** tab
2. Under "Start a new console", click **Bash**

---

## Step 3: Clone Your GitHub Repository

In the Bash console, run:

```bash
git clone https://github.com/YOUR_USERNAME/doctor-finder.git
cd doctor-finder
```

---

## Step 4: Set Up Virtual Environment on PythonAnywhere

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 5: Configure the Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## Step 6: Update settings.py for Production

Edit `doctor_finder/settings.py`:

```python
# Change ALLOWED_HOSTS to your PythonAnywhere domain
ALLOWED_HOSTS = ['YOUR_USERNAME.pythonanywhere.com']

# Set DEBUG to False for production
DEBUG = False

# Make sure STATIC_ROOT is set
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## Step 7: Set Up the Web App on PythonAnywhere

1. Go to the **Web** tab in the PythonAnywhere Dashboard
2. Click **Add a new web app**
3. Click **Next** (your domain is `YOUR_USERNAME.pythonanywhere.com`)
4. Choose **Manual configuration** (NOT the Django option)
5. Select **Python 3.10**
6. Click **Next**

---

## Step 8: Configure the WSGI File

On the Web tab, find the **WSGI configuration file** link (looks like
`/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`) and click it.

Delete all the existing contents and replace with:

```python
import sys
import os

# Add your project directory to the Python path
path = '/home/YOUR_USERNAME/doctor-finder'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'doctor_finder.settings'

# Start the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `YOUR_USERNAME` with your actual PythonAnywhere username.**

Click **Save**.

---

## Step 9: Configure the Virtual Environment

Back on the **Web** tab, find the **Virtualenv** section.

Enter the path:

```
/home/YOUR_USERNAME/doctor-finder/venv
```

Click the checkmark to save.

---

## Step 10: Configure Static Files

On the **Web** tab, scroll to the **Static files** section.

Click **Enter URL** and set:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/YOUR_USERNAME/doctor-finder/staticfiles/` |
| `/media/` | `/home/YOUR_USERNAME/doctor-finder/media/` |

---

## Step 11: Reload the Web App

At the top of the **Web** tab, click the green **Reload** button:

```
Reload YOUR_USERNAME.pythonanywhere.com
```

---

## Step 12: Visit Your Live App

Open your browser and go to:

```
https://YOUR_USERNAME.pythonanywhere.com
```

You should see the Doctor Finder home page with **"Welcome to Doctor Finder"**.

Admin panel is at:

```
https://YOUR_USERNAME.pythonanywhere.com/admin/
```

---

## Updating the Live App After Changes

Whenever you push new code to GitHub:

```bash
# In PythonAnywhere Bash console:
cd ~/doctor-finder
git pull
source venv/bin/activate
pip install -r requirements.txt   # if dependencies changed
python manage.py migrate          # if models changed
python manage.py collectstatic --noinput
```

Then go to the **Web** tab and click **Reload**.

---

## Troubleshooting

### Error log location
```
/var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

View it in the Bash console:
```bash
tail -50 /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### Common issues

| Problem | Solution |
|---------|---------|
| 500 error on site | Check the error log; usually a missing migration or wrong WSGI path |
| Static files not loading | Re-run `collectstatic` and check static files paths on Web tab |
| `DisallowedHost` error | Add your domain to `ALLOWED_HOSTS` in settings.py |
| Database errors | Run `python manage.py migrate` again in Bash console |
| Import errors | Make sure `venv` path is set correctly on Web tab |

---

## Summary

After completing these steps:
- Doctor Finder is **live on the internet**
- Accessible at `https://YOUR_USERNAME.pythonanywhere.com`
- Admin panel available at `/admin/`
- Automatically serves your Django app using WSGI
