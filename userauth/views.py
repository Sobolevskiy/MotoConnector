from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework_simplejwt.views import TokenObtainPairView

from userauth.serializers import MyTokenObtainPairSerializer, RegistrationSerializer, UserProfileSerializer
from service import tasks


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_profile.verified)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self._get_response_body(serializer.data), status=status.HTTP_201_CREATED, headers=headers)


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsOwner,)
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
    tasks.send_verification_email.apply_async(args=[user.email, verification.verification_code])
