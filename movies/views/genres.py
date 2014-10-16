from django.shortcuts import render_to_response
from movies.models import Genre, Library
from _helpers import movie_list_context


def genres(request):
    library = Library.objects.default
    genres_list = []
    for genre in library.genres:
        genre.movie = library.random_movie(genre=genre)
        genres_list.append(genre)

    context = {'page': 'genres',
               'genres': genres_list}

    return render_to_response('genres.html', context)


def genre(request, genre_id):
    genre = Genre.objects.get(moviedb_id=genre_id)
    movies_qs = Library.objects.default.movies.filter(genres=genre)
    context = movie_list_context(request, "genres", movies_qs)
    context['genre'] = genre
    return render_to_response('genre.html', context)