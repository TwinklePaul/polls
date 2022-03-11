from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test",
            email="test@test.com",
            password="testpass123"
        )

        self.assertEqual(user.username, "test")
        self.assertEqual(user.email, "test@test.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            username="testsuper",
            email="testsuper@test.com",
            password="testpass123"
        )

        self.assertEqual(user.username, "testsuper")
        self.assertEqual(user.email, "testsuper@test.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
