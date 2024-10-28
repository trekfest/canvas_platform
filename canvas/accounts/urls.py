from django.urls import include, path

from .views import GoogleLogin, LoginPage


urlpatterns = [
    
    path("login/", LoginPage.as_view(), name="login"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')),
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    
]