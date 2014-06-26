import time
import os
import urllib

from django.db import models


class ImageManager(models.Manager):

    def get_image(self, storage_path, image_url):
        if not os.path.isfile(storage_path):
            urllib.urlretrieve(image_url, storage_path)
            time.sleep(0.5)


class Image(models.Model):
    filepath = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    size = models.CharField(max_length=200)

    class Meta:
        app_label = 'movies'
        
    objects = ImageManager()