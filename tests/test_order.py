import json

from django.test import TestCase

from app.auth.models import AuthUser
from app.product.models import Product, ProductItem
from .base import TestClient


class OrderTest(TestCase):
    client_class = TestClient

    def setUp(self):
        super().setUp()
        product = Product.objects.create(name="상품")
        item1 = ProductItem.objects.create(
            product=product,
            name="아이템1",
            cost=10000,
            price=8900,
            item_quantity=100,
        )
        item2 = ProductItem.objects.create(
            product=product,
            name="아이템2",
            cost=25000,
            price=19900,
            item_quantity=100,
        )
        self.user = AuthUser.objects.create(email="test@test.com")
        self.product = product
        self.item1 = item1
        self.item2 = item2

    def test_주문(self):
        """
        Query 리스트
            1. SELECT 1 FROM tb_order WHERE order_number = {order_number} LIMIT 1
            2. SELECT * FROM tb_product WHERE id = {product_id}
            3. SELECT * FROM tb_auth_user WHERE id = {user_id}
            4. INSERT INTO tb_order ( ... )
            5. SAVEPOINT "s8497511104_x8"
            6. SELECT * FROM tb_product WHERE id = {product_id} FOR UPDATE
            7. SELECT * FROM tb_product_item WHERE id IN ( ... )
            8. INSERT INTO tb_order_item ( ... ) RETURNING id
            9. RELEASE SAVEPOINT "s8497511104_x8"
            10. UPDATE tb_order SET status = 'COMPLETED' WHERE id = {order_id}
        """
        self.client.force_login(self.user)

        payload = {
            "order_number": "test",
            "product_id": self.product.pk,
            "items": [
                {"item_id": self.item1.pk, "quantity": 3},
                {"item_id": self.item2.pk, "quantity": 2},
            ],
        }
        with self.assertNumQueries(10):
            response = self.client.post("/orders", data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        return response.json()

    def test_재고_없이_주문시_실패(self):
        self.client.force_login(self.user)

        payload = {
            "order_number": "test",
            "product_id": self.product.pk,
            "items": [
                {"item_id": self.item1.pk, "quantity": 0},
                {"item_id": self.item2.pk, "quantity": 1},
            ],
        }
        response = self.client.post("/orders", data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_품목_없이_주문시_실패(self):
        self.client.force_login(self.user)

        payload = {
            "order_number": "test", "product_id": self.product.pk, "items": []
        }
        response = self.client.post("/orders", data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_동일한_주문번호로_주문시_실패(self):
        self.client.force_login(self.user)
        order = self.test_주문()

        payload = {
            "order_number": order["order_number"],
            "product_id": self.product.pk,
            "items": [
                {"item_id": self.item1.pk, "quantity": 1},
                {"item_id": self.item2.pk, "quantity": 1},
            ],
        }
        response = self.client.post("/orders", data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)

    def test_주문_조회(self):
        order = self.test_주문()

        with self.assertNumQueries(2):
            response = self.client.get(f"/orders/{order["pk"]}")
        self.assertEqual(response.status_code, 200)
