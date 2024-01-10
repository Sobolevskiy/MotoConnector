from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from rest_framework_simplejwt.views import TokenObtainPairView

from userauth.serializers import MyTokenObtainPairSerializer, RegistrationSerializer, UserProfileSerializer
from userauth.utils import send_sync_verification_email


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
    def _is_user_already_created(email):
        user = User.objects.filter(email=email)

        user_id = None
        exists = user.exists()
        if exists:
            user_id = user.first().pk

        return user_id, exists

    def create(self, request, *args, **kwargs):
        if request.data.get('email'):
            user_id, exists = self._is_user_already_created(request.data['email'])
            if exists:
                return Response({"user_id": user_id, "msg": "User with this email already exists"},
                                status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self._get_response_body(serializer.data), status=status.HTTP_201_CREATED, headers=headers)


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsOwnerOrReadVerified,)
    serializer_class = UserProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email(request):
    # TODO: добавить сериалайзер
    user_id = request.data.get('user_id')
    token = request.data.get('token')
    user = User.objects.get(id=user_id)
    if user.codes.last().is_valid(token):
        user.user_profile.verified = True
        user.user_profile.save()
    return Response({'success': True, "msg": "User verified"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_email(request):
    # TODO: добавить сериалайзер
    user_id = request.data.get('user_id')
    user = User.objects.get(id=user_id)
    verification = user.user_profile.generate_verification()
    send_sync_verification_email(user.email, verification.verification_code)
