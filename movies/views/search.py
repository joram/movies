from django.shortcuts import render_to_response
from movies.models import Movie, MovieDB
from django.views.decorators.csrf import csrf_exempt


def _do_search(search_text):
    mdb = MovieDB()
    results = mdb.search_for_movie(search_text)
    return results


@csrf_exempt
def search(request):
    context = {'page': 'search'}
    if request.method == 'POST':
        search_text = request.POST['search']
        context['search_text'] = search_text
        context['results'] = _do_search(search_text)
        context['movie_ids'] = [m['id'] for m in context['results']['results']]

    return render_to_response('search.html', context)

@csrf_exempt
def add_to_watchlist(request):
    context = {'page': 'search'}
    if request.method == 'POST':
        search_text = request.POST['search']
        context['search_text'] = search_text
        context['results'] = _do_search(search_text)
        context['movie_ids'] = [m['id'] for m in context['results']['results']]

    return render_to_response('search.html', context)