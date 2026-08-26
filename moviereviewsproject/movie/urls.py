from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movies_list, name='movies'),
    path('movies-by-year/', views.movies_by_year, name='movies_by_year'),
    path('movies-by-genre/', views.movies_by_genre, name='movies_by_genre'),
]

