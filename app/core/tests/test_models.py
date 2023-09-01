"""Tests for models"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def create_user(email='user@example.com', password='pass1234'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test successful user creation."""

        email = "test@example.com"  # example.com is reserved for testing
        password = "testpass1"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        test_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected_email in test_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='password',
            )
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email(self):
        """Raising a ValueError if an email is incorrect."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test1')

    def test_create_superuser(self):
        """Test superuser creation."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'password',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recipe(self):
        user = get_user_model().objects.create_user(
            'user@example.com',
            'pass1234',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Simple recipe',
            time_min=5,
            price=Decimal('5.50'),  # integer is ususally better
            description='Simple recipe description.',
        )

        self.assertEqual(str(recipe), recipe.title)  # str() returns the title

    def test_create_tag(self):
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    @patch('core.models.uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/recipe/{uuid}.jpg')
