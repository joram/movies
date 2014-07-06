from django.shortcuts import render_to_response
from movies.models import Movie, Recommendation, Library


def recommendations(request):

    library = Library.objects.default
    recommended_movies = library.recommendations
    context = {'movies': recommended_movies[:30]}
    return render_to_response('recommendations.html', context)

