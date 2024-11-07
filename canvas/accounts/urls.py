from django.urls import include, path

from .views import registration_email, activate_user, update_user


urlpatterns = [
    
    path("", include("dj_rest_auth.urls")),
    path('registration/', include('dj_rest_auth.registration.urls')),
    # path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('update/', update_user, name='user-update'),
    path('registration_email/', registration_email, name='registration-email'),
    path('activate/<int:pk>/<str:code>/', activate_user, name='activate-user'),
]