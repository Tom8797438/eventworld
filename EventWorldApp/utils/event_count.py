from django.db.models import Sum
from EventWorldApp.models import Ticketing

def calculate_remaining_places(event):
    total_reserved = (
        Ticketing.objects
        .filter(event=event, status__in=["valid", "used"])
        .aggregate(Sum("quantity"))["quantity__sum"] or 0
    )
    return max(event.number_place - total_reserved, 0)
