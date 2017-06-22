from django.shortcuts import render_to_response, get_object_or_404
from apps.movies.models import Movie, Library


def movie(request, movie_id):
    movie = get_object_or_404(Movie, moviedb_id=movie_id)
    recommendations = Movie.objects.get_recommendations_based_on_movies(Movie.objects.filter(id=movie.id))
    context = {
        'movie': movie,
        'in_library': Library.objects.default.contains(movie),
        'watching': Library.objects.default.watchlist.contains(movie),
        'recommendations': recommendations}
    return render_to_response('movie.html', context)

