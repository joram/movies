from movies.models import Movie
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fetch_torrent_for_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if movie.fetch_torrent():
        return HttpResponse()
    return HttpResponseNotFound()