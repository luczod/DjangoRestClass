from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ..permissions import IsOwner
from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 2
    invalid_page_message = "not found"


""" class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination """


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["example"] = 'this is in context now'
        return context

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def get_object(self):
        pk = self.kwargs.get('pk', '')

        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )
        self.check_object_permissions(self.request, obj)

        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner(), ]

        return super().get_permissions()

    # overrite def partial_update in def patch
    def partial_update(self, request, *args, **kwargs):
        print('REQUEST: ', request.user, self.request.user)
        recipe = self.get_object()
        pk = kwargs.get('pk')
        recipe = self.get_queryset().filter(pk=pk).first()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)


""" @api_view(http_method_names=['get', 'patch', 'delete'])
def recipe_api_details(request, pk):
    recipe = Recipe.objects.filter(pk=pk).first()
    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
        )
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """
