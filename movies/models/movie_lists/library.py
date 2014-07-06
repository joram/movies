from django.conf import settings
from django.db import models

from movies.models.movie_list import MovieList
from movies.models import Watchlist


class LibraryManager(models.Manager):

    @property
    def default(self):
        l, _ = self.get_or_create(name=settings.DEFAULT_LIBRARY_NAME)
        l.object_id = l.id
        l.save()
        return l


class Library(MovieList):

    @property
    def breadcrumbs(self):
        return [self.name]

    @property
    def watchlist(self):
        wl, _ = Watchlist.objects.get_or_create(library=self, name="Watchlist")
        return wl

    class Meta(MovieList.Meta):
        db_table = 'movies_library'

    objects = LibraryManager()