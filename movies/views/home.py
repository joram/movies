from math import floor
from django.shortcuts import render_to_response
from movies.models import Movie, Genre, Collection


def _nav_bar(context):
    collection, _ = Collection.objects.get_or_create(name="Initial Collection")
    context.update({
        'movie_count': collection.movies.count(),
        'genre_count': Genre.objects.all().count()})
    return context


def home(request):
    collection, _ = Collection.objects.get_or_create(name="Initial Collection")
    return _paginated_movies(request, collection.movies)


def _paginated_movies(request, movies):
    number_per_page = 20
    page_number = int(request.GET.get('page_number', 1))
    max_page_index = floor(movies.count()/number_per_page)+1
    start_movie_index = (page_number-1)*number_per_page
    end_movie_index = page_number*number_per_page
    movies = list(movies)[start_movie_index:end_movie_index]
    context = {'page': 'home',
               'movies': movies,
               'all_page_numbers': range(1, int(max_page_index)+1),
               'page_number': page_number}
    context = _nav_bar(context)
    return render_to_response('movies.html', context)


