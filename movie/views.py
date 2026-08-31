from django.shortcuts import render
from django.http import HttpResponse

import matplotlib.pyplot as plt
import matplotlib
import io
import base64

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Nicolas'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'name': 'Nicolas Ortiz', 'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')

    # ---- Movies per year ----
    all_movies = Movie.objects.all()

    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year else "None"
        if year in movie_counts_by_year:
            movie_counts_by_year[year] += 1
        else:
            movie_counts_by_year[year] = 1

    # ordenar por año (dejando "None" al final)
    sorted_years = sorted(
        movie_counts_by_year.keys(),
        key=lambda y: (y == "None", y)
    )
    movie_counts_by_year = {y: movie_counts_by_year[y] for y in sorted_years}

    bar_width = 0.5
    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(12, 5))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic_by_year = base64.b64encode(image_png).decode('utf-8')

    # ---- Movies per genre (solo el primer genero) ----
    movie_counts_by_genre = {}
    for movie in all_movies:
        if movie.genre:
            genre = movie.genre.split(',')[0].strip()
        else:
            genre = "None"
        if genre in movie_counts_by_genre:
            movie_counts_by_genre[genre] += 1
        else:
            movie_counts_by_genre[genre] = 1

    bar_positions_genre = range(len(movie_counts_by_genre))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=bar_width, align='center', color='green')
    plt.title('Movies per genre (first only)')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    plt.close()

    image_png2 = buffer2.getvalue()
    buffer2.close()
    graphic_by_genre = base64.b64encode(image_png2).decode('utf-8')

    return render(request, 'statistics.html', {
        'graphic': graphic_by_year,
        'graphic_genre': graphic_by_genre,
    })
