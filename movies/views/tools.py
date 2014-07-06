import os, json

from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from common.models import Image
from movies.models import Movie, Library, Recommendation


def _files_in_dir(path, file_types=['.avi', '.mp4'], ignore_paths=[]):
    files = []
    for f in os.listdir(path):

        # collect files
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            fileName, fileExtension = os.path.splitext(full_path)
            if fileExtension.lower() in file_types:
                files.append(full_path)

        # recurse into sub folders
        if os.path.isdir(full_path) and full_path not in ignore_paths:
            files.extend(_files_in_dir(full_path))

    return files


def rebuild(request):
    Movie.objects.all().delete()
    for image in Image.objects.all():
        image.delete()
    Library.objects.all().delete()
    return rescan(request)


def rescan(request):
    library = Library.objects.default
    files = _files_in_dir(settings.MOVIE_ROOT, ignore_paths=[os.path.join(settings.MOVIE_ROOT, "Backup")])
    context = {'page': 'tools',
               'filenames': files,
               'library': library}
    return render_to_response('tools/rebuild.html', context)


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
