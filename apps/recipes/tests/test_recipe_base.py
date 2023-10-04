from django.test import TestCase
from django.urls import reverse
from recipes.models import Category, Recipe, User

# Create your tests here.
# == assert check value
# is assertIs checek memory ref value
# in test django use temp database


class RecipeMixin:
    # Mixin pattern
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            # desempacotamento **category_data the same is {...rest}
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
            cover="recipes/covers/2023/07/28/paradoxa.jpeg"
        )

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {'title': f'Recipe Title {i}',
                      'slug': f'r{i}',
                      'author_data': {'username': f'u{i}'}}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeAPIMixin(RecipeMixin):
    def get_recipe_reverse_url(self, reverse_result=None):
        api_url = reverse_result or reverse('recipes:recipes-api-list')
        return api_url

    def get_recipe_api_list(self, reverse_result=None):
        api_url = self.get_recipe_reverse_url(reverse_result)
        response = self.client.get(api_url)
        return response

    def get_jwt_access_login(self):
        userData = {
            'username': 'TesteUser',
            'password': 'TestePassword'
        }
        self.make_author(
            username=userData.get('username'),
            password=userData.get('password')
        )

        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userData})

        return response.data.get('access')


class RecipeTestBase(TestCase, RecipeMixin):
    # Template method pattern
    def setUp(self) -> None:
        return super().setUp()
