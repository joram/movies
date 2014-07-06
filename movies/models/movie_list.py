import random

from django.db import models
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from movies.models import Movie
from movies.models import MovieListMovieMap


class MovieList(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    genre = models.ForeignKey('Genre', null=True, blank=True)

    # generic foreign key to parent since this class is abstract
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    parent = generic.GenericForeignKey('content_type', 'object_id')

    @property
    def movies(self):
        return Movie.objects.filter(map_movie__object_id=self.object_id)
        # if self.parent:
        #     qs = self.parent.movies
        # else:
        #     maps = MovieListMovieMap.objects.filter(
        #         object_id=self.id,
        #         content_type=ContentType.objects.get_for_model(self))
        #     movie_ids = [mcmap.movie.id for mcmap in maps]
        #     qs = Movie.objects.filter(id__in=movie_ids)
        #
        # if self.genre:
        #     qs = qs.filter(genres__id=self.genre_id)
        # return qs

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
        recs = Movie.objects.filter(recommended_movie__based_on_movie__in=self.movies).annotate(num_recommendations=Count('recommended_movie')).order_by('-num_recommendations')
        print "num recommendations: %s" % recs.count()
        for r in recs:
            print "%s - %s" % (r.num_recommendations, r)
        return Movie.objects.filter(recommended_movie__based_on_movie__in=self.movies).annotate(num_recommendations=Count('recommended_movie')).order_by('-num_recommendations')

    def random_movie(self, poster_required=True):
        movies = self.movies
        movie = None
        while not movie and movies.count() > 1:
            movie = random.choice(movies)
            if not poster_required or movie.poster:
                return movie
            movies.remove(movie)

    def genre_movie_list(self, genre):
        sublist = MovieList()
        sublist.name = genre.name
        sublist.genre = genre
        sublist.parent = self
        return sublist

    def add_movie(self, movie):
        MovieListMovieMap.objects.create(movie=movie, movie_list=self)

    class Meta:
        app_label = 'movies'
        abstract = True