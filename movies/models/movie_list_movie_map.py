from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class MovieListMovieMap(models.Model):
    movie = models.ForeignKey('Movie', related_name='map_movie')

    # generic foreign key to movie_list since it's abstract
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    movie_list = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        return unicode("%s - %s" % (self.movie_list, self.movie))