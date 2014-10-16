from math import floor
from movies.models import Movie
from django.shortcuts import render_to_response
from django.template.loader import render_to_string


def movie_list_context(request, page_title, movies_qs):
    recommendations_qs = Movie.objects.get_recommendations_based_on_movies(movies_qs)
    context = {
        'page': page_title,
        'movies': movies_qs,
        'rendered_movies': _paginated_movies_string(request, movies_qs, recommendations_qs)}
    return context


def _paginated_movies_context(request, movies_qs):
    number_per_page = 20
    page_number = int(request.GET.get('page_number', 1))
    max_page_index = floor(movies_qs.count()/number_per_page)+1
    start_movie_index = (page_number-1)*number_per_page
    end_movie_index = page_number*number_per_page
    movies = movies_qs[start_movie_index:end_movie_index]
    recommendations_qs = Movie.objects.get_recommendations_based_on_movies(movies_qs)[:24]
    context = {'page': 'home',
               'movies': movies,
               'movie_list': movies_qs,
               'all_page_numbers': range(1, int(max_page_index)+1),
               'page_number': page_number,
               'recommendations': recommendations_qs}
    return context


def _paginated_movies(request, movies):
    return render_to_response('movies.html', _paginated_movies_context(request, movies))


def _paginated_movies_string(request, movies, recommendations_qs):
    return render_to_string('movies.html', _paginated_movies_context(request, movies))
