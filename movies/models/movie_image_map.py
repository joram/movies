from django.db import models


class MovieImageMap(models.Model):
    movie = models.ForeignKey('Movie')
    image = models.ForeignKey('Image')

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        return unicode("%s - %s" % (self.movie, self.image))