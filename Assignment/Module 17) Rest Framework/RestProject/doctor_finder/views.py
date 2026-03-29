from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.conf import settings
from django.shortcuts import render
from .models import Doctor
from .serializers import DoctorSerializer
import requests
import stripe
from twilio.rest import Client
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import json

# ================================
# Phase 5: Map View Integration
# ================================
def map_view(request):
    """
    Lab 22: Google Maps Integration
    """
    doctors = Doctor.objects.all()
    doctor_data = [
        {"name": d.name, "lat": d.latitude, "lng": d.longitude, "specialty": d.specialty}
        for d in doctors if d.latitude is not None and d.longitude is not None
    ]
    return render(request, 'doctor_finder/index.html', {'doctor_data': json.dumps(doctor_data)})


# ================================
# Phase 3: Doctor CRUD Views
# ================================

class DoctorListCreateView(generics.ListCreateAPIView):
    """
    Lab 5 & 7 & 12: View to List and Create Doctor Profiles with Pagination.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # Lab 13: Limit access somewhat

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Lab 5 & 12: View to Read, Update, Delete Doctor Profiles.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ================================
# Phase 4: Third-Party API Integrations
# ================================

class OpenWeatherView(APIView):
    """
    Lab 14: Fetch OpenWeatherMap Data.
    Expected usage: /api/weather/?city=London
    """
    permission_classes = [AllowAny]
    def get(self, request):
        city = request.query_params.get('city', 'New York')
        api_key = settings.OPENWEATHERMAP_API_KEY
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        return Response(response.json(), status=response.status_code)

class GeocodeView(APIView):
    """
    Lab 15: Google Maps Geocoding API.
    Expected usage: /api/geocode/?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA
    *Uses OpenStreetMap Nominatim as fallback for demonstration so you don't need real CC API keys initially*
    """
    permission_classes = [AllowAny]
    def get(self, request):
        address = request.query_params.get('address', '')
        # Using free Nominatim to fulfill the "convert address to lat long requirement" without billing issues
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        try:
            response = requests.get(url, headers={'User-Agent': 'Tops_Assignment_App'})
            data = response.json()
            if data:
                return Response({'latitude': data[0]['lat'], 'longitude': data[0]['lon']})
            return Response({'error': 'Address not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GitHubIntegrationView(APIView):
    """
    Lab 16: GitHub API Integration.
    Create a repository or retrieve user data.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        token = settings.GITHUB_API_TOKEN
        repo_name = request.data.get('repo_name', 'rest-framework-lab-repo')
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        
        url = "https://api.github.com/user/repos"
        payload = {"name": repo_name, "private": False}
        
        response = requests.post(url, json=payload, headers=headers)
        return Response(response.json(), status=response.status_code)

    def get(self, request):
        username = request.query_params.get('username', 'octocat')
        url = f"https://api.github.com/users/{username}/repos"
        response = requests.get(url)
        return Response(response.json(), status=response.status_code)

class TwitterIntegrationView(APIView):
    """
    Lab 17: Fetch recent tweets.
    Since Twitter API has strict paid tiers, this returns mocked data for demonstration
    unless a real bearer token is somehow provided.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        username = request.query_params.get('username', 'example_user')
        mock_tweets = [
            {"id": 1, "text": f"Hello world from {username}!"},
            {"id": 2, "text": "Learning Django REST Framework is awesome!"},
            {"id": 3, "text": "Just completed my API integration lab."},
        ]
        return Response({"user": username, "tweets": mock_tweets})

class RestCountriesView(APIView):
    """
    Lab 18: Fetch country details.
    Expected usage: /api/country/?name=india
    """
    permission_classes = [AllowAny]
    def get(self, request):
        country_name = request.query_params.get('name', 'india')
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()[0]
            # Extract population, language, currency
            currencies = data.get('currencies', {})
            languages = data.get('languages', {})
            
            summary = {
                "name": data.get("name", {}).get("common"),
                "population": data.get("population"),
                "currency": currencies,
                "languages": languages
            }
            return Response(summary)
        return Response({"error": "Country not found"}, status=response.status_code)

class SendGridEmailView(APIView):
    """
    Lab 19: Send Email using Sendgrid
    """
    permission_classes = [AllowAny]
    def post(self, request):
        to_email = request.data.get('email', 'test@example.com')
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        from_email = Email("your_verified_email@example.com")
        to_email = To(to_email)
        subject = "Registration Confirmation"
        content = Content("text/plain", "Thanks for registering at Doctor Finder!")
        mail = Mail(from_email, to_email, subject, content)
        
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
            return Response({"message": "Email sent"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class TwilioOTPView(APIView):
    """
    Lab 20: Send OTP via Twilio
    """
    permission_classes = [AllowAny]
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "phone_number required"}, status=400)
            
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        try:
            message = client.messages.create(
                body="Your OTP for Doctor Finder is: 123456",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            return Response({"message": "OTP Sent", "sid": message.sid})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class StripePaymentView(APIView):
    """
    Lab 21: Stripe Payment intent creation for booking
    """
    permission_classes = [AllowAny]
    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = request.data.get('amount', 5000) # 5000 cents = $50
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={'integration_check': 'accept_a_payment'},
            )
            return Response({"client_secret": intent.client_secret})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
