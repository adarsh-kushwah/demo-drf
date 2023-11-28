import io

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework_jwt import utils
from rest_framework.parsers import JSONParser

from user.models import UserProfile

from test.user.factories import user_factory


class UserLogin(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = reverse("user:token_obtain_pair")

    def setUp(self) -> None:
        self.password = "testing"
        self.user = user_factory.CreateUserFactory(password=self.password)
        return super().setUp()

    def test_login_using_valid_credentials(self):
        client = APIClient()
        response = client.post(
            self.url, {"username": self.user.username, "password": self.password}
        )
        decoded_payload = utils.jwt_decode_handler(response.data["access"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(decoded_payload["user_id"], self.user.id)

    def test_login_using_invalid_credentials(self):
        response = self.client.post(
            self.url, {"username": self.user.username, "password": "Invalid password"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_blank_username(self):
        response = self.client.post(self.url, {"password": "Invalid password"})
        # response.data['username'][0].title()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        data["username"]
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["username"][0], "This field is required.")

    def test_login_blank_password(self):
        response = self.client.post(self.url, {"username": self.user.username})
        # response.data['password'][0].title()
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["password"][0], "This field is required.")

    def test_login_blank_username_password(self):
        response = self.client.post(self.url, {})
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["username"][0], "This field is required.")
        self.assertEqual(data["password"][0], "This field is required.")
