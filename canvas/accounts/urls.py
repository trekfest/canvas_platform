from django.urls import include, path
from .views import UpdateProfilePicture, UserProfileView, registration_email, activate_user, update_user
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    
    path("", include("dj_rest_auth.urls")),
    path('registration/', include('dj_rest_auth.registration.urls')),
    # path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('update/', update_user, name='user-update'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('update-photo/', UpdateProfilePicture.as_view(), name='update_user_photo'),
    path('registration_email/', registration_email, name='registration-email'),
    path('activate/<int:pk>/<str:code>/', activate_user, name='activate-user'),
]