#!/usr/bin/env python

import django
django.setup()
from apps.movies.views.tools.rebuild import repopulate_movies
from apps.movies.models.movie import Movie

import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)

repopulate_movies()
for m in Movie.objects.all().order_by('name'):
    print u"getting metadata for: {}".format(m.name)
    m.get_metadata()
    print u"getting recommendations for: {}".format(m.name)
    recs = m.get_recommendations()
    for r in recs:
        r.get_poster()
