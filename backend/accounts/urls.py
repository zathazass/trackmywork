from django.urls import path
from .views import LoginAPI, LogoutAPI

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)


urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('verify-token/', TokenVerifyView.as_view(), name='verify_token'),
]
