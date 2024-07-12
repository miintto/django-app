from rest_framework import serializers

from .models import Product, ProductItem


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("pk", "name", "price", "is_active")

    def get_price(self, obj):
        return obj.min_price

    def get_is_active(self, obj):
        return obj.min_price is not None


class ProductItemSerializer(serializers.ModelSerializer):
    discount = serializers.SerializerMethodField()

    class Meta:
        model = ProductItem
        fields = (
            "pk",
            "name",
            "cost",
            "price",
            "discount",
            "item_quantity",
            "sold_quantity",
        )

    def get_discount(self, obj):
        try:
            return 100 - int(obj.price * 100 / obj.cost)
        except ZeroDivisionError:
            return 0


class ProductDetailSerializer(serializers.ModelSerializer):
    items = ProductItemSerializer(source="activated_items", many=True)

    class Meta:
        model = Product
        fields = ("pk", "name", "items")

