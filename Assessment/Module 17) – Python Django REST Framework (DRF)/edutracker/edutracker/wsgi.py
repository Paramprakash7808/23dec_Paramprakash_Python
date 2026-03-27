"""
WSGI config for EduTracker project.
Used by PythonAnywhere and other WSGI-compatible servers.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edutracker.settings')

application = get_wsgi_application()
