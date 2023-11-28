from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from test.user.factories import user_factory


class UserProfile(APITestCase):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_url = reverse('token_obtain_pair')

    def setUp(self) -> None:
        self.password = 'testing'
        self.user = user_factory.CreateUserFactory(password=self.password)
        client = APIClient()
        response = client.post(self.login_url, {'username':self.user.username, 'password':self.password})
        self.access_token = response.data['access']
        return super().setUp()
    
    def test_view_profile(self):
        profile_url = reverse('userprofile-detail', args=[self.user.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(profile_url)
        breakpoint()