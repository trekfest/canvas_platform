from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models. CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)