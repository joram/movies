import os, json

from django.conf import settings
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from common.models import Image
from movies.models import Movie, Collection


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
    Image.objects.all().delete()
    Collection.objects.all().delete()

    collection = Collection.objects.create(name="Initial Collection")
    files = _files_in_dir(settings.MOVIE_ROOT, ignore_paths=[os.path.join(settings.MOVIE_ROOT, "Backup")])
    context = {'page': 'tools',
               'filenames': files,
               'collection': collection}
    return render_to_response('tools/rebuild.html', context)


@csrf_exempt
def add_movie(request):
    filename = request.POST.get('filename')
    movie, created = Movie.objects.create_from_filepath(filename)
    context = {'movie': movie}
    response = render_to_response('tools/add_movie.html', context)
    print type(response)
    return response