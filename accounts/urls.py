from django.urls import path
from . import views
from . import apis

from rest_framework_simplejwt.views import (
    TokenRefreshView, TokenVerifyView
)

app_name = 'accounts'

urlpatterns = [
    path('api/login/', apis.LoginAPI.as_view(), name='login'),
    path('api/logout/', apis.LogoutAPI.as_view(), name='logout'),
    path('api/refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/verify-token/', TokenVerifyView.as_view(), name='verify_token'),

    path('login/', views.login_page, name='login_page'),
    path('home/', views.home_page, name='home_page'),
]
