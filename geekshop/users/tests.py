from django.test import TestCase
from django.test.client import Client

from geekshop import settings
from users.models import User

# Create your tests here.


class TestMainappSmoke(TestCase):
    status_code_success = 200
    status_code_render = 302
    username = 'django'
    email = 'django@mail.ru'
    password = 'geekbrains'

    new_user_data = {
        'username': 'django1',
        'first_name': 'Django',
        'last_name': 'Django2',
        'email': 'jango1@mail.ru',
        'password1': 'geekbrains',
        'password2': 'geekbrains',
    }

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, self.status_code_render)

    def test_register(self):
        response = self.client.post('/users/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.status_code_render)

        new_user = User.objects.get(username=self.new_user_data['username'])
        # print(new_user)

        activation_url = f"{settings.DOMAIN_NAME}/users/verify/{self.new_user_data['email']}/{new_user.activation_key}/"
        # print(activation_url)
        response = self.client.get(activation_url)

        self.assertEqual(response.status_code, self.status_code_render)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def tearDown(self) -> None:
        pass
