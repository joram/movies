import random
from django.shortcuts import render_to_response
from movies.models import Genre, Movie


def genres(request):
    genres = Genre.objects.all()
    for genre in genres:
        movies = Movie.objects.filter(genres=genre)
        if movies:
            movie = random.choice(movies)
            while not movie.poster and movies.count() > 1:
                print "no image for %s" % movie
                movies = movies.exclude(id=movie.id)
                movie = random.choice(movies)
            genre.movie = movie

    context = {'page': 'genres',
               'genres': genres}

    return render_to_response('genres.html', context)


def genre(request, genre_id):
    genre = Genre.objects.get(moviedb_id=genre_id)
    movies = Movie.objects.filter(genres=genre)

    context = {
        'page': 'genres',
        'genre': genre,
        'movies': movies}

    return render_to_response('genre.html', context)