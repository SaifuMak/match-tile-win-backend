from django.contrib import admin

# Register your models here.
from .models import Participant, Prize

admin.site.register(Participant)
admin.site.register(Prize)
