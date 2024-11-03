from django.urls import include, path

from .views import UserUpdateView


urlpatterns = [
    
    path("", include("dj_rest_auth.urls")),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    
]