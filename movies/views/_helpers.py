from math import floor
from django.shortcuts import render_to_response
from django.template.loader import render_to_string


def _paginated_movies_context(request, movie_list):
    number_per_page = 20
    page_number = int(request.GET.get('page_number', 1))
    max_page_index = floor(movie_list.movies.count()/number_per_page)+1
    start_movie_index = (page_number-1)*number_per_page
    end_movie_index = page_number*number_per_page
    movies = list(movie_list.movies)[start_movie_index:end_movie_index]
    context = {'page': 'home',
               'movies': movies,
               'movie_list': movie_list,
               'all_page_numbers': range(1, int(max_page_index)+1),
               'page_number': page_number,
               'recommendations': movie_list.recommendations}
    return context


def _paginated_movies(request, movies):
    return render_to_response('movies.html', _paginated_movies_context(request, movies))


def _paginated_movies_string(request, movies):
    return render_to_string('movies.html', _paginated_movies_context(request, movies))
