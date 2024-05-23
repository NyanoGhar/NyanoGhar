from rest_framework import serializers
from .models import User,UserProfile
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import check_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Fetch user based on the provided username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid username')

            # Check if the password matches
            if not check_password(password, user.password):
                raise serializers.ValidationError('Invalid password')

            # Check if the user account is active
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')

            # If everything is valid, add the user to the data dictionary
            data['user'] = user
        else:
            raise serializers.ValidationError('Both username and password are required')

        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['biography', 'contact_information']