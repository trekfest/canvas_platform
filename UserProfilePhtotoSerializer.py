from rest_framework import serializers
from .models import SUerProfile


class UserProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
         model = UserProfile
         fields = ['profile_photo']