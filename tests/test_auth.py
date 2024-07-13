import json

from django.test import TestCase

from .base import TestClient


class AuthTest(TestCase):
    client_class = TestClient

    def test_회원가입(self):
        data = {
            "email": "test-user@test.com",
            "password": "password",
            "password_check": "password",
        }
        with self.assertNumQueries(2):
            response = self.client.post(
                "/auth/register", data=json.dumps(data)
            )
        self.assertEqual(response.status_code, 200)

    def test_회원가입_비밀번호_불일치(self):
        data = {
            "email": "test-user@test.com",
            "password": "password",
            "password_check": "password123",
        }
        response = self.client.post("/auth/register", data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_로그인(self):
        self.test_회원가입()

        data = {"email": "test-user@test.com", "password": "password"}
        with self.assertNumQueries(2):
            response = self.client.post("/auth/login", data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_로그인_실패(self):
        self.test_회원가입()

        data = {"email": "test-user@test.com", "password": "1234"}
        response = self.client.post("/auth/login", data=json.dumps(data))
        self.assertEqual(response.status_code, 400)
