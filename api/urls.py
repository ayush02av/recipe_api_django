from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_api_overview.as_view()),
    path('recipe/', views.recipe_api_view.as_view()),
    path('recipe/<int:pk>/', views.recipe_specific_api_view.as_view()),
    path('item/', views.recipe_item_api_view.as_view())
]
