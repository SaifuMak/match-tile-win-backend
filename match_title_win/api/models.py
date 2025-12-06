from django.db import models
from match_title_win.storages_backends import R2PublicStorage
from match_title_win.mixins import R2PublicURLMixin
# Create your models here.


class Participant(R2PublicURLMixin,models.Model):
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
     retailer = models.CharField(max_length=100, null=True, blank=True)
     amount_spent = models.PositiveBigIntegerField(null=True, blank=True)
     has_played = models.BooleanField(default=False, null=True, blank=True)
     invoice = models.FileField(
        upload_to='assets/invoices/',
        storage=R2PublicStorage(),
        blank=True, null=True
    )
     invoice_public_url = models.URLField(max_length=500, blank=True, null=True)

     is_prize_claimed = models.BooleanField(default=False)

     file_field_name = "invoice"
     url_field_name = "invoice_public_url"
     path_prefix="assets/invoices"

     def __str__(self):
         return self.name 
     

class Prize(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(null=True, blank=True)  # $10 / $20 / $50 / $100 etc.
    quantity = models.PositiveIntegerField(default=0)
    quantity_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.amount} Gift Card ({self.quantity} left)"


class ConsolationPrize(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.quantity} left)"

class PrizeConfig(models.Model):
    reset_date = models.DateTimeField(null=True, blank=True)
    

class PrizeResetLog(models.Model):
    recorded_at = models.DateTimeField(auto_now_add=True)
    snapshot = models.JSONField()

    def __str__(self):
        return f"Reset Log - {self.recorded_at}"