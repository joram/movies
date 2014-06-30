
from django.conf import settings
from django.shortcuts import render_to_response

from movies.models import Movie
import requests

from tpb import TPB, CATEGORIES, ORDERS
import transmissionrpc


def _get_torrent(movie, required_likes=2):
    t = TPB('https://thepiratebay.se')
    search = t.search(""+movie.name, category=CATEGORIES.VIDEO.MOVIES)
    search.order(ORDERS.SEEDERS.DES).page(1)
    for torrent in search:
        (created, current_time) = torrent._created
        if torrent.seeders <= 0:
            return

        likes = 0
        if movie.name.lower() in torrent.title.lower():
            likes += 1
        if 'dvdrip' in torrent.title.lower():
            likes += 1
        if torrent.size > 700:
            likes += 1
        if torrent.seeders > 10:
            likes += 1
        if created > movie.release_date:
            likes += 1

        if likes > required_likes:
            return torrent


def _add_torrent_to_transmission(torrent):
    tc = transmissionrpc.Client(
        address=settings.TRANSMISSION_ADDRESS,
        port=settings.TRANSMISSION_PORT,
        user=settings.TRANSMISSION_USERNAME,
        password=settings.TRANSMISSION_PASSWORD)

    tc_torrent = tc.add_torrent(
        torrent=torrent.magnet_link,
        download_dir=settings.MOVIE_ROOT)

    return tc_torrent


def download(request, movie_id):
    try:
        movie = Movie.objects.get(moviedb_id=movie_id)
    except:
        movie = None

    torrent = False
    if movie:
        torrent = _get_torrent(movie)
        if torrent:
            tc_torrent = _add_torrent_to_transmission(torrent)

    context = {
        'movie': movie,
        'downloaded': bool(torrent)}
    return render_to_response('movie.html', context)
