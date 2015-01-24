from django.db import models
from django.conf import settings
from tpb import TPB, CATEGORIES, ORDERS
import transmissionrpc


def _year(movie):
    parts = movie.release_date.split("-")
    if len(parts) == 3:
        return int(parts[0])


def _torrent_quality(torrent, created, movie):
    likes = 0
    if movie.name.lower() in torrent.title.lower():
        likes += 1

    for good_word in ["english", 'dvdrip']:
        if good_word in torrent.title.lower():
            likes += 1

    for bad_word in ["collection", 'cam']:
        if bad_word in torrent.title.lower():
            likes -= 1

    if torrent.size > 700:
        likes += 1
    if created > movie.release_date:
        likes += 1

    year = _year(movie)
    if year and str(year) in torrent.title.lower():
        likes += 2

    if torrent.seeders > 10:
        likes += 1
    if torrent.seeders <= 0:
        return 0

    return likes


def _find_torrent(movie, minimum_torrent_quality=2):
    t = TPB('https://thepiratebay.se')
    search = t.search("%s %s" % (movie.name, _year(movie)), category=CATEGORIES.VIDEO)
    search.order(ORDERS.SEEDERS.DES).page(1)
    best_torrent = None
    best_torrent_quality = None
    for torrent in search:
        (created, current_time) = torrent._created

        quality = _torrent_quality(torrent, created, movie)
        if not best_torrent or quality > best_torrent_quality:
            best_torrent = torrent
            best_torrent_quality = quality

    if best_torrent_quality > minimum_torrent_quality:
        return best_torrent


def _add_torrent_to_transmission(torrent):

    transmission = transmissionrpc.Client(
        address=settings.TRANSMISSION_ADDRESS,
        port=settings.TRANSMISSION_PORT,
        user=settings.TRANSMISSION_USERNAME,
        password=settings.TRANSMISSION_PASSWORD)

    tc_torrent = transmission.add_torrent(
        torrent=torrent.magnet_link,
        download_dir=settings.MOVIE_ROOT)
    return tc_torrent


class TorrentManager(models.Manager):

    def get_or_create_for_movie(self, movie):
        torrents = self.filter(movie_id=movie.id)
        if torrents.exist():
            return self.filter(movie_id=movie.id)
        return self.create_for_movie(movie)

    def create_for_movie(self, movie):
        rpc_torrent = _find_torrent(movie)
        if rpc_torrent:
            transmission_torrent = _add_torrent_to_transmission(rpc_torrent)
            if transmission_torrent:
                return Torrent.objects.create(movie=movie, transmission_id=transmission_torrent.id)


class Torrent(models.Model):
    movie = models.ForeignKey('Movie')
    transmission_id = models.IntegerField()
    objects = TorrentManager()

    @property
    def transmission(self):
        return transmissionrpc.Client(
            address=settings.TRANSMISSION_ADDRESS,
            port=settings.TRANSMISSION_PORT,
            user=settings.TRANSMISSION_USERNAME,
            password=settings.TRANSMISSION_PASSWORD)

    def __unicode__(self):
        try:
            return unicode(self.transmission.get_torrent(self.transmission_id))
        except KeyError:
            return unicode("Unknown torrent")

    class Meta:
        app_label = 'movies'
        db_table = "movies_torrent"
