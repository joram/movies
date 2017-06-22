import time
import os
import urllib

from django.db import models


class ImageManager(models.Manager):
    IMAGE_DIR = "apps/movies/static/"

    def get_image(self, image_url, directory, filename):

        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            print image_url, filepath
            urllib.urlretrieve(image_url, filepath)
            time.sleep(0.5)

    def create(self, image_type, size, filename, image_url):
        image = models.Manager.create(
            self,
            image_type=image_type,
            size=size,
            filename=filename)

        directory = "images/{image_type}/{size}".format(image_type=image_type, size=size)
        self.get_image(image_url, os.path.join(self.IMAGE_DIR, directory), filename)
        image.image = os.path.join(directory, filename)
        image.save()
        return image


def upload_to(self):
    return "{image_type}/{size}/{filename}".format(
        image_type=self.image_type,
        size=self.size,
        filename=self.filename
    )


class Image(models.Model):
    DEFAULT_STATIC_IMAGE_URL = "images/placeholder_movie_poster.jpg"

    image_type = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    @property
    def static_url(self):
        url = str(self.image) if self.image else self.DEFAULT_STATIC_IMAGE_URL
        return url

    class Meta:
        app_label = 'movies'
        db_table = "movies_image"

    objects = ImageManager()
