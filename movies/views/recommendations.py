from django.shortcuts import render_to_response
from movies.models import Movie, Recommendation


def recommendations(request):
    movies = Movie.objects.get_recommendations_based_on_movies(Movie.objects.all())
    movies = movies[:30]
    for rec in movies:
        movie = rec['movie']
        Movie.objects.get_poster(movie, "w342")

    context = {'movies': movies}
    return render_to_response('recommendations.html', context)

