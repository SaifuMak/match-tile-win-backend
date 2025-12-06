from datetime import timedelta
from django.db.models import F
from django.db import transaction
from pytz import timezone
from .models import ConsolationPrize, Prize, PrizeConfig, PrizeResetLog
from django.utils.timezone import now


def draw_prize():
    # Pick a random prize that has stock
    prize = Prize.objects.filter(quantity__gt=0).order_by("?").first()

    if not prize:
        return None

    # reduce stock safely
    prize.quantity = F("quantity") - 1
    prize.save(update_fields=["quantity"])
 
    
    return prize


def handle_consolation_prize():
    consolation_prize = ConsolationPrize.objects.first()
    if consolation_prize and consolation_prize.quantity > 0:
            consolation_prize.quantity = F("quantity") - 1
            consolation_prize.save(update_fields=["quantity"])


def reset_prizes():
        prizes = Prize.objects.all()
        consolation_prize = ConsolationPrize.objects.first()

        snapshot = {
        "timestamp": str(now()),
        "prizes": list(prizes.values("name","amount", "quantity", "quantity_limit")),
        "consolation": {
            "quantity": consolation_prize.quantity if consolation_prize else 0
            }
        }
        print("Prize Reset Snapshot:", snapshot)
        
        PrizeResetLog.objects.create(snapshot=snapshot)

        for prize in prizes:
            if prize.amount == 10:
                prize.quantity = 140
            elif prize.amount == 20:
                prize.quantity = 5
            elif prize.amount == 50:
                prize.quantity = 3
            elif prize.amount == 100:
                prize.quantity = 2
            prize.save(update_fields=["quantity"])
        
        consolation_prize = ConsolationPrize.objects.first()

        if consolation_prize:
            consolation_prize.quantity = 1000
            consolation_prize.save(update_fields=["quantity"])
        
        config = PrizeConfig.objects.first()
        config.reset_date  += timedelta(days=7) 
        config.save()


def check_and_reset_prizes():
    config = PrizeConfig.objects.first()

    if not config or not config.reset_date:
        return  # nothing to compare or reset

    if now() >= config.reset_date:
        reset_prizes()


