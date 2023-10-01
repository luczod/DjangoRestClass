# from utis.recipes.factory import make_recipe
import os
from django.utils import translation
from typing import Any, Dict
from tag.models import Tag
from ..models import Recipe
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import Http404
from django.db.models.aggregates import Count
from django.views.generic import DetailView, ListView
from django.forms.models import model_to_dict
# from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from utils.pagination import make_pagination
# from django.contrib import messages


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def theory(request, *args, **kwargs):
    """  try:
         recipes = Recipe.objects.get(pk=10000)
     except ObjectDoesNotExist:
         recipes = None
     recipes = Recipe.objects.filter(
         Q(
             Q(title__icontains='da',
               id__gt=2,
               is_published=True,) |
             Q(
                 id__gt=1000
             )
         )
     )[:10] """
    # recipes = Recipe.objects.values('id', 'title', 'author__username')[:10]
    recipes = Recipe.objects.get_published()
    number_of_recipes = recipes.aggregate(number=Count('id'))

    # make other sql query
    # print(recipes[0])

    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes['number']
    }
    return render(request, 'recipes/pages/theory.html', context=context)


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        # join in tables recipe,author and category to avoid n+1
        # qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('author', 'category', 'author__profile')
        # in case many to many
        qs = qs.prefetch_related('tags')

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )

        html_language = translation.get_language()

        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
                'html_language': html_language,
            }
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context: Dict[str, Any],
                           **response_kwargs: Any):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('id')
        )
        if not qs:
            raise Http404()

        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update(
            {'title': f'{self.object_list[0].category.name} | Category'}
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(
            slug=self.kwargs.get('slug', '')).first()

        if not page_title:
            page_title = 'No recipes found'

        page_title = f'{page_title} - Tag |'

        ctx.update({
            'page_title': page_title,
        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True
        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)[:19]
        recipe_dict['updated_at'] = str(recipe.updated_at)[:19]

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri()[:22] + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)

    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


""" def search(request):
    # request query
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__contains=search_term),
        ), is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    }) """
