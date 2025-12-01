import random
from .models import Prize
from django.db import transaction

@transaction.atomic 
def draw_prize():
    prizes = Prize.objects.filter(quantity__gt=0)  # only available

    if not prizes.exists():
        return None  # no prizes left

    total_qty = sum(p.quantity for p in prizes)
    rand = random.randint(1, total_qty)

    # Weighted selection based on quantity
    cumulative = 0
    for prize in prizes:
        cumulative += prize.quantity
        if rand <= cumulative:
            # decrease quantity
            prize.quantity -= 1
            prize.save()
            return prize
