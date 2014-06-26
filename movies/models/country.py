from django.db import models

        
class Country(models.Model):
    iso_id = models.CharField(null=True, blank=True, max_length=2)
    name = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        app_label = 'movies'

    def __unicode__(self):
        return self.name
