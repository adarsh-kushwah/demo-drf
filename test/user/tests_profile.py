from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status

from test.user.factories import user_factory

from user.models import UserProfile


class UserProfileTest(APITestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_url = reverse("user:token_obtain_pair")

    def setUp(self) -> None:
        self.password = "testing"
        self.user = user_factory.CreateUserFactory(password=self.password)
        self.profile_url = reverse("user:userprofile-detail", args=[self.user.id])
        response = self.client.post(
            self.login_url, {"username": self.user.username, "password": self.password}
        )
        self.access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        return super().setUp()

    def test_view_profile(self):
        response = self.client.get(self.profile_url)
        # self.assertIn('username', response.data.keys())
        try:
            user_address = self.user.useraddress
        except:
            user_address = None
        user_dict = {
            "id": self.user.id,
            "username": self.user.username,
            "useraddress": user_address,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            "user_type": self.user.user_type,
            "gender": self.user.gender,
            "phone_number": self.user.phone_number,
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertDictEqual(response.data, user_dict)

    def test_update_profile(self):
        updata_data = {"first_name": "Testing", "phone_number": "1111111111"}
        response = self.client.patch(self.profile_url, data=updata_data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "user updated successfully")
        self.assertEqual(updata_data["first_name"], self.user.first_name)
        self.assertEqual(updata_data["phone_number"], self.user.phone_number)

    def test_delete_profile(self):
        total_profiles_before_delete = UserProfile.objects.all().count()
        response = self.client.delete(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "user deleted successfully")
        total_profiles_after_delete = UserProfile.objects.all().count()
        self.assertEqual(total_profiles_after_delete, total_profiles_before_delete - 1)
