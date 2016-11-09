import time
import os
import urllib

from django.conf import settings
from django.db import models


class ImageManager(models.Manager):

    def get_image(self, storage_path, image_url):

        directory = os.path.dirname(storage_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.isfile(storage_path):
            urllib.urlretrieve(image_url, storage_path)
            time.sleep(0.5)

        return storage_path

    def create(self, image_type, size, filename, image_url):
        image = models.Manager.create(
            self,
            image_type=image_type,
            size=size,
            filename=filename)

        media_path = upload_to(image)
        self.get_image(os.path.join(settings.MEDIA_ROOT, media_path), image_url)
        image.image = media_path
        image.save()
        return image


def upload_to(self):
    return "%s/%s/%s" % (self.image_type, self.size, self.filename)


class Image(models.Model):
    image_type = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    filename = models.CharField(max_length=200)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    class Meta:
        app_label = 'movies'
	db_table = "movies_image"
        
    objects = ImageManager()
