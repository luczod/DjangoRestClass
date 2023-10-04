from rest_framework import test
from django.urls import reverse
from unittest.mock import patch
from recipes.tests.test_recipe_base import RecipeAPIMixin


class RecipeAPIv2Test(test.APITestCase, RecipeAPIMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.get_recipe_api_list()
        self.assertEqual(
            response.status_code,
            200
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=8)
    def test_recipe_api_number_of_recipes_per_page(self):
        number_recipes = 8
        self.make_recipe_in_batch(qtd=number_recipes)
        response = self.client.get(
            reverse('recipes:recipes-api-list') + '?page=1')
        qtd_recipes_response = len(response.data.get('results'))
        self.assertEqual(
            number_recipes,
            qtd_recipes_response
        )

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        response = self.get_recipe_api_list()
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # Creates categories
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')

        # Creates 10 recipes
        recipes = self.make_recipe_in_batch(qtd=10)

        # Change all recipes to the wanted category
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # Change one recipe to the NOT wanted category
        # As a result, this recipe should NOT show in the page
        recipes[0].category = category_not_wanted
        recipes[0].save()

        # Action: get recipes by wanted category_id
        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.get_recipe_api_list(reverse_result=api_url)

        # We should only see recipes from the wanted category
        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_check_jwt_token_to_create_recipe(self):
        api_url = self.get_recipe_reverse_url()
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code,
            401
        )

    def test_recipe_api_list_logged_user_create_a_recipe(self):
        data = self.get_recipe_raw_data()
        print(data)
        response = self.client.post(
            self.get_recipe_reverse_url(),
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_access_token()}'
        )
        # print(response.data)

        self.assertEqual(
            response.status_code,
            201
        )
