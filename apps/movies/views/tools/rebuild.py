import os, json
from urllib import quote, unquote

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from common.models import Image
from apps.movies.models import Movie, Library
from helpers import movie_files


def _rescan(request):
    library = Library.objects.default
    files = movie_files()  # _files_in_dir(settings.MOVIE_ROOT, ignore_paths=[os.path.join(settings.MOVIE_ROOT, "Backup")])
    context = {'page': 'tools',
               'filenames': files,
               'library': library}
    return render_to_response('tools/rebuild.html', context)


def rebuild(request):
    Movie.objects.all().delete()
    for image in Image.objects.all():
        image.delete()
    Library.objects.all().delete()
    return _rescan(request)


@csrf_exempt
def rebuild_operation(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    filepath = unquote(request.POST.get('path'))
    if not filepath or filepath not in movie_files():
        return HttpResponseBadRequest()

    library = Library.objects.default
    movie, created = Movie.objects.get_or_create_from_filepath(filepath)
    if movie:
        library.add_movie(movie)
        return HttpResponse()

    return HttpResponseNotFound()


@csrf_exempt
def rebuild_actions(request):
    actions = []
    files = movie_files()
    files.sort()
    for f in files:
        short_name, _ = os.path.splitext(f.split("/")[-1])

        # add movie to the system
        actions.append({
            'action': "Add",
            'details': short_name,
            'action_url': reverse('rebuild_operation'),
            'action_params': {'path': quote(f)}
        })

        # find recommendations for movie
        actions.append({
            'action': "Get Recommendations",
            'details': short_name,
            'action_url': reverse('get_recommendations'),
            'action_params': {
                'path': quote(f),
                'max_recommendations': 10}
        })
    return HttpResponse(json.dumps(actions))

