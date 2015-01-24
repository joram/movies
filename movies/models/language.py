from django.db import models

                
class Language(models.Model):
    iso_id = models.CharField(null=True, blank=True, max_length=200)
    name = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        app_label = 'movies'
        db_table = "movies_language"
        
    def __unicode__(self):
        return self.name
