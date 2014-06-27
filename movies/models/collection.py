from django.db import models
from movies.models.movie_collection_map import MovieCollectionMap


class Collection(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)

    def add_movie(self, movie):
        MovieCollectionMap.objects.create(movie=movie, collection=self)

    class Meta:
        app_label = 'movies'
