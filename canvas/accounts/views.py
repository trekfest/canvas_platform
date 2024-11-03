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
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import CustomUser
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserUpdateSerializer
from dj_rest_auth.views import LoginView
from allauth.account.signals import user_logged_in
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView


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
        if not user.username:
            user.username = email.split('@')[0]  
            user.save()

        if created:
            user.set_password(random_password)
            user.save()  # Ensures the user data is saved
            logger.info(f"Created new user with pk={user.pk}, email={user.email}")

        else:
            logger.info(f"Retrieved existing user with pk={user.pk}, email={user.email}")

        response_data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "pk": user.pk,
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
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

class UserUpdateView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        user_id = self.kwargs.get("pk")  # Assuming 'pk' is used in the URL
        return get_object_or_404(CustomUser, pk=user_id)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)  # This will raise a 400 response if validation fails
        self.perform_update(serializer)  # Save the updated user instance
        return Response(serializer.data)