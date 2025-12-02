from django.db import models

# Create your models here.
class Participant(models.Model):
     name = models.CharField(max_length=100)
     email = models.EmailField()
     phone = models.CharField(max_length=15)
     city = models.CharField(max_length=100)
     created_at = models.DateTimeField(auto_now_add=True)
     reward = models.PositiveBigIntegerField(null=True, blank=True)
     has_won = models.BooleanField(default=False)
     time_taken = models.CharField(max_length=50, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
     played_at = models.DateTimeField(auto_now=True,null=True, blank=True)

     def __str__(self):
         return self.name 
     

class Prize(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField()  # $10 / $20 / $50 / $100 etc.
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.amount} Gift Card ({self.quantity} left)"
