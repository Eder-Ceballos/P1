from django.shortcuts import render
from django.db.models import Count
from .models import Movie
import json


def home(request):
    """Página de inicio con buscador"""
    search_term = request.GET.get('searchMovie')
    
    if search_term:
        movies = Movie.objects.filter(title__icontains=search_term)
    else:
        movies = Movie.objects.all()[:6]
        
    context = {
        'searchTerm': search_term,
        'movies': movies,
    }
    return render(request, 'movie/home.html', context)


def movies_list(request):
    """Lista TODAS las películas en Cards"""
    movies = Movie.objects.all().order_by('-year')
    context = {'movies': movies}
    return render(request, 'movie/movies_list.html', context)


def movies_by_year(request):
    """Gráfica: películas por año"""
    movies_data = (
        Movie.objects
        .values('year')
        .annotate(count=Count('id'))
        .order_by('year')
    )
    
    years = [str(item['year']) for item in movies_data]
    counts = [item['count'] for item in movies_data]
    
    context = {
        'years': json.dumps(years),
        'counts': json.dumps(counts),
    }
    return render(request, 'movie/movies_by_year.html', context)


def movies_by_genre(request):
    """Gráfica: películas por género"""
    movies_data = (
        Movie.objects
        .values('genre')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    genres = [item['genre'] for item in movies_data]
    counts = [item['count'] for item in movies_data]
    
    context = {
        'genres': json.dumps(genres),
        'counts': json.dumps(counts),
    }
    return render(request, 'movie/movies_by_genre.html', context)