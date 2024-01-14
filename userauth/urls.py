from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from userauth.views import MyObtainTokenPairView, UserRegistrationView, UserProfileView, verify_email, resend_email
from drf_yasg.utils import swagger_auto_schema
from userauth.openapi import registration_response_schema_dict


decorated_registration_view = swagger_auto_schema(
    method='post',
    responses=registration_response_schema_dict
)(UserRegistrationView.as_view())

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', decorated_registration_view, name='user_registration'),
    path('registration/verify_email/', verify_email, name='verify_email'),
    path('registration/resend_email/', resend_email, name='resend_email'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]
