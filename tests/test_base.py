from django.test import TestCase
from users.models import User

class TestBase(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def create_user(self):
        user = User.objects.create(username='test', email='test@test.com')
        user.set_password('1234')
        user.save()
        return user

    def login(self):
        user_logged = self.client.login(email='test@test.com', password='1234')
        return user_logged