from django.shortcuts import render_to_response
from movies.models import Movie, Recommendation, Collection


def recommendations(request):

    collection, _ = Collection.objects.get_or_create(name="Initial Collection")
    recommended_movies = Movie.objects.all().exclude(id__in=[m.id for m in collection.movies])
    context = {'movies': recommended_movies[:30]}
    return render_to_response('recommendations.html', context)

