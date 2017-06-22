
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from apps.movies.models import Movie, Library, Recommendation

from helpers import movie_files
from rebuild import rebuild_actions, rebuild
from recommend import get_single_recommendation, get_recommendation_list, get_recommendations_for_movie


def rebuild_recommendations(request):
    Recommendation.objects.all().delete()
    library = Library.objects.default
    recommended_movies = Movie.objects.all().exclude(id__in=[m.id for m in library.movies])
    recommended_movies.delete()

    context = {'page': 'tools',
               'movies': library.movies.order_by('name'),
               'library': library}
    return render_to_response('tools/rebuild_recommendations.html', context)


@csrf_exempt
def add_movie(request):
    library = Library.objects.default
    filename = request.POST.get('filename')
    movie, created = Movie.objects.get_or_create_from_filepath(filename)
    if movie:
        library.add_movie(movie)
    context = {'movie': movie}
    response = render_to_response('tools/add_movie.html', context)
    return response
