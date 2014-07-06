from django.db import models


class MovieWatchlistMap(models.Model):
    movie = models.ForeignKey('Movie')
    watchlist = models.ForeignKey('Watchlist')

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        return unicode("%s - %s" % (self.watchlist, self.movie))