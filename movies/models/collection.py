from django.db import models


class Collection(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)

    @property
    def movies(self):
        from movies.models import MovieCollectionMap
        from movies.models import Movie
        movie_ids = [mcmap.movie.id for mcmap in MovieCollectionMap.objects.filter(collection=self)]
        return Movie.objects.filter(id__in=movie_ids)

    def add_movie(self, movie):
        from movies.models import MovieCollectionMap
        MovieCollectionMap.objects.create(movie=movie, collection=self)

    class Meta:
        app_label = 'movies'
