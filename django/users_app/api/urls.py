from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users_app.api.views import LogoutAPIView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]