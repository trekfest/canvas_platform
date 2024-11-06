from rest_framework.generics import RetrieveUpdateAPIView
from .models import UserProfile
from .serializers import UserProfilePhotoSerializer

class UserProfilePhotoView(RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfilePhotoSerializer

    def get_object(self):
        return self.request.user.userprofile # assume userprofile is for each user
                        