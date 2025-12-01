import django.urls as urls  
from . import views 

urlpatterns = [
    urls.path('register/', views.register_user, name='register_user'),  
    urls.path('get-my-rewards/', views.get_my_rewards, name='get_my_rewards'),  

]