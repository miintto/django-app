from django.db.models import F, OuterRef, Prefetch, Q, Subquery
from django.utils import timezone

from .models import Product, ProductItem


class ProductListMixin:
    def get_queryset(self):
        return (
            Product.objects.annotate(
                min_price=Subquery(
                    ProductItem.objects.filter(
                        Q(sale_start_dtm__isnull=True)
                        | Q(sale_start_dtm__lt=timezone.localtime()),
                        Q(sale_close_dtm__isnull=True)
                        | Q(sale_close_dtm__gt=timezone.localtime()),
                        product=OuterRef("pk"),
                        is_active=True,
                        sold_quantity__lt=F("item_quantity"),
                    )
                    .order_by("price")
                    .values("price")[:1]
                )
            )
            .filter(is_displayed=True)
        )


class ProductMixin:
    def get_queryset(self):
        return (
            Product.objects.prefetch_related(
                Prefetch(
                    "productitem_set",
                    queryset=ProductItem.objects.filter(is_active=True),
                    to_attr="activated_items",
                )
            )
        )
