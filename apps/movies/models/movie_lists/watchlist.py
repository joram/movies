from django.db import models

from apps.movies.models import MovieList


class Watchlist(MovieList):
    library = models.ForeignKey('Library')

    class Meta(MovieList.Meta):
        db_table = 'movies_watchlist'

