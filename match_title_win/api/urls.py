import django.urls as urls  
from . import views 

urlpatterns = [
    urls.path('register/', views.register_user, name='register_user'),  
]