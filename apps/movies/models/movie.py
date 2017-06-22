import os
import uuid

from django.conf import settings

from apps.common.models import Image
from apps.movies.models.movie_image_map import MovieImageMap
from apps.movies.models.recommendation import Recommendation
from apps.movies.models.torrent import Torrent
from company import *
from country import *
from genre import *
from language import *
from services.moviedb import MovieDB

MDB = MovieDB()


class MovieManager(models.Manager):

    def __init__(self):
        super(MovieManager, self).__init__()

    def get_or_create_from_filepath(self, filepath, get_metadata=False):
        path, filename = os.path.split(filepath)
        movie = Movie.objects.create(
            name=MDB.filename_to_title(filename),
            filename=filename
        )
        if get_metadata:
            movie.get_metadata()
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


class Movie(models.Model):
    name = models.CharField(null=True, blank=True, max_length=2000)
    name_the_less = models.CharField(null=True, blank=True, max_length=2000)
    filename = models.CharField(default="", null=True, blank=True, max_length=2000)
    pub_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    moviedb_id = models.CharField(null=True, blank=True, max_length=2000)
    imdb_id = models.CharField(null=True, blank=True, max_length=2000)
    original_title = models.CharField(null=True, blank=True, max_length=2000)
    overview = models.CharField(null=True, blank=True, max_length=2000)
    popularity = models.IntegerField(null=True, blank=True)
    release_date = models.CharField(null=True, blank=True, max_length=2000)
    tagline = models.CharField(null=True, blank=True, max_length=2000)
    runtime = models.IntegerField(null=True, blank=True)
    revenue = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    vote_average = models.IntegerField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)

    genres = models.ManyToManyField('Genre')
    production_companies = models.ManyToManyField('Company')
    production_countries = models.ManyToManyField('Country')
    spoken_languages = models.ManyToManyField('Language')

    has_metadata = models.BooleanField(default=False)
    has_recommendations = models.BooleanField(default=False)

    objects = MovieManager()

    @property
    def pub_id_string(self):
        return str(self.pub_id)

    @property
    def images(self):
        from apps.common.models.image import Image
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

    def get_recommendations(self, max_recommendations=10):
        from apps.movies.models.movie_lists.library import Library
        if not Library.objects.default.contains(self):
            self.has_recommendations = True
            self.save()
            return []

        recommendations = MDB.get_similar_movies(self).get('results', [])
        max_len = min(len(recommendations), max_recommendations)

        results = []
        for recommendation in recommendations[:max_len]:
            qs = Movie.objects.filter(name=recommendation.get("title"))
            if qs.count() > 0:
                recommended_movie = qs[0]
            else:
                recommended_movie, created = Movie.objects.get_or_create(name=recommendation.get("title"))

            if not recommended_movie.filename:
                recommended_movie.filename = ""
                recommended_movie.save()
            recommended_movie.get_moviedb_details(moviedb_id=recommendation.get("id"))
            Recommendation.objects.create_from_moviedb_info(self, recommended_movie, recommendation)
            results.append(recommended_movie)

        self.has_recommendations = True
        self.save()
        return results

    @property
    def downloading(self):
        return Torrent.objects.filter(movie=self).exists()

    def get_metadata(self):
        self.get_moviedb_details()
        self.get_poster()
        self.has_metadata = True
        self.save()

    def get_poster(self, image_size=settings.DEFAULT_THUMBNAIL_SIZE):
        """
        poster sizes include: w92, w154, w185, w342, w500, w780, original
        """
        from apps.common.models.image import Image

        filename = "moviedb_%s_poster_%s.jpg" % (self.moviedb_id, 0)
        filepath = "apps/movies/static/images/poster/w342/{}".format(filename)
        if os.path.exists(filepath):
            image = Image.objects.create(
                image_type='poster',
                size=image_size,
                image_url="???",
                filename=filename)
            MovieImageMap.objects.create(movie=self, image=image)

        mdb = MovieDB()
        images = mdb.get_image_list(self.moviedb_id)
        config = mdb.get_configuration()
        posters = images.get('posters', [])

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

    def get_moviedb_details(self, moviedb_id=-1):
        movie_year = MDB.filename_to_year(self.filename)
        if moviedb_id == -1:
            moviedb_id = MDB.get_id(self.name, movie_year)
        if moviedb_id == -1:
            print "can't find movie: {}".format(self.filename)
            return

        # create new one
        details = MDB.get_movie_details_by_id(moviedb_id)
        if not details:
            details = MDB.get_movie_details(self.name)
        if not details:
            print "no details"
            return

        self.moviedb_id = moviedb_id
        self.name = details['title']
        self.budget = details['budget']
        self.imdb_id = details['imdb_id']
        self.original_title = details['original_title']
        self.overview = details['overview']
        self.popularity = details['popularity']
        self.release_date = details['release_date']
        self.revenue = details['revenue']
        self.runtime = details['runtime'] if details['runtime'] else 0
        self.tagline = details['tagline']
        self.vote_average = details['vote_average']
        self.vote_count = details['vote_count']

        if self.name.lower().startswith("the "):
            self.name_the_less = self.name[5:]
        else:
            self.name_the_less = self.name

        for company in details['production_companies']:
            c, _ = Company.objects.get_or_create(moviedb_id=int(company['id']), name=company['name'])
            self.production_companies.add(c)

        for country in details['production_countries']:
            c, _ = Country.objects.get_or_create(iso_id=country['iso_3166_1'], name=country['name'])
            self.production_countries.add(c)

        for language in details['spoken_languages']:
            l, _ = Language.objects.get_or_create(iso_id=language['iso_639_1'], name=language['name'])
            self.spoken_languages.add(l)

        for genre in details['genres']:
            g, _ = Genre.objects.get_or_create(moviedb_id=int(genre['id']), name=genre['name'])
            self.genres.add(g)

        self.save()

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
        db_table = 'movies_movie'

    def __unicode__(self):
        unicode_str = ''.join([i if ord(i) < 128 else ' ' for i in self.name])
        return unicode("%s" % unicode_str)

    def fetch_torrent(self):
        if Torrent.objects.create_for_movie(self):
            return True
        return False
