from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class MovieListMovieMapManager(models.Manager):

    def filter_on_foreign_key(self, foreign_object):
        content_type = ContentType.objects.get_for_model(foreign_object)
        return self.filter(object_id=foreign_object.id, content_type=content_type)


class MovieListMovieMap(models.Model):
    movie = models.ForeignKey('Movie', related_name='map_movie')

    # generic foreign key to movie_list since it's abstract
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    movie_list = generic.GenericForeignKey('content_type', 'object_id')
    objects = MovieListMovieMapManager()

    class Meta:
        app_label = 'movies'
        db_table = "movies_movie_list_movie_map"

    def __unicode__(self):
        return unicode("%s - %s" % (self.movie_list, self.movie))
