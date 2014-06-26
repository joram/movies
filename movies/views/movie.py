from django.shortcuts import render_to_response
from movies.models import Movie


def movie(request, movie_id):
    movie = Movie.objects.get(moviedb_id=movie_id)
    context = {'movie': movie}
    return render_to_response('movie.html', context)

