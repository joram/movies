from django.db import models


class Watchlist(models.Model):

    @property
    def movies(self):
        from movies.models import MovieWatchlistMap
        from movies.models import Movie
        movie_ids = [mcmap.movie.id for mcmap in MovieWatchlistMap.objects.filter(collection=self)]
        return Movie.objects.filter(id__in=movie_ids)

    def add_movie(self, movie):
        from movies.models import MovieCollectionMap
        MovieCollectionMap.objects.create(movie=movie, collection=self)

    class Meta:
        app_label = 'movies'
