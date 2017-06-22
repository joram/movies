from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('apps.movies.views',

    url(r'^$', 'search.search', name='search'),
    url(r'^all/$', 'home.home', name='home'),
    url(r'^recommendations/$', 'recommendations.recommendations', name='recommendations'),
    url(r'^watchlist/$', 'watchlist.watchlist', name='watchlist'),
    url(r'^watchlist/(?P<watchlist_id>[0-9]+)/add/(?P<movie_id>[0-9]+)/$', 'watchlist.add_to_watchlist', name='add_to_watchlist'),
    url(r'^genres/$', 'genres.genres', name='genres'),
    url(r'^search/$', 'search.search', name='search'),
    url(r'^genre/(?P<genre_id>[0-9]+)/$', 'genres.genre', name='genre'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', 'movie.movie', name='movie'),
    url(r'^movie/(?P<moviedb_id>[0-9]+)/fetch/$', 'download.fetch_torrent_for_movie', name='fetch_movie'),
    url(r'^movies/rebuild/$', 'tools.rebuild.rebuild', name='rebuild'),
    url(r'^movies/rebuild/actions/list/$', 'tools.rebuild.rebuild_actions', name='rebuild_actions'),
    url(r'^movies/rebuild/actions/add/$', 'tools.rebuild.rebuild_operation', name='rebuild_operation'),
    url(r'^movies/rebuild/actions/get_recommendations/$', 'tools.recommend.get_recommendations_for_movie', name='get_recommendations'),
    url(r'^movies/rescan/$', 'tools.rebuild.rebuild', name='rescan'),
    url(r'^movies/rebuild/recomendations/$', 'tools.rebuild_recommendations', name='rebuild recommendations'),

    # AJAX
    url(r'^movies/add_movie/$', 'tools.add_movie', name='add_movie'),
    url(r'^movies/rebuild/recomendation/list/$', 'tools.get_recommendation_list', name='get recommendations'),
    url(r'^movies/rebuild/recomendation/movie/$', 'tools.get_single_recommendation', name='get single recommendations'),

    # url(r'^movie_manager/', include('movie_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT}))
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
