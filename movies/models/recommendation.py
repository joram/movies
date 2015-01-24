from django.db import models

from moviedb import MovieDB


class RecommendationManager(models.Manager):

    def create_from_id(self, movie_id, recommended_id):
        from movies.models import Movie

        if Movie.objects.filter(id=recommended_id).exists():
            recommended_movie = Movie.objects.get(id=recommended_id)
            return recommended_movie

        mdb = MovieDB()
        movie = Movie.objects.get(id=movie_id)
        details = mdb.get_movie_details_by_id(recommended_id)
        print details
        if details:
                recommended_movie, created = Movie.objects.create_from_moviedb_id(recommended_id,  details.get('title'), "", "recommended")
                print recommended_movie

                # create recommendation assosiations
                recomendation = self.create_from_moviedb_info(
                    based_on_movie=movie,
                    recommended_movie=recommended_movie,
                    details=details)
                print recomendation

                return recommended_movie

    def create_from_moviedb_info(self, based_on_movie, recommended_movie, details):
        return Recommendation.objects.get_or_create(
            based_on_movie=based_on_movie,
            recommended_movie=recommended_movie,
            recommended_id=details['id'],
            poster_path=details['poster_path'],
            release_date=details['release_date'],
            title=details['title'],
            vote_average=details['vote_average'],
            vote_count=details['vote_count'],
            popularity=details['popularity'],
        )


class Recommendation(models.Model):
    based_on_movie = models.ForeignKey('Movie', related_name='based_on_movie')
    recommended_movie = models.ForeignKey('Movie', null=True, blank=True, related_name='recommended_movie')

    recommended_id = models.CharField(null=True, blank=True, max_length=200)
    poster_path = models.CharField(null=True, blank=True, max_length=200)
    release_date = models.CharField(null=True, blank=True, max_length=200)
    title = models.CharField(null=True, blank=True, max_length=200)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    popularity = models.FloatField()

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'movies'
	db_table = "movies_recommendation"

    objects = RecommendationManager()
