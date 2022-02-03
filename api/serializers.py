from pyrsistent import field
from rest_framework import serializers
from database import models

class recipe_item_serializer(serializers.ModelSerializer):
    class Meta():
        model = models.recipe_item
        fields = ('recipe_item_name',)

class recipe_with_items_serializer(serializers.ModelSerializer):
    recipe_items = recipe_item_serializer(many=True)
    class Meta():
        model = models.recipe
        fields = '__all__'

class recipe_serializer(serializers.ModelSerializer):
    class Meta():
        model = models.recipe
        fields = '__all__'