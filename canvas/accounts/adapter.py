from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import CustomUser

class GoogleAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email')
        
        # Check if a user with the given email already exists
        user = CustomUser.objects.filter(email=email).first()
        
        if user is None:
            # If the user does not exist, create a new one
            username = email.split('@')[0]
            user = CustomUser(email=email, username=username)
            user.first_name = sociallogin.account.extra_data.get('given_name', '')
            user.last_name = sociallogin.account.extra_data.get('family_name', '')
            user.set_unusable_password()  # or set_password if you want to use it
            user.save()
        
        # Connect the social login to the existing or newly created user
        sociallogin.connect(request, user)
