from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

# serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Check if passwords match
        if validated_data['password'] != validated_data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})

        # create a new user
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user


# serializer for user login
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(request=self.context.get('request'), **attrs)
        if user:
            return user
        raise serializers.ValidationError("Invalid credentials")


# serializer for user profile updat
class UserUpdateSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)  # add profile photo field

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'profile_photo'] 
        extra_kwargs = {
            'email': {'read_only': True}  
        }

    def update(self, instance, validated_data):
        # updat user fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)

        # handle profile photo update if provided
        if validated_data.get('profile_photo'):
            instance.profile_photo = validated_data['profile_photo']

        instance.save()
        return instance
