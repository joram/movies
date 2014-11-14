import os

from django.conf import settings

from country import *
from company import *
from genre import *
from language import *
from movie_image_map import MovieImageMap
from recommendation import Recommendation
from common.models.image import Image
from moviedb import MovieDB
from movies.models import Torrent


class MovieManager(models.Manager):

    def __init__(self):
        super(MovieManager, self).__init__()
        self.mdb = MovieDB()

    def get_or_create_from_filepath(self, filepath):
        if filepath:
            path, filename = os.path.split(filepath)
            movie_name = self.mdb.filename_to_title(filename)
            movie_year = self.mdb.filename_to_year(filename)
            moviedb_id = self.mdb.get_id(movie_name, movie_year)
            if moviedb_id != -1:
                movie, created = self.create_from_moviedb_id(moviedb_id, movie_name, filename)
                movie.get_poster()
                return movie, created
        return None, False

    def create_from_moviedb_id(self, moviedb_id=None, movie_name="", filename="", state="available"):

        # return pre-existing movie
        if Movie.objects.filter(moviedb_id=moviedb_id).exists():
            return Movie.objects.get(moviedb_id=moviedb_id), False

        # create new one
        details = None
        if moviedb_id:
            details = self.mdb.get_movie_details_by_id(moviedb_id)
        else:
            if movie_name:
                details = self.mdb.get_movie_details(movie_name)

        if not details:
            return None, False

        movie = Movie.objects.create(
            filename=filename,
            moviedb_id=moviedb_id,

            name=details['title'],
            budget=details['budget'],
            imdb_id=details['imdb_id'],
            original_title=details['original_title'],
            overview=details['overview'],
            popularity=details['popularity'],
            release_date=details['release_date'],
            revenue=details['revenue'],
            runtime=details['runtime'] if details['runtime'] else 0,
            tagline=details['tagline'],
            vote_average=details['vote_average'],
            vote_count=details['vote_count'])

        for company in details['production_companies']:
            c, _ = Company.objects.get_or_create(moviedb_id=int(company['id']), name=company['name'])
            movie.production_companies.add(c)

        for country in details['production_countries']:
            c, _ = Country.objects.get_or_create(iso_id=country['iso_3166_1'], name=country['name'])
            movie.production_countries.add(c)

        for language in details['spoken_languages']:
            l, _ = Language.objects.get_or_create(iso_id=language['iso_639_1'], name=language['name'])
            movie.spoken_languages.add(l)

        for genre in details['genres']:
            g, _ = Genre.objects.get_or_create(moviedb_id=int(genre['id']), name= genre['name'])
            movie.genres.add(g)

        movie.get_poster()
        movie.save()
        return movie, True

    def get_recommendations_based_on_movies(self, movies_qs):
        recommendations = Recommendation.objects.filter(based_on_movie__in=movies_qs)
        recommended_movies = set([r.recommended_movie for r in recommendations if r.recommended_movie not in movies_qs])

        movies = []
        for recommended_movie in recommended_movies:
            num_recommendations = recommendations.filter(recommended_movie=recommended_movie).count()
            movies.append({
                'num_recommendations': num_recommendations,
                'movie': recommended_movie
            })
        movies = sorted(movies, key=lambda k: k['num_recommendations'])
        movies.reverse()
        return movies

    def get_or_create(self, **kwargs):
        if self.filter(**kwargs).exists():
            return self.get(**kwargs), False
        return self.create(**kwargs)

    def create(self, **kwargs):
        movie = models.Manager.create(self, **kwargs)
        if movie.name.lower().startswith("the "):
            movie.name_the_less = movie.name[5:]
        else:
            movie.name_the_less = movie.name
        movie.save()
        return movie


class Movie(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    name_the_less = models.CharField(null=True, blank=True, max_length=200)
    filename = models.CharField(null=True, blank=True, max_length=200)

    moviedb_id = models.CharField(null=True, blank=True, max_length=200)
    imdb_id = models.CharField(null=True, blank=True, max_length=200)
    original_title = models.CharField(null=True, blank=True, max_length=200)
    overview = models.CharField(null=True, blank=True, max_length=200)
    popularity = models.IntegerField()
    release_date = models.CharField(null=True, blank=True, max_length=200)
    tagline = models.CharField(null=True, blank=True, max_length=200)
    runtime = models.IntegerField()
    revenue = models.IntegerField()
    budget = models.IntegerField()
    vote_average = models.IntegerField()
    vote_count = models.IntegerField()

    genres = models.ManyToManyField('Genre')
    production_companies = models.ManyToManyField('Company')
    production_countries = models.ManyToManyField('Country')
    spoken_languages = models.ManyToManyField('Language')

    objects = MovieManager()

    @property
    def images(self):
        image_ids = [mimap.image.id for mimap in MovieImageMap.objects.filter(movie=self)]
        return Image.objects.filter(id__in=image_ids)

    @property
    def poster(self):
        images = self.images.filter(size=settings.DEFAULT_THUMBNAIL_SIZE)
        if images.count() >= 1:
            return images[0]
        return None

    @property
    def recommendations(self):
        return Movie.objects.filter(recommended_movie__based_on_movie=self)

    def get_recommendations(self):
        return Recommendation.objects.create_from_movie(self)

    def get_recommendation_list(self):
        mdb = MovieDB()
        return mdb.get_similar_movies(self)['results']

    @property
    def downloading(self):
        return Torrent.objects.filter(movie=self).exists()

    def get_poster(self, image_size=settings.DEFAULT_THUMBNAIL_SIZE):
        """
        poster sizes include: w92, w154, w185, w342, w500, w780, original
        """
        mdb = MovieDB()
        images = mdb.get_image_list(self.moviedb_id)
        config = mdb.get_configuration()
        posters = images.get('posters')

        for poster in posters:
            if posters and len(posters):
                language = poster['iso_639_1']
                if language == "en":

                    url = "%s%s%s" % (config['images']['base_url'], image_size, poster['file_path'])
                    filename = "moviedb_%s_poster_%s.jpg" % (self.moviedb_id, images['posters'].index(poster))
                    image = Image.objects.create(
                        image_type='poster',
                        size=image_size,
                        image_url=url,
                        filename=filename)
                    MovieImageMap.objects.create(movie=self, image=image)
                    return

        for poster in posters:
            if posters and len(posters):
                url = "%s%s%s" % (config['images']['base_url'], image_size, poster['file_path'])
                filename = "moviedb_%s_poster_%s.jpg" % (self.moviedb_id, images['posters'].index(poster))
                image = Image.objects.create(
                    image_type='poster',
                    size=image_size,
                    image_url=url,
                    filename=filename)
                MovieImageMap.objects.create(movie=self, image=image)
                return

        print "no poster for: %s" % self.name
        print posters

    @property
    def status(self):
        from movie_lists.library import Library
        if self.downloading:
            return "downloading"
        if Library.objects.default.contains(self):
            return "have"
        if Library.objects.default.watchlist.contains(self):
            return "watching"
        return "available"

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        unicode_str = ''.join([i if ord(i) < 128 else ' ' for i in self.name])
        return unicode("%s" % unicode_str)

    def fetch_torrent(self):
        if Torrent.objects.create_for_movie(self):
            return True
        return False