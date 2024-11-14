import logging
import secrets
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from urllib.parse import urljoin
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from django.views import View
import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import CustomUser
from .serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from dj_rest_auth.views import LoginView
from allauth.account.signals import user_logged_in
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from hashlib import sha256
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# send_mail('A cool subject', 'A stunning message', settings.EMAIL_HOST_USER, ["colten478@gmail.com"])

User = get_user_model()
logger = logging.getLogger(__name__)

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get("code")

        if code is None:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_endpoint_url = "https://oauth2.googleapis.com/token"
        
        payload = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_endpoint_url, data=payload)

        if response.status_code != 200:
            return Response(response.json(), status=response.status_code)

        tokens = response.json()
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")

        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_response = requests.get(
            user_info_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info_response.status_code != 200:
            return Response(user_info_response.json(), status=user_info_response.status_code)

        user_info = user_info_response.json()
        email = user_info.get("email")
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")

        random_password = secrets.token_urlsafe(20)

        # Retrieve or create the user in the database
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'username': email.split('@')[0],
                "first_name": first_name,
                "last_name": last_name,
                'password': random_password
            }
        )
        if created:
            user.set_password(random_password)
            user.save()
            logger.info(f"Created new user with pk={user.pk}, email={user.email}")
        else:
            logger.info(f"Retrieved existing user with pk={user.pk}, email={user.email}")

        # Generate a JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Prepare the response data
        response_data = {
            "access_token": access_token,
            "refresh_token": str(refresh),
            "user": {
                "pk": user.pk,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,    
            }
        }

        # Create the response object and set cookies
        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=str(refresh),
            httponly=True,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        return response
    
@receiver(user_logged_in)
def save_google_user_data(sender, request, user, **kwargs):
    user.email = request.user.email
    user.first_name = request.user.first_name
    user.last_name = request.user.last_name
    user.save()


class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
    
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class UserLoginView(LoginView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def registration_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        code = sha256((username + email + settings.EMAIL_SECRET_KEY).encode()).hexdigest()

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                "first_name": first_name,
                "last_name": last_name,
                'is_active': False,
            }
        )
        if created:
            user.set_password(password)
            user.save()

            send_mail(
                'Activate your account',
                f'Click this link to activate your account: http://localhost:8000/api/v1/auth/activate/{user.pk}/{code}',
                settings.EMAIL_HOST_USER,
                [email]
            )
        
        return JsonResponse({"message": "Email sent"}, status=200)
    else:
        return HttpResponse("You need to make a POST request to this endpoint to send an email.")
    
@csrf_exempt
def activate_user(request, pk, code):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.is_active:
        return HttpResponse("User already activated")
    
    if sha256((user.username + user.email + settings.EMAIL_SECRET_KEY).encode()).hexdigest() == code:
        user.is_active = True
        user.save()

        # Generate JWT token for activated user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        return JsonResponse({"message": "User activated", "access_token": access_token}, status=200)
    else:
        return HttpResponse("Invalid activation code")

@csrf_exempt
def update_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # Ensure the user is authenticated via JWT
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            return JsonResponse({"error": "Authorization header is missing"}, status=401)

        try:
            # Split 'Bearer' and the actual token
            token = auth_header.split()[1]
            # Attempt to decode the token and get the user
            user = JWTAuthentication().get_user(validated_token=token)
            
            # Debugging: print out the user object to inspect its structure
            print(f"Decoded JWT token result: {user}")
            
            if isinstance(user, str):
                # If the user is a string, it might be an error message, so handle it
                return JsonResponse({"error": "Authentication failed. Token invalid or expired."}, status=401)
            
        except Exception as e:
            return JsonResponse({"error": f"Authentication failed: {str(e)}"}, status=401)

        # Find the user to update by email (only admin can update others)
        if data.get("email"):
            target_user = get_object_or_404(CustomUser, email=data.get("email"))
        else:
            return JsonResponse({"error": "Missing email"}, status=400)

        # Check if the authenticated user is an admin
        if user.role != 'admin':  # Only admin can update other users
            if user != target_user:
                return JsonResponse({"error": "You can only update your own information"}, status=403)

        # Update the user fields (admin can update all, non-admins can only update their own details)
        if data.get("username"):
            target_user.username = data.get("username")
        if data.get("first_name"):
            target_user.first_name = data.get("first_name")
        if data.get("last_name"):
            target_user.last_name = data.get("last_name")

        if user.role == 'admin':  # Admin can update roles
            if data.get("role"):
                new_role = data.get("role")
                if new_role in ['admin', 'student', 'teacher']:
                    target_user.role = new_role
                else:
                    return JsonResponse({"error": "Invalid role. Valid roles are: admin, student, teacher."}, status=400)

        # Save the updated user
        target_user.save()

        return JsonResponse({"message": "User updated successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

class UpdateProfilePicture(APIView):
    """
    This view allows a user to update their profile picture using an access token for authentication.
    """
    permission_classes = [IsAuthenticated]  # Require authentication to access this view

    def post(self, request, *args, **kwargs):
        # Step 1: Retrieve the profile photo from the request
        if 'image' not in request.FILES:
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES['image']

        # Step 2: Get the authenticated user
        user = request.user

        # Step 3: Save the uploaded image to the user's profile
        user.image.save(f"{user.username}_profile.jpg", image, save=True)

        return Response({"message": "Profile picture updated successfully"}, status=status.HTTP_200_OK)

    def verify_google_token(self, access_token):
        """
        Verify the access token by making a request to Google's OAuth 2.0 endpoint.
        """
        url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()  # Returns the user info if token is valid
        else:
            return None  # Return None if token is invalid
    
class UserProfileView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
