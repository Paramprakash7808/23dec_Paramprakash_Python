from django.urls import path
from .views import (
    DoctorListCreateView, DoctorRetrieveUpdateDestroyView,
    RegisterView, LoginView, LogoutView,
    WeatherView, GeocodingView, GitHubRepoView, GitHubRepoCreateView,
    CountryDetailView, SendOTPView, TwitterLatestTweetsView, StripePaymentView
)

urlpatterns = [
    # Doctor CRUD
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor-detail'),
    
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('weather/', WeatherView.as_view(), name='weather'),
    path('geocode/', GeocodingView.as_view(), name='geocode'),
    path('github/repos/', GitHubRepoView.as_view(), name='github-repos'),
    path('github/repos/create/', GitHubRepoCreateView.as_view(), name='github-repo-create'),
    path('country/', CountryDetailView.as_view(), name='country-detail'),
    path('twitter/tweets/', TwitterLatestTweetsView.as_view(), name='twitter-tweets'),
    path('otp/send/', SendOTPView.as_view(), name='otp-send'),
    path('payment/stripe/', StripePaymentView.as_view(), name='stripe-payment'),
]
