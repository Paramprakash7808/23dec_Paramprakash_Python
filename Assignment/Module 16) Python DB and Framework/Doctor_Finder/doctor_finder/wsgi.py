"""
WSGI config for doctor_finder project.
Practical 18: Used by PythonAnywhere for live deployment.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_finder.settings')

application = get_wsgi_application()
