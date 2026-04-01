from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
import requests
import os
from dotenv import load_dotenv
from .models import Doctor
from .serializers import DoctorSerializer
from django.shortcuts import render

load_dotenv()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class DashboardView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return render(request, 'index.html')

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password:
            return Response({"error": "Missing username or password"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.pk})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"})

class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer
    # AllowAny for now so the user can easily test
    permission_classes = [permissions.AllowAny]

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.AllowAny]

# --- Integration Views ---

class WeatherView(APIView):
    def get(self, request):
        city = request.query_params.get('city', 'London')
        
        # 1. Get coordinates for the city (Free Open-Meteo Geocoding API)
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        try:
            geo_response = requests.get(geocode_url)
            geo_data = geo_response.json()
            
            if not geo_data.get('results'):
                return Response({"error": f"City '{city}' not found"}, status=status.HTTP_404_NOT_FOUND)
                
            location = geo_data['results'][0]
            lat = location['latitude']
            lon = location['longitude']
            country = location.get('country', '')
            
            # 2. Get current weather for the coordinates (Free Open-Meteo Weather API)
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json()
            
            if 'current_weather' in weather_data:
                current = weather_data['current_weather']
                return Response({
                    "city": f"{location.get('name', city)}",
                    "country": country,
                    "temperature_celsius": current.get('temperature'),
                    "windspeed_kmh": current.get('windspeed'),
                    "status": "Success",
                    "source": "Open-Meteo (Free API)"
                })
            else:
                return Response({"error": "Failed to retrieve weather data"}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GeocodingView(APIView):
    def get(self, request):
        address = request.query_params.get('address', 'Surat, Gujarat, India')
        
        # Using free Nominatim (OpenStreetMap) API instead of requiring Google Maps API key
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        headers = {'User-Agent': 'DjangoRestApp/1.0'}
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if not data:
                return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                "results": [{
                    "formatted_address": data[0].get('display_name'),
                    "geometry": {
                        "location": {
                            "lat": float(data[0]['lat']),
                            "lng": float(data[0]['lon'])
                        }
                    }
                }],
                "status": "OK",
                "source": "Nominatim (OpenStreetMap)"
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GitHubRepoView(APIView):
    def get(self, request):
        username = request.query_params.get('username', 'google')
        url = f"https://api.github.com/users/{username}/repos"
        try:
            response = requests.get(url)
            # Retrieve limited data for list
            repos = [{"name": r["name"], "url": r["html_url"]} for r in response.json()[:10]]
            return Response(repos)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CountryDetailView(APIView):
    def get(self, request):
        country = request.query_params.get('country', 'India')
        # Use fullText=true to prevent matching "British Indian Ocean Territory" when searching for "India"
        url = f"https://restcountries.com/v3.1/name/{country}?fullText=true"
        try:
            response = requests.get(url)
            data = response.json()[0]
            result = {
                "name": data["name"]["common"],
                "population": data["population"],
                "capital": data.get("capital", ["N/A"])[0],
                "region": data["region"]
            }
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        sid = os.getenv('TWILIO_ACCOUNT_SID')
        token = os.getenv('TWILIO_AUTH_TOKEN')
        from_phone = os.getenv('TWILIO_PHONE_NUMBER', '+1234567890')
        
        if not sid or not token or sid == 'your_twilio_sid':
            return Response({"error": "Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN in .env", "hint": "Please add keys to use actual SMS sending."}, status=status.HTTP_501_NOT_IMPLEMENTED)
            
        try:
            from twilio.rest import Client
            client = Client(sid, token)
            message = client.messages.create(
                body="Your OTP is 123456",
                from_=from_phone,
                to=phone
            )
            return Response({"message": f"OTP successfully sent to {phone}. Message SID: {message.sid}"})
        except Exception as e:
            return Response({"error": f"Twilio Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class TwitterLatestTweetsView(APIView):
    def get(self, request):
        username = request.query_params.get('username', 'elonmusk')
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        if not bearer_token or bearer_token == 'your_twitter_token':
            return Response({"error": "Missing TWITTER_BEARER_TOKEN in .env", "hint": "Twitter API v2 requires an active dev account & bearer token."}, status=status.HTTP_501_NOT_IMPLEMENTED)
            
        try:
            import tweepy
            client = tweepy.Client(bearer_token=bearer_token)
            # Fetch user ID first
            user_response = client.get_user(username=username)
            if not user_response.data:
                return Response({"error": "Twitter user not found"}, status=status.HTTP_404_NOT_FOUND)
                
            user_id = user_response.data.id
            tweets_response = client.get_users_tweets(user_id, max_results=5)
            
            if tweets_response.data:
                tweets = [t.text for t in tweets_response.data]
            else:
                tweets = []
                
            return Response({"tweets": tweets, "user": username})
        except Exception as e:
            return Response({"error": f"Twitter API Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

import stripe
class StripePaymentView(APIView):
    def post(self, request):
        amount = request.data.get('amount', 500) # In cents
        stripe_key = os.getenv('STRIPE_SECRET_KEY')
        
        if not stripe_key or stripe_key == 'your_stripe_key':
            return Response({"error": "Missing STRIPE_SECRET_KEY in .env", "hint": "Provide a Stripe test key like sk_test_..."}, status=status.HTTP_501_NOT_IMPLEMENTED)
            
        stripe.api_key = stripe_key
        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({
                "message": f"Payment intention created successfully.",
                "client_secret": intent.client_secret,
                "amount": amount/100,
                "status": intent.status
            })
        except Exception as e:
            return Response({"error": f"Stripe Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class GitHubRepoCreateView(APIView):
    def post(self, request):
        repo_name = request.data.get('name', 'new-repo')
        token = os.getenv('GITHUB_TOKEN')
        
        if not token or token == 'your_github_token':
            return Response({"error": "Missing GITHUB_TOKEN in .env", "hint": "Provide a Personal Access Token with repo scope."}, status=status.HTTP_501_NOT_IMPLEMENTED)
            
        url = "https://api.github.com/user/repos"
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {
            "name": repo_name,
            "description": "Created via Django REST Framework API",
            "private": False
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 201:
                return Response({"message": f"Repository '{repo_name}' created successfully on GitHub!", "url": response.json().get('html_url')})
            else:
                return Response({"error": "GitHub API failed", "details": response.json()}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
