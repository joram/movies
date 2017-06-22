from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from apps.movies.models import Movie
from services.moviedb import MovieDB


def _do_search(search_text):
    mdb = MovieDB()
    results = mdb.search_for_movie(search_text)
    return results


@csrf_exempt
def search(request):
    context = {
        'page': 'search',
        'search_text': ""}
    if request.method == 'POST':
        search_text = request.POST['search']
        context['search_text'] = search_text

        context["movies"] = []
        for movie_id in [r['id'] for r in _do_search(search_text).get('results', [])]:
            print "getting movie %s" % movie_id
            movie, _ = Movie.objects.create_from_moviedb_id(moviedb_id=movie_id)
            if movie:
                print movie
                context["movies"].append(movie)

    return render_to_response('search.html', context)