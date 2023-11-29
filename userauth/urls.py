from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from userauth.views import MyObtainTokenPairView, UserRegistrationView, UserProfileView, verify_email, resend_email


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', UserRegistrationView.as_view(), name='user_registration'),
    path('registration/verify_email/', verify_email, name='verify_email'),
    path('registration/resend_email/', resend_email, name='resend_email'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]
