from urllib import quote, unquote

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from movies.models import Movie, Library, Recommendation
from helpers import movie_files


@csrf_exempt
def get_recommendations_for_movie(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    filepath = unquote(request.POST.get('path'))
    max_recommendations = int(request.POST.get('max_recommendations'))
    if not max_recommendations or not filepath or filepath not in movie_files():
        return HttpResponseBadRequest()

    movie, created = Movie.objects.get_or_create_from_filepath(filepath)
    recommendations = movie.get_recommendation_list()
    max_len = min(len(recommendations), max_recommendations)
    for recommendation in recommendations[:max_len]:
        recommended_movie, created = Movie.objects.create_from_moviedb_id(moviedb_id=recommendation.get("id"))
        Recommendation.objects.create_from_moviedb_info(movie, recommended_movie, recommendation)

    return HttpResponse()

@csrf_exempt
def get_recommendation_list(request):
    movie_id = request.POST.get('movie_id')
    movie = Movie.objects.get(id=movie_id)
    context = {'recommendations': [r['id'] for r in movie.get_recommendation_list()]}
    response = render_to_response('tools/recommendation_list.html', context)
    return response


@csrf_exempt
def get_single_recommendation(request):
    library = Library.objects.default
    movie_id = request.POST['movie_id']
    recommended_id = request.POST['recommended_id']
    movie = Recommendation.objects.create_from_id(movie_id, recommended_id)
    have = False
    if movie:
        if movie in library.movies:
            have = True

    context = {'have': have}
    response = render_to_response('tools/get_single_recommendation.html', context)
    return response