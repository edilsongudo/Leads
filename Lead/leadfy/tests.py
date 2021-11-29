from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.db import IntegrityError

User = get_user_model()
c = Client()

class UserTestCast(TestCase):

    def setUp(self):
        user_a = User.objects.create(
            username='cfe',
            email='cfe@invalid.com',
            password='some_123_password')
        self.user_a = user_a
        user_b = User.objects.create(
            username='cfe2',
            email='cfe2@invalid.com',
            password='some_123_password')
        self.user_b = user_b

    def test_user_exists(self):
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 2)
        self.assertNotEqual(user_count, 0)

    def test_username_is_lowercase(self):
        username = 'CRIstiano'
        username_lower = username.lower()
        User.objects.create(username=username,
                            email='cristiano@cristianoronaldo.com',
                            password='cristiano123')
        user1 = User.objects.filter(username=username_lower).count()
        user2 = User.objects.filter(username=username).count()
        self.assertEqual(user1, 1)
        self.assertEqual(user2, 0)

    def test_unique_username_with_different_cases(self):
        with self.assertRaises(IntegrityError):
            self.user_b.username = self.user_a.username.upper()
            self.user_b.save()

    def test_login_url(self):
        login_url = '/accounts/login/'
        data = {"username": "cfe", "password": "some_123_password"}
        response = self.client.post(login_url, data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_url(self):
        signup_url = '/accounts/signup/'
        data = {"username": "cfe", "password": "some_123_password"}
        response = self.client.post(signup_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
