from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.common.fields import UserFromRequestField
from app.product.mixins import Product
from .models import Order, OrderItem


class OrderItemParamSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("`quantity` must be bigger than zero.")
        return value


class OrderParamSerializer(serializers.ModelSerializer):
    user = UserFromRequestField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )
    items = OrderItemParamSerializer(many=True)

    class Meta:
        model = Order
        fields = ("order_number", "product_id", "user", "items")

    def validate_items(self, value):
        if len(value) == 0:
            raise ValidationError(
                "The `items` list must contain at least one item."
            )
        return value

    def create(self, validated_data) -> Order:
        items = validated_data.pop("items")
        order = super().create(validated_data)

        order.items = order.create_items(items)
        order.status = Order.OrderStatus.COMPLETED
        order.save(update_fields=["status"])
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("pk", "item_id", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "pk",
            "order_number",
            "status",
            "product_id",
            "canceled_dtm",
            "confirmed_dtm",
            "created_dtm",
            "items",
        )
