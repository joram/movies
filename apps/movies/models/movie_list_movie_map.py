from django.db import models


class MovieListMovieMap(models.Model):
    movie_pub_id = models.CharField(max_length=32)
    movie_list_pub_id = models.CharField(max_length=32)

    class Meta:
        app_label = 'movies'
        db_table = "movies_movie_list_movie_map"

    def __unicode__(self):
        from apps.movies.models import Movie, MovieList
        movie = Movie.objects.get(id=self.movie_id)
        movie_list = MovieList.objects.get(id=self.movie_list_id)
        return unicode("%s - %s" % (movie_list, movie))
