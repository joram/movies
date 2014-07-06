from django.db import models

from movies.models import MovieList


class Watchlist(MovieList):
    library = models.ForeignKey('Library')