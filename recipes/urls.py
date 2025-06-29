from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.home, name="home-workout"),
    path('category/<int:category_id>/', views.category, name="category"),
    path('cards/<int:id>/', views.card_training, name="card-training"),
    path('recipes/search/', views.search, name='search')
]
