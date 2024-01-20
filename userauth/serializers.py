from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from userauth.models import UserProfile
from userauth.utils import send_sync_verification_email


class TokenValidationError(Exception):
    pass


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True, validators=[UniqueValidator(queryset=User.objects.all())])
    profile = ProfileSerializer(required=True, source='user_profile')
    # groups = GroupSerializer(many=True, read_only=True)
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile', 'groups', 'is_staff', 'is_superuser')

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


class VerifyEmailSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.get(id=attrs['user_id'])
        if not user.codes.last().is_valid(attrs['token']):
            raise TokenValidationError('Invalid code')
        else:
            user.user_profile.verified = True
            user.user_profile.save()
        return attrs


class VerifyEmailResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True, initial=True)
    msg = serializers.CharField(default='User verified', initial='User verified')


class ResendEmailSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
