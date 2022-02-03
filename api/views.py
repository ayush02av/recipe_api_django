from sqlite3 import apilevel
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

from database import models
from . import serializers

class recipe_api_overview(APIView):

    def get(self, request):

        overview_content = [
            {
                'endpoint' : 'recipe/',
                'methods allowed' : [
                    'GET',
                    'POST'
                ],
                'GET Method' : {
                    'GET recipe' : 'get all recipes',
                    'GET recipe?recipe=<str:recipe_name>' : 'get all recipes with recipe name search filter',
                    'GET recipe?ingredients=<str:recipe_ingredients>' : 'get all recipes with recipe ingredients search filter',
                    'GET recipe?instructions=<str:recipe_instructions>' : 'get all recipes with recipe instructions search filter',
                },
                'POST Method' : {
                    'POST recipe/' : 'create a new recipe'
                }
            },
            {
                'endpoint' : 'recipe/<int:recipe_id>',
                'methods allowed' : [
                    'GET',
                    'PUT',
                    'DELETE'
                ],
                'GET Method' : {
                    'GET recipe/<int:recipe_id>' : 'get recipe of given recipe id',
                },
                'PUT Method' : {
                    'PUT recipe/<int:recipe_id>' : 'update recipe of given recipe id'
                },
                'DELETE Method' : {
                    'DELETE recipe/<int:recipe_id>' : 'delete recipe of given recipe id'
                }
            },
            {
                'endpoint' : 'item/',
                'methods allowed' : [
                    'GET',
                    'POST'
                ],
                'GET Method' : {
                    'GET item' : 'get all recipe item',
                },
                'POST Method' : {
                    'POST item/' : 'create a new recipe item'
                }
            },
        ]
        
        return Response(overview_content)

class recipe_api_view(APIView):
    serializer_class = serializers.recipe_serializer

    def get(self, request):
        serializer = serializers.recipe_with_items_serializer

        try:
            queryset = models.recipe.objects.all()

            if 'recipe' in request.GET:
                queryset = models.recipe.objects.filter(recipe_name__icontains=request.GET['recipe'])

            if 'ingredients' in request.GET:
                queryset = models.recipe.objects.filter(recipe_ingredients__icontains=request.GET['ingredients'])
            
            if 'instructions' in request.GET:
                queryset = models.recipe.objects.filter(recipe_instructions__icontains=request.GET['instructions'])

            queryset = queryset.order_by('-_created')
            
            serializer = serializer(queryset, many=True)
            return Response(serializer.data)
            
        except:
            return HttpResponse(status=500, content=b'Internal Server Error')

    def post(self, request):
        serializer = self.serializer_class

        try:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        except:
            return HttpResponse(status=500, content=b'Internal Server Error')

class recipe_specific_api_view(APIView):
    serializer_class = serializers.recipe_serializer

    def get(self, request, pk):
        serializer = serializers.recipe_with_items_serializer

        try:
            queryset = models.recipe.objects.get(_id=pk)
            serializer = serializer(queryset, many=False)
            return Response(serializer.data)
            
        except models.recipe.DoesNotExist:
            return HttpResponse(status=404, content=b'Recipe with this id does not exist')
            
        except Exception as exception:
            return HttpResponse(status=500, content=b'Internal Server Error')
    
    def put(self, request, pk, format=None):
        serializer = self.serializer_class

        try:
            queryset = models.recipe.objects.get(_id=pk)
            serializer = serializer(queryset, data=request.data)

            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
            
        except models.recipe.DoesNotExist:
            return HttpResponse(status=404, content=b'Recipe with this id does not exist')

        except Exception as exception:
            return HttpResponse(status=500, content=b'Internal Server Error')
    
    def delete(self, request, pk):

        try:
            queryset = models.recipe.objects.get(_id=pk)
            queryset.delete()
            return HttpResponse(status=200, content=b'Recipe deleted')

        except models.recipe.DoesNotExist:
            return HttpResponse(status=404, content=b'Recipe with this id does not exist')
            
        except Exception as exception:
            return HttpResponse(status=500, content=b'Internal Server Error')

class recipe_item_api_view(APIView):
    serializer_class = serializers.recipe_item_serializer

    def get(self, request):
        serializer = self.serializer_class

        try:
            queryset = models.recipe_item.objects.all()

            queryset = queryset.order_by('-_created')
            
            serializer = serializer(queryset, many=True)
            return Response(serializer.data)
            
        except:
            return HttpResponse(status=500, content=b'Internal Server Error')

    def post(self, request):
        serializer = self.serializer_class

        try:
            serializer = serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        except:
            return HttpResponse(status=500, content=b'Internal Server Error')