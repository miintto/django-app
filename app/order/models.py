from django.db import models, transaction

from app.auth.models import AuthUser
from app.product.models import Product, ProductItem


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = ("PENDING", "주문 대기")
        COMPLETED = ("COMPLETED", "주문 완료")
        CONFIRMED = ("CONFIRMED", "주문 확정")
        CANCELLED = ("CANCELLED", "주문 취소")

    order_number = models.CharField("주문번호", max_length=100, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(AuthUser, null=True, on_delete=models.SET_NULL)
    status = models.CharField(
        "주문 상태",
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    canceled_dtm = models.DateTimeField("주문 취소 일시", null=True)
    confirmed_dtm = models.DateTimeField("주문 확정 일시", null=True)
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_order"

    def create_items(self, items: list):
        with transaction.atomic():
            Product.objects.select_for_update().get(pk=self.product_id)
            item_map = {
                it["item_id"]: {"quantity": it["quantity"]} for it in items
            }
            for item in ProductItem.objects.filter(pk__in=item_map.keys()):
                if item.item_quantity <= item.sold_quantity:
                    raise
                item_map[item.pk]["price"] = item.price

            self.items = OrderItem.objects.bulk_create(
                [
                    OrderItem(order=self, item_id=item_id, price=data["price"])
                    for item_id, data in item_map.items()
                    for _ in range(data["quantity"])
                ]
            )

        self.status = self.OrderStatus.COMPLETED
        self.save(update_fields=["status"])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField("판매가")
    created_dtm = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_order_item"
