from django.db import models


class Product(models.Model):
    name = models.CharField("상품명", max_length=100)
    is_displayed = models.BooleanField("노출 여부", default=True)
    created_dtm = models.DateTimeField(auto_now_add=True)
    updated_dtm = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_product"


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField("품목명", max_length=100)
    cost = models.PositiveBigIntegerField("원가")
    price = models.PositiveBigIntegerField("판매가")
    is_active = models.BooleanField(default=True)
    sale_start_dtm = models.DateTimeField("판매 시작일", null=True)
    sale_close_dtm = models.DateTimeField("판매 종료일", null=True)
    item_quantity = models.PositiveIntegerField("재고")
    sold_quantity = models.PositiveIntegerField("판매 수량", default=0)
    created_dtm = models.DateTimeField(auto_now_add=True)
    updated_dtm = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tb_product_item"
