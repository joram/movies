from default_django import *
import os

_EXPECTED_ENVIRONMENT_VARIABLES = {
    'required': [],
    'optional': []
}


def get_env(env_name, default=None, required=False):
    env_name = "MV_"+env_name
    _EXPECTED_ENVIRONMENT_VARIABLES['required' if required else 'optional'].append(env_name)
    if not os.environ.has_key(env_name):
        if required:
            raise Exception("required env variable `{env_name}` does not exist.".format(env_name=env_name))
        return default
    return os.environ.get(env_name)

DEFAULT_LIBRARY_NAME = "Serenity Library"
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
MOVIE_ROOT = "/media/silvia/Movies/"
TRANSMISSION_ADDRESS = get_env("TRANSMISSION_ADDRESS", required=False)
TRANSMISSION_PORT = get_env("TRANSMISSION_ADDRESS", required=False)
TRANSMISSION_USERNAME = get_env("TRANSMISSION_ADDRESS", required=False)
TRANSMISSION_PASSWORD = get_env("TRANSMISSION_ADDRESS", required=False)
TRANSMISSION_DOWNLOAD_DIR = get_env("TRANSMISSION_ADDRESS", required=False)
MOVIEDB_API_KEY = get_env("MOVIEDB_API_KEY", required=True)
MOVIEDB_WAIT_TIME = 0.5
DEFAULT_THUMBNAIL_SIZE = get_env("TRANSMISSION_ADDRESS", required=False, default="w342")


