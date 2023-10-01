from django.urls import reverse
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


# Create your tests here.
# == assert check value
# is assertIs checek memory ref value
# in test django use temp database


class RecipeHomeViewsPages(RecipeTestBase):

    def test_recipe_home_is_paginated(self):
        for i in range(18):
            kwargs = {'slug': f'slug-TESTE{i}',
                      'author_data': {'username': f'author{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=6):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 6)
            self.assertEqual(len(paginator.get_page(2)), 6)
            self.assertEqual(len(paginator.get_page(3)), 6)
