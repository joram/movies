import random

from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from movies.models import Movie
from movies.models import MovieListMovieMap


class MovieList(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)

    # generic foreign key to parent since this class is abstract
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    movie_list = generic.GenericForeignKey('content_type', 'object_id')

    @property
    def movies(self):
        return Movie.objects.filter(map_movie__object_id=self.object_id).order_by('name_the_less')

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
        return Movie.objects.filter(recommended_movie__based_on_movie__in=self.movies).annotate(num_recommendations=Count('recommended_movie')).order_by('-num_recommendations')

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
        content_type = ContentType.objects.get_for_model(self)
        MovieListMovieMap.objects.get_or_create(movie=movie, object_id=self.id, content_type=content_type)

    def remove_movie(self, movie):
        content_type = ContentType.objects.get_for_model(self)
        movie_list_maps = MovieListMovieMap.objects.filter(movie=movie, object_id=self.id, content_type=content_type)
        movie_list_maps.delete()

    def contains(self, movie):
        content_type = ContentType.objects.get_for_model(self)
        movie_list_maps = MovieListMovieMap.objects.filter(movie=movie, object_id=self.id, content_type=content_type)
        if movie_list_maps.exists():
            return True
        return False

    def __unicode__(self):
        return unicode("%s" % self.name)

    class Meta:
        app_label = 'movies'
        abstract = True
