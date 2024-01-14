from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

from userauth.serializers import (
    MyTokenObtainPairSerializer,
    RegistrationSerializer,
    UserProfileSerializer,
    VerifyEmailSerializer,
    VerifyEmailResponseSerializer,
    TokenValidationError,
    ResendEmailSerializer,
)
from userauth.utils import send_sync_verification_email
from userauth.openapi import (
    verify_email_response_schema_dict,
    resend_email_response_schema_dict,
    registration_response_schema_dict
)


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_profile.verified)


class IsOwnerOrReadVerified(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.user_profile.verified)
        else:
            return obj.pk == request.user.pk


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    @staticmethod
    def _get_response_body(instance_data):
        return {"success": True, "msg": "Verification code sent", "user_id": instance_data.get('pk')}

    @staticmethod
    def _is_user_already_exists(email):
        exists = False
        msg = {}
        user = User.objects.filter(email=email)

        if user.exists():
            finded_user = user.first()
            exists = True
            msg = {
                "user_id": finded_user.pk,
                "verified": finded_user.user_profile.verified,
                "msg": "User with this email already exists"
            }

        return exists, msg

    def create(self, request, *args, **kwargs):
        if request.data.get('email'):
            exists, msg = self._is_user_already_exists(request.data['email'])
            if exists:
                return Response(
                    msg,
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #TODO: переделать ответ на сериалайзеры
        return Response(self._get_response_body(serializer.data), status=status.HTTP_201_CREATED, headers=headers)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadVerified,)
    serializer_class = UserProfileSerializer


@swagger_auto_schema(method='post',
                     request_body=VerifyEmailSerializer,
                     responses=verify_email_response_schema_dict
                     )
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    msg = None
    success = True
    resp_status = status.HTTP_200_OK

    serializer = VerifyEmailSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except TokenValidationError as e:
        msg = str(e)
        resp_status = status.HTTP_403_FORBIDDEN
        success = False
    finally:
        resp_data = {'success': success}
        if msg:
            resp_data['msg'] = msg
        resp = VerifyEmailResponseSerializer(data=resp_data)
        resp.is_valid()

    return Response(resp.data, status=resp_status)


@swagger_auto_schema(method='post', request_body=ResendEmailSerializer, responses=resend_email_response_schema_dict)
@api_view(['POST'])
@permission_classes([AllowAny])
def resend_email(request):
    serializer = ResendEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.get(id=serializer.data['user_id'])
    verification = user.user_profile.generate_verification()
    send_sync_verification_email(user.email, verification.verification_code)
    return Response(status=status.HTTP_200_OK)
