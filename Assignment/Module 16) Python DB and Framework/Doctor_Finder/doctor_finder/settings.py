"""
Doctor Finder Project - settings.py
Practical 4: Django project structure understanding
Practical 11: Database Connectivity (SQLite default + MySQL option)
Practical 19: Social Authentication (Google & Facebook)
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-doctor-finder-secret-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = ['*']  # For PythonAnywhere deployment (Practical 18)

# Practical 6: Installed apps including the 'doctor' app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Doctor app (Practical 6)
    'doctor',
    # Social Authentication (Practical 19)
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Social auth middleware (Practical 19)
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'doctor_finder.urls'

# Practical 1 & 7: Template configuration (MVT Pattern)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Social auth context processors (Practical 19)
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'doctor_finder.wsgi.application'

# Practical 11: Database Connectivity
# Default: SQLite (works out of the box)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Practical 11: MySQL option (uncomment and configure to use MySQL)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'doctor_finder_db',
#         'USER': 'your_mysql_user',
#         'PASSWORD': 'your_mysql_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript) - Practical 2 & 3
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Doctor profile images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

# Authentication URLs (Practical 13)
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Practical 19: Social Authentication - Google & Facebook
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

# Google OAuth2 credentials (Practical 19) - replace with real keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'YOUR_GOOGLE_CLIENT_ID'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'

# Facebook OAuth2 credentials (Practical 19) - replace with real keys
SOCIAL_AUTH_FACEBOOK_KEY = 'YOUR_FACEBOOK_APP_ID'
SOCIAL_AUTH_FACEBOOK_SECRET = 'YOUR_FACEBOOK_APP_SECRET'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'id, name, email'}

SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Practical 16: Paytm Payment Gateway configuration
PAYTM_MERCHANT_KEY = 'YOUR_PAYTM_MERCHANT_KEY'
PAYTM_MERCHANT_ID = 'YOUR_PAYTM_MERCHANT_ID'
PAYTM_WEBSITE = 'WEBSTAGING'  # Use 'DEFAULT' for production
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'
PAYTM_TRANSACTION_URL = 'https://securegw-stage.paytm.in/order/process'
PAYTM_API_URL = 'https://securegw-stage.paytm.in/merchant-status/getTxnStatus'

# Practical 20: Google Maps API Key
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

# Email configuration for password reset (Practical 13)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
