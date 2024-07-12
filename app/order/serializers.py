from rest_framework import serializers

from app.common.fields import UserFromRequestField
from app.product.mixins import Product
from .models import Order, OrderItem


class OrderItemParamSerializer(serializers.Serializer):
    item_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)


class OrderParamSerializer(serializers.ModelSerializer):
    user = UserFromRequestField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )
    items = OrderItemParamSerializer(many=True)

    class Meta:
        model = Order
        fields = ("order_number", "product_id", "user", "items")

    def create(self, validated_data):
        validated_data.pop("items")
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("id", "item_id", "price")


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
