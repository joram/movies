from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'movies.views.home.home', name='home'),
    url(r'^all/$', 'movies.views.home.home', name='all'),
    url(r'^recommendations/$', 'movies.views.recommendations.recommendations', name='recommendations'),
    url(r'^genres/$', 'movies.views.genres.genres', name='genres'),
    url(r'^genre/(?P<genre_id>[0-9]+)/$', 'movies.views.genres.genre', name='genre'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', 'movies.views.movie.movie', name='movie'),

    # url(r'^movie_manager/', include('movie_manager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
