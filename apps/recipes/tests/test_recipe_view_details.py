from django.urls import reverse, resolve
from recipes.views import site
from .test_recipe_base import RecipeTestBase


# Create your tests here.
# == assert check value
# is assertIs checek memory ref value
# in test django use temp database


class RecipeDetailsViewsTest(RecipeTestBase):
    def test_recipe_details_class_view(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, site.RecipeDetail)

    def test_recipe_details_view_code_404_if_not_recipe(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_details_template_loads_recipes(self):
        need_title = 'this is a detail page - it load one recipe'
        # Need a recipe only for this test
        self.make_recipe(title=need_title)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        content = response.content.decode('utf-8')  # html in string

        self.assertIn(need_title, content)

    def test_recipe_details_not_load_template_recipe_not_published(self):
        """ DocStrig show in test and in documentation tools """
        # Need a recipe only for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.id}))
        self.assertEqual(response.status_code, 404)
        pass

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
