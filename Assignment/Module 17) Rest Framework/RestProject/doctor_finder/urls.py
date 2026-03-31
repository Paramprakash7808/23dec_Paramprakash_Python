from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    # Phase 3: Doctor CRUD APIs (Lab 6 URL Routing)
    path('doctors/', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', views.DoctorRetrieveUpdateDestroyView.as_view(), name='doctor-detail'),
    
    # Phase 4: Auth API (Token Auth for Lab 13)
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
    # Note: Google Login is handled via allauth at /accounts/

    # Phase 4: Third-Party API Integrations
    path('weather/', views.OpenWeatherView.as_view(), name='api-weather'),
    path('geocode/', views.GeocodeView.as_view(), name='api-geocode'),
    path('github/', views.GitHubIntegrationView.as_view(), name='api-github'),
    path('twitter/', views.TwitterIntegrationView.as_view(), name='api-twitter'),
    path('country/', views.RestCountriesView.as_view(), name='api-country'),
    path('sendgrid/', views.SendGridEmailView.as_view(), name='api-sendgrid'),
    path('twilio/', views.TwilioOTPView.as_view(), name='api-twilio'),
    path('stripe/', views.StripePaymentView.as_view(), name='api-stripe'),

    # Phase 5: Map/Dashboard View is now at the Project Root.
]
