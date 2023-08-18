from django.test import TestCase
from .models import Profile, Avatar
from django.contrib.auth.models import User

# Create your tests here.
class AccountTestCase(TestCase):
    def setUp(self) -> None:
        self.print_info('Start setUp')
        self.user = User.objects.create_user(username='username', password='password')
        avatar = Avatar.objects.create()
        self.profile = Profile.objects.create(user=self.user, fullName='name', avatar=avatar)
        self.print_info('Finish setUp')

    def test_user_creation(self):
        # Проверка создания объекта User
        self.print_info('Start test_user_creation')
        self.assertEqual(self.user.get_username, 'username')
        self.assertEqual(self.user.password, 'password')
        self.print_info('Finish test_movie_creation')

    