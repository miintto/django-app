from django.db.models import Prefetch

from .models import Order, OrderItem


class OrderMixin:
    def get_queryset(self):
        return (
            Order.objects.select_related("user", "product")
            .prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("item"),
                    to_attr="items",
                )
            )
        )
