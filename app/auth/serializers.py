from datetime import datetime, timezone
import datetime as dt
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from app.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False,)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user
    


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=250, read_only=True)
    last_name = serializers.CharField(max_length=250, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


    def validate(self, data):

        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            # signin_count = (user.sign_in_count) + 1
            # user.sign_in_count = signin_count
            # user.last_sign_in_at = user.current_sign_in_at
            # user.current_sign_in_at = datetime.now(tz=timezone.utc)
            # user.api_token = access_token
            user.save()

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'first_name' : user.first_name,
                'last_name': user.last_name
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

