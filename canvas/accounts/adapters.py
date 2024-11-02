# from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# from .models import CustomUser
# import logging

# logger = logging.getLogger(__name__)

# class GoogleAdapter(DefaultSocialAccountAdapter):
#     def pre_social_login(self, request, sociallogin):
#         logger.debug("pre_social_login called")
#         email = sociallogin.account.extra_data.get('email')
#         logger.debug(f"Social login attempt for email: {email}")

#         user = CustomUser.objects.filter(email=email).first()

#         if user is None:
#             logger.debug("No existing user found, creating a new one.")
#             username = email.split('@')[0]
#             user = CustomUser(email=email, username=username)
#             user.first_name = sociallogin.account.extra_data.get('given_name', '')
#             user.last_name = sociallogin.account.extra_data.get('family_name', '')
#             user.set_unusable_password()  # or set_password if you want to use it
#             user.save()
    
    
#         sociallogin.connect(request, user)  

        
#     def get_user_search_fields(self):
#         return ['email', 'username']