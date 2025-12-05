import django.urls as urls  
from . import views 

urlpatterns = [
    urls.path('register/', views.register_user, name='register_user'),  
    urls.path('get-my-rewards/', views.get_my_rewards, name='get_my_rewards'),
    urls.path('participants/', views.list_participants, name='list_participants'), 
    urls.path('winners/', views.list_winners, name='list_winners'), 
    urls.path('all-participants/', views.list_all_participants, name='list_all_participants'),
    urls.path('all-winners/', views.list_all_winners, name='list_all_winners'),
    urls.path('update-prize-claim/<int:participant_id>/', views.update_prize_claim_status, name='update_prize_claim_status'),

]