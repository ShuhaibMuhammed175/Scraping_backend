from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

urlpatterns = [
    # This uses a custom view that adds extra claims to the token (username and is_admin).
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint to refresh a JWT token using the built-in DRF view.
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # The view checks if the email is unique and registers the user if valid.
    path('register/', views.userRegistrationView.as_view(), name='register')
]
