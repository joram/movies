import os, json

from django.db import models
from country import *
from company import *
from genre import *
from language import *
from recommendation import Recommendation
from common.models.image import Image

from moviedb import MovieDB
#from torrents.thePirateBay import ThePirateBay


class MovieManager(models.Manager):

    def __init__(self):
        super(MovieManager, self).__init__()
        self.mdb = MovieDB()

    def create_from_filepath(self, filepath, state="available"):

        path, filename = os.path.split(filepath)
        movie_name = self.mdb.filename_to_title(filename).replace(".mp4", "")
        movie_year = self.mdb.filename_to_year(filename)
        moviedb_id = self.mdb.get_id(movie_name, movie_year)
        if moviedb_id != -1:
            return self.create_from_moviedb_id(moviedb_id, movie_name, filename, state)
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
            state= state,
            filename= filename,
            moviedb_id= moviedb_id,

            name= details['title'],
            budget= details['budget'],
            imdb_id= details['imdb_id'],
            original_title= details['original_title'],
            overview= details['overview'],
            popularity = details['popularity'],
            release_date= details['release_date'],
            revenue= details['revenue'],
            runtime= details['runtime'] if details['runtime'] else 0,
            tagline= details['tagline'],
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

        self.get_poster(movie)
        movie.save()
        return movie, True

    def get_poster(self, movie, image_size="w92"):
        """
        poster sizes include: w92, w154, w185, w342, w500, w780, original
        """
        mdb = MovieDB()
        images = mdb.get_image_list(movie.moviedb_id)
        config = mdb.get_configuration()

        poster_directory = "./common/static/images/poster/%s" % image_size
        if not os.path.exists(poster_directory):
            os.makedirs(poster_directory)

        posters = images.get('posters')
        if posters and len(posters):
            image = posters[0]
            language = image['iso_639_1']
            if language == "en":
                url = "%s%s%s" % (config['images']['base_url'], image_size, image['file_path'])
                filename = "moviedb_%s_poster_%s.jpg" % (movie.moviedb_id, images['posters'].index(image))
                storage_path = "%s/%s" % (poster_directory, filename)
                static_path = "images/poster/%s/%s" % (image_size, filename)
                Image.objects.get_image(storage_path, url)

                image = Image.objects.create(
                    filepath=static_path,
                    type='poster',
                    size=image_size)

                if not movie.default_poster:
                    movie.default_poster = image

                movie.posters.add(image)
                movie.save()

    def get_recommendations(self, movie):
        return Recommendation.objects.create_from_movie(movie)

    def get_recommendations_based_on_movies(self, movies_qs, ignore_available=True):
        recommendations = Recommendation.objects.filter(based_on_movie__in=movies_qs)
        recommended_movies = set([r.recommended_movie for r in recommendations])

        if ignore_available:
            recommended_movies = [movie for movie in recommended_movies if movie.state != "available"]

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
    name = models.CharField(null=True, blank=True, max_length=200)
    filename = models.CharField(null=True, blank=True, max_length=200)
    poster = models.ForeignKey('Image', null=True, blank=True, related_name='+')
    
    default_poster = models.ForeignKey('Image', null=True, blank=True, related_name='poster')
    default_background = models.ForeignKey('Image', null=True, blank=True, related_name='background')
    posters = models.ManyToManyField('Image', null=True, blank=True, related_name='posters')
    backgrounds = models.ManyToManyField('Image', null=True, blank=True, related_name='backgrounds')


    moviedb_id = models.CharField(null=True, blank=True, max_length=200)
    imdb_id = models.CharField(null=True, blank=True, max_length=200)
    original_title = models.CharField(null=True, blank=True, max_length=200)
    overview = models.CharField(null=True, blank=True, max_length=200)
    popularity = models.IntegerField()
    release_date = models.CharField(null=True, blank=True, max_length=200)
    tagline = models.CharField(null=True, blank=True, max_length=200)
    state = models.CharField(default="available", max_length=200)
    runtime = models.IntegerField()
    revenue = models.IntegerField()
    budget = models.IntegerField()
    vote_average = models.IntegerField()
    vote_count = models.IntegerField()

    genres = models.ManyToManyField('Genre')
    production_companies = models.ManyToManyField('Company')
    production_countries = models.ManyToManyField('Country')
    spoken_languages = models.ManyToManyField('Language')

    recommendations = models.ManyToManyField('Movie', related_name='++')

    objects = MovieManager()

    @property
    def poster(self, poster_size="w342"):
        for poster in self.posters.all():
            if poster.size == poster_size:
                return poster.filepath
        return ""

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        return self.name
        
 #    def torrent(self):
 #        tpb = ThePirateBay()
 #        search_results = tpb.search(self.name)
 #        if len(search_results)>1:
 #            best_result = search_results[0]
 # #           if best_result['seeds'] > 100:
 #            print "sending torrent to transmision: %s" %  best_result['mag_lnk']
 #            self.state = "downloading"
 #            self.save()
