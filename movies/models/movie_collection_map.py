from django.db import models


class MovieCollectionMap(models.Model):
    movie = models.ForeignKey('Movie')
    collection = models.ForeignKey('Collection')

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        return unicode("%s - %s" % (self.collection, self.movie))