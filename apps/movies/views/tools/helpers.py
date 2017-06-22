import os
from django.conf import settings


def _files_in_dir(path, file_types=['.avi', '.mp4', '.mkv', '.m4v', '.mpg', '.flv', '.wmv', '.mov'], ignore_paths=[]):
    if settings.FAKE_MOVIES_DIR:
        with open("tmp/movies.txt") as f:
            files = f.readlines()
            files = [f.replace("\n", "") for f in files]
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


def movie_files():
    return _files_in_dir(settings.MOVIE_ROOT, ignore_paths=[os.path.join(settings.MOVIE_ROOT, "Backup")])


