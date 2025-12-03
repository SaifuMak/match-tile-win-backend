from django.urls import path,include

from .views import *

urlpatterns = [

   path('login-admin/', login, name='login_admin'),
   path('check/', CheckLoginStatus.as_view(), name='check'),
   path('logout/', user_logout, name='user_logout'),
#   path('change-password/', change_password, name='change_password'),
]