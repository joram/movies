import uuid
import random

from django.db import models
from django.db.models import Count

from apps.movies.models import Movie
from apps.movies.models import MovieListMovieMap


class MovieList(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    pub_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    @property
    def movies(self):
        mappings = MovieListMovieMap.objects.filter(movie_list_pub_id=self.pub_id)
        movie_pub_ids = [mapping.movie_pub_id for mapping in mappings]
        movies_qs = Movie.objects.filter(pub_id__in=movie_pub_ids).exclude(moviedb_id=None)
        if hasattr(self, 'genre'):
            movies_qs = movies_qs.filter(genres=self.genre)
        movies_qs = movies_qs.order_by('name_the_less')
        return movies_qs

    @property
    def breadcrumbs(self):
        if self.parent:
            return self.parent.breadcrumbs.extend(self.name)
        return [self.name]

    @property
    def genres(self):
        # TODO make from filters to speedup
        genres_list = []
        for genres_of_movie in [movie.genres for movie in self.movies]:
            for genre in genres_of_movie.all():
                if genre not in genres_list:
                    genres_list.append(genre)

        return genres_list

    @property
    def recommendations(self):
        return Movie.objects.filter(recommended_movie__based_on_movie__in=self.movies).annotate(num_recommendations=Count('recommended_movie')).order_by('-num_recommendations')[:24]

    def random_movie(self, poster_required=True, genre=None):
        movies = self.movies
        if genre:
            movies = movies.filter(genres=genre)
        movies = [m for m in movies]

        movie = None
        while not movie and len(movies) > 1:
            movie = random.choice(movies)
            movies.remove(movie)
            if movie.poster or not poster_required:
                return movie

        print "no movies with posters"

    def add_movie(self, movie):
        print "adding %s to list: %s" % (movie, self)
        MovieListMovieMap.objects.get_or_create(
            movie_pub_id=movie.pub_id,
            movie_list_pub_id=self.pub_id
        )

    def remove_movie(self, movie):
        movie_list_maps = MovieListMovieMap.objects.filter(
            movie_pub_id=movie.pub_id,
            movie_list_pub_id=self.pub_id
        )
        movie_list_maps.delete()

    def contains(self, movie):
        movie_list_maps = MovieListMovieMap.objects.filter(
            movie_pub_id=movie.pub_id,
            movie_list_pub_id=self.pub_id
        )
        if movie_list_maps.exists():
            return True
        return False

    def __unicode__(self):
        return unicode("%s" % self.name)

    class Meta:
        app_label = 'movies'
        abstract = True
