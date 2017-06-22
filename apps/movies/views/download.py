from apps.movies.models import Movie
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fetch_torrent_for_movie(request, moviedb_id):
    movie, _ = Movie.objects.create_from_moviedb_id(moviedb_id=moviedb_id)
    torrent = movie.fetch_torrent()
    if torrent:
        return HttpResponse()
    return HttpResponseNotFound()
