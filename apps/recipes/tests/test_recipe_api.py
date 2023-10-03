from rest_framework import test
from recipes.tests.test_recipe_base import RecipeMixin


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def test_initial(self):
        assert 2 == 2
