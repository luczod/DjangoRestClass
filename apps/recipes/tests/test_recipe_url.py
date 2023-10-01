from django.test import TestCase
from django.urls import reverse


# Create your tests here.
# == assert check value
# is assertIs checek memory ref value


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse('recipes:category', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_details_url_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/1/')

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')

# RED - GREEN - REFACTOR
