from django.db import models

# Create your models here.
class Participant(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField()
     phone = models.CharField(max_length=15)
     city = models.CharField(max_length=100)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.name 