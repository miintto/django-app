from django.test import TestCase

from app.product.models import Product, ProductItem
from .base import TestClient


class ProductTest(TestCase):
    client_class = TestClient

    def setUp(self):
        super().setUp()
        product = Product.objects.create(name="상품1")
        Product.objects.create(name="상품2")
        Product.objects.create(name="상품3")
        Product.objects.create(name="상품4")
        ProductItem.objects.bulk_create(
            [
                ProductItem(
                    product=product,
                    name="아이템1",
                    cost=10000,
                    price=8900,
                    item_quantity=100,
                ),
                ProductItem(
                    product=product,
                    name="아이템2",
                    cost=20000,
                    price=14900,
                    item_quantity=100,
                ),
                ProductItem(
                    product=product,
                    name="아이템3",
                    cost=28000,
                    price=15900,
                    item_quantity=100,
                ),
                ProductItem(
                    product=product,
                    name="아이템4",
                    cost=35000,
                    price=18900,
                    item_quantity=100,
                ),
            ]
        )
        self.product = product

    def test_상품_리스트_조회(self):
        with self.assertNumQueries(1):
            response = self.client.get(f"/products")
        self.assertEqual(response.status_code, 200)

    def test_상품_조회(self):
        with self.assertNumQueries(2):
            response = self.client.get(f"/products/{self.product.pk}")
        self.assertEqual(response.status_code, 200)

    def test_존재하지_않는_상품_조회(self):
        response = self.client.get(f"/products/{self.product.pk + 999}")
        self.assertEqual(response.status_code, 404)
