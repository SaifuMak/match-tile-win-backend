from django.db.models import F
from django.db import transaction
from .models import Prize


def draw_prize():
    # Pick a random prize that has stock
    prize = Prize.objects.filter(quantity__gt=0).order_by("?").first()

    if not prize:
        return None

    # reduce stock safely
    prize.quantity = F("quantity") - 1
    prize.save(update_fields=["quantity"])
    print("Prize drawn without refresh:", prize)
    # prize.refresh_from_db()
    print("Prize drawn with refresh:", prize)
    print("Prize amount:", prize.amount)
    
    return prize
