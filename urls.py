from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import apps.movies.views as movie_views
from apps.movies.views.search import search
from apps.movies.views.home import home
from apps.movies.views.recommendations import recommendations
from apps.movies.views.watchlist import watchlist
from apps.movies.views.genres import genre, genres
from apps.movies.views.movie import movie
from apps.movies.views.download import fetch_torrent_for_movie
from apps.movies.views.tools.rebuild import rebuild, rebuild_actions, rebuild_operation

urlpatterns = [

    url(r'^$', search, name='search'),
    url(r'^all/$', movie_views.home.home, name='home'),
    url(r'^recommendations/$', movie_views.recommendations.recommendations, name='recommendations'),
    url(r'^watchlist/$', movie_views.watchlist.watchlist, name='watchlist'),
    url(r'^watchlist/(?P<watchlist_id>[0-9]+)/add/(?P<movie_id>[0-9]+)/$', movie_views.watchlist.add_to_watchlist, name='add_to_watchlist'),
    url(r'^genres/$', genres, name='genres'),
    url(r'^search/$', search, name='search'),
    url(r'^genre/(?P<genre_id>[0-9]+)/$', genre, name='genre'),
    url(r'^movie/(?P<pub_id>[0-9a-z\-]+)/$', movie, name='movie'),
    url(r'^movie/(?P<moviedb_id>[0-9]+)/fetch/$', fetch_torrent_for_movie, name='fetch_movie'),
    url(r'^movies/rebuild/$', rebuild, name='rebuild'),
    url(r'^movies/rebuild/actions/list/$', rebuild_actions, name='rebuild_actions'),
    url(r'^movies/rebuild/actions/add/$', rebuild_operation, name='rebuild_operation'),
    url(r'^movies/rebuild/actions/get_recommendations/$', movie_views.tools.recommend.get_recommendations_for_movie, name='get_recommendations'),
    url(r'^movies/rescan/$', rebuild, name='rescan'),
    url(r'^movies/rebuild/recomendations/$', movie_views.tools.rebuild_recommendations, name='rebuild recommendations'),

    # AJAX
    url(r'^movies/add_movie/$', movie_views.tools.add_movie, name='add_movie'),
    url(r'^movies/rebuild/recomendation/list/$', movie_views.tools.get_recommendation_list, name='get recommendations'),
    url(r'^movies/rebuild/recomendation/movie/$', movie_views.tools.get_single_recommendation, name='get single recommendations'),

    # url(r'^movie_manager/', include('movie_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

# urlpatterns += [
#     r'^media/(?P<path>.*)$', 'static.serve', { 'document_root': settings.MEDIA_ROOT},
# ]
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
