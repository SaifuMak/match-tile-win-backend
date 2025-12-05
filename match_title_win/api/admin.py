from django.contrib import admin

# Register your models here.
from .models import ConsolationPrize, Participant, Prize, PrizeConfig

admin.site.register(Participant)
admin.site.register(Prize)
admin.site.register(ConsolationPrize)   
admin.site.register(PrizeConfig)