from django.urls import reverse, resolve
from recipes.views import site
from .test_recipe_base import RecipeTestBase


# Create your tests here.
# == assert check value
# is assertIs checek memory ref value
# in test django use temp database


class RecipeCategoryViewsTest(RecipeTestBase):
    def test_recipe_category_template_loads_recipes(self):
        need_title = 'this is a category test'
        # Need a recipe only for this test
        self.make_recipe(title=need_title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')  # html in string

        self.assertIn(need_title, content)

    def test_recipe_category_class_view(self):
        view = resolve(reverse('recipes:category', kwargs={'id': 1000}))
        self.assertIs(view.func.view_class, site.RecipeListViewCategory)

    def test_recipe_category_view_code_404_if_not_category(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'id': 10}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False dont show"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)
