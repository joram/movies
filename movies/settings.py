from django.conf import settings
from movies.models import Library

DEFAULT_LIBRARY, _ = Library.objects.get_or_create(name=settings.DEFAULT_LIBRARY_NAME)

