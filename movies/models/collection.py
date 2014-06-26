from django.db import models
from movies.models.movie import *
from movies.models.recommendation import *

class CollectionManager(models.Manager):

    
    def create_from_list(self, collection_name, movie_list_filename, build_recommendations):
        collection, _ = Collection.objects.get_or_create(name=collection_name)
        collection.save()
        
        i = 0        
        f = open(movie_list_filename, "r")
        for movie_title in f:
            res = Movie.objects.create_from_filepath(movie_title, 'have')
            if res:
                movie, created = res
                print "%s:\t%s" % (i, movie.name)

                if created:
                    collection.movies.add(movie)
                if build_recommendations:
                    Recommendation.objects.create_from_moviedb_id(movie.moviedb_id)
                
            i += 1
            
        collection.save()
        return 

    def get_or_create_all_encompassing_collection(self):
        collection = self.get(name="Entire Collection")
        if collection:
            return collection

        collection = self.create(name="Entire Collection")
        for movie in Movie.objects.all():
            collection.movies.add(movie)

    def get(self, *args, **kwargs):
        collection = super(CollectionManager, self).get(args, kwargs)
        if collection:
            return collection
        return create_all_encompassing_collection
               
class Collection(models.Model):
    name = models.CharField(null=True, blank=True, max_length=200)
    movies = models.ManyToManyField('Movie', related_name='+')

    objects = CollectionManager()
    
    class Meta:
        app_label = 'movies'
