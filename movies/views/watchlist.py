from movies.models import Library
from _helpers import _paginated_movies


def watchlist(request):
    watchlist = Library.objects.default.watchlist
    return _paginated_movies(request, watchlist)