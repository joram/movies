#!/usr/bin/python
from django.conf import settings

import os
from apps.movies.models import Movie, Library

DEFAULT_LIBRARY = settings.get_default_library()


def build_recommendations():
    for movie in Movie.objects.filter(state='available'):
        Movie.objects.get_recommendations(movie)


def _files_in_dir(path, file_types=['.avi', '.mp4'], ignore_paths=[]):
    if settings.FAKE_MOVIES_DIR:
        with open("tmp/movies.txt") as f:
            files = f.readlines()
            return files

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


# poster sizes include: w92, w154, w185, w342, w500, w780, original
def scan_movie_folder():
    files = _files_in_dir(settings.MOVIE_ROOT, ignore_paths=[os.path.join(settings.MOVIE_ROOT, "Backup")])
    for fullpath in files:
        movie, created = Movie.objects.create_from_filepath(fullpath)
        if movie:
            Movie.objects.get_poster(movie, "w342")

            # if created:
            #     print "created %s" % movie.name
            # else:
            #     print "already have: %s" % movie.name
        else:
            print "problem with: %s" % fullpath

scan_movie_folder()
#build_recommendations()

# for movie in Movie.objects.all():
#     print "getting poster for: %s" % movie.name
#     Movie.objects.get_poster(movie, "w342")



# for image in Image.objects.all():
#     image.delete()
