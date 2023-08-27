from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tictactoe_app/', include('tictactoe_app.api.urls')),
    path('users_app/', include('users_app.api.urls')),
]
