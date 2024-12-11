from django.test import TestCase

from PharmaQ.consultation.models import Category


class TestCategoryModel(TestCase):
    def setUp(self):

        self.data = {
            'title': 'Test Category',
            'description': 'Test Category',
        }



    def test__create_category__generate_slug_automatic__expected_slug_to_be_generated(self):

        category = Category(**self.data)
        category.save()
        category_id = category.id
        self.assertEqual(category.slug, f'test-category-{category_id}')