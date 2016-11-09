from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.movies.models import Library, Movie, Watchlist
from _helpers import _paginated_movies


def watchlist(request):
    watch_list = Library.objects.default.watchlist
    return _paginated_movies(request, watch_list.movies)


@csrf_exempt
def add_to_watchlist(request, watchlist_id, movie_id):
    movie, _ = Movie.objects.create_from_moviedb_id(movie_id)
    watchlist = Library.objects.default.watchlist
    watchlist.add_movie(movie)
    return HttpResponse()
