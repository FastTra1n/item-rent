from .models import Item


def item_context(request):
    return {
        "site_name": "Rently",
        "items_count": Item.objects.count(),
    }
