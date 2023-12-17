from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauth.models import UserProfile
from userauth.utils import send_sync_verification_email


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class ProfileSerializer(serializers.ModelSerializer):
    verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('phone', 'avatar', 'verified')


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True, validators=[UniqueValidator(queryset=User.objects.all())])
    profile = ProfileSerializer(required=True, source='user_profile')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('user_profile')
        user_profile = instance.user_profile
        for attr, value in profile_data.items():
            setattr(user_profile, attr, value)
        user_profile.save()
        return super().update(instance, validated_data)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('pk', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        verification = user.user_profile.generate_verification()
        send_sync_verification_email(user.email, verification.verification_code)

        return user
