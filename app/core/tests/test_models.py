"""
Test for Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):
    """Test Models"""

    def test_create_user_with_email(self):
        """Verify success create user with an email"""

        email = "test@example.com"
        password = "@Test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_normalized_email(self):
        """Verify success create user with a normalized email"""
        sample_emails = [
            ["test1@MAIL.COM", "test1@mail.com"],
            ["Test2@Mail.com", "Test2@mail.com"],
            ["TEST3@MAIL.COM", "TEST3@mail.com"],
            ["test4@mail.COM", "test4@mail.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_create_user_without_email(self):
        """Verify failed create user without email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Verify success create superuser"""
        user = get_user_model().objects.create_superuser(
            "superuser@example.com", "@Superuser123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
