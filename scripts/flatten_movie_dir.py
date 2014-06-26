#!/usr/bin/python
import os
from django.conf import settings

delete_extensions = ['.nfo', '.txt', '.html', '.db', '.jpg']
wanted_extensions = ['.avi', '.mp4', '.mkv', '.mov', '.flv', '.mpg', '.m4v', '.wmv']


def _files_in_dir(path, file_types=[]):
    files = []
    for f in os.listdir(path):

        # collect files
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            fileName, fileExtension = os.path.splitext(full_path)
            fileExtension = fileExtension.lower()
            if fileExtension in file_types:
                files.append(full_path)

        # recurse into sub folders
        if os.path.isdir(full_path):
            files.extend(_files_in_dir(full_path, file_types=file_types))

    return files


def _dirs(path):
    dirs = []

    if len(os.listdir(path)) == 0:
        dirs.append(path)

    for f in os.listdir(path):

        # collect files
        full_path = os.path.join(path, f)

        # recurse into sub folders
        if os.path.isdir(full_path):
            dirs.extend(_dirs(full_path))

    return dirs


def _new_path(filepath):
    # filename, fileExtension = os.path.splitext(filepath)
    path, filename = os.path.split(filepath)
    filename = filename.replace("_", " ")
    return os.path.join(settings.MOVIE_ROOT, filename)

# wanted_files = _files_in_dir(settings.MOVIE_ROOT, file_types=wanted_extensions)
# for filepath in wanted_files:
#     new_filepath = _new_path(filepath)
#     if new_filepath != filepath:
#         print "move: %s -> %s" % (filepath, new_filepath)
#         os.rename(filepath, new_filepath)
# print ""

## delete garbage files
# garbage_files = _files_in_dir(settings.MOVIE_ROOT, file_types=delete_extensions)
# for f in garbage_files:
#     print "deleting: %s" % f
#     os.remove(f)

for d in _dirs(settings.MOVIE_ROOT):
    print d
    os.rmdir(d)


# for fullpath in files:
#     movie, created = Movie.objects.create_from_title(fullpath, 'available')