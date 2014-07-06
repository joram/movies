from django.shortcuts import render_to_response
from movies.models import Genre, Library
from _helpers import _paginated_movies_string


def genres(request):
    library = Library.objects.default
    genres_list = []
    for genre in library.genres:
        genre.movie = library.genre_movie_list(genre).random_movie()
        genres_list.append(genre)

    context = {'page': 'genres',
               'genres': genres_list}

    return render_to_response('genres.html', context)


def genre(request, genre_id):
    genre = Genre.objects.get(moviedb_id=genre_id)
    genre_library = Library.objects.default.genre_movie_list(genre)
    context = {
        'page': 'genres',
        'genre': genre,
        'movies': genre_library.movies,
        'rendered_movies': _paginated_movies_string(request, genre_library)}
    return render_to_response('genre.html', context)