from unittest.mock import patch
from django.urls import reverse, resolve
from recipes.views import site
from .test_recipe_base import RecipeTestBase
# from unittest import skip

# Create your tests here.
# == assert check value
# is assertIs checek memory ref value
# in test django use temp database


class RecipeHomeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, site.RecipeListViewHome)

    def test_recipe_home_view_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # @skip('WIP -> WORK IN PROGRESS')
    def test_recipe_home_template_if_not_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1 styles="text-align: center">No recipes found here</h1>',
            response.content.decode('utf-8')
        )
        # tenho que escrever mais
        # self.fail('para que eu termine de digitar')

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe only for this test
        self.make_recipe(preparation_time=5)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')  # html in string
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)
        pass

    def test_recipe_home_not_load_template_recipe_if_not_published(self):
        """ DocStrig show in test and in documentation tools """
        # Need a recipe only for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']

        self.assertEqual(len(response_context_recipes), 0)
        pass

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )
