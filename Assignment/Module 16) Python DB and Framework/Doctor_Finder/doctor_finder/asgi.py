"""
ASGI config for doctor_finder project.
Practical 4: Understanding Django project directory structure.
             asgi.py is part of the standard Django project layout,
             used for async-capable servers (e.g. Daphne, Uvicorn).
Practical 18: PythonAnywhere can also serve via ASGI if configured.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_finder.settings')

application = get_asgi_application()
