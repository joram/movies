from django.db import models

    
class Company(models.Model):
    moviedb_id = models.IntegerField()
    name = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        app_label = 'movies'
        
    def __unicode__(self):
        return self.name
