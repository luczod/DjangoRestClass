import os
import string
from PIL import Image
from tag.models import Tag
from random import SystemRandom
from django.conf import settings
from django.db import models
from django.urls import reverse
from collections import defaultdict
from django.utils.text import slugify
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


from django.db.models import F,  Value
from django.db.models.functions import Concat

# Create your models here.
# python manage.py makemigrations
# python manage.py migrate
# srt(recipes.query)


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:  # __ __ call thunder
        return self.name


class RecipeManager(models.Manager):
    # add new personal function to the objects
    def get_published(self):
        return self.filter(
            is_published=True
        ).annotate(
            author_full_name=Concat(
                F('author__first_name'), Value(' '),
                F('author__last_name'), Value(' ('),
                F('author__username'), Value(')'),
            )
        ).order_by('-id')\
            .select_related('category', 'author')\
            .prefetch_related('tags')


class Recipe(models.Model):
    # add new personal objects Manager to class
    objects = RecipeManager()
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # add datatime to update
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')  # noqa: E501 path to images dir
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width <= new_width:
            image_pillow.close()
            return

        new_height = round((new_width * original_width) / original_height)
        # shrinking the image and maintaining the aspect ratio
        new_image = image_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):
        # call pre-save
        if not self.slug:
            rand_letters = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...

        return saved
    # call post-save

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)


# EDITED
# category (Relação)
# Author (Relação)
