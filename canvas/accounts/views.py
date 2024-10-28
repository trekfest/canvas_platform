from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from urllib.parse import urljoin
from django.shortcuts import render
from django.views import View
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        This endpoint processes the Google OAuth callback and exchanges the authorization code
        for access tokens.
        """

        code = request.GET.get("code")

        if code is None:
            return Response({"error": "Authorization code not provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Endpoint to exchange code for access token
        token_endpoint_url = "https://oauth2.googleapis.com/token"
        
        # Payload for the POST request to exchange code for tokens
        payload = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH_CALLBACK_URL,
            'grant_type': 'authorization_code'
        }

        # Make a POST request to exchange the code
        response = requests.post(token_endpoint_url, data=payload)

        # Check for successful response
        if response.status_code != 200:
            return Response(response.json(), status=response.status_code)

        # Assuming successful response; now parse the tokens
        tokens = response.json()
        
        # You might want to include the user's profile information retrieval here
        return Response(tokens, status=status.HTTP_200_OK)


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