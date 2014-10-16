from django.shortcuts import render_to_response
from movies.models import Movie, Library


def movie(request, movie_id):
    try:
        movie = Movie.objects.get(moviedb_id=movie_id)
    except:
        movie = None

    recommendations = Movie.objects.get_recommendations_based_on_movies(Movie.objects.filter(id=movie_id))
    context = {
        'movie': movie,
        'in_library': Library.objects.default.contains(movie),
        'watching': Library.objects.default.watchlist.contains(movie),
        'recommendations': recommendations}
    return render_to_response('movie.html', context)

