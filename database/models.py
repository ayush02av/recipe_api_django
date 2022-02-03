from django.db import models
from django.utils import timezone
from uuid import uuid4
from utility import path

class recipe(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    _created = models.DateTimeField(default=timezone.now, editable=False)

    recipe_name = models.CharField(max_length=255)
    recipe_ingredients = models.TextField(null=True, blank=True)
    recipe_instructions = models.TextField(null=True, blank=True)
    recipe_items = models.ManyToManyField(to="database.recipe_item", blank=True)
    recipe_photo = models.ImageField(upload_to=path.recipe_image_path, null=True)

class recipe_item(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    _created = models.DateTimeField(default=timezone.now, editable=False)

    recipe_item_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.recipe_item_name