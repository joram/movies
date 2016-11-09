from django.db import models


class MovieImageMap(models.Model):
    movie = models.ForeignKey('Movie')
    image = models.ForeignKey('Image')

    class Meta:
        app_label = 'movies'
        db_table = "movies_movie_image_map"

    def __unicode__(self):
        return unicode("%s - %s" % (self.movie, self.image))
