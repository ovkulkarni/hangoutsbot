import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COOKIES_FILE_PATH = os.path.join(BASE_DIR, "private/refresh_token.txt")

DATABASE_PATH = os.path.join(BASE_DIR, "private/database.db")

LOGGING_DIRECTORY = os.path.join(BASE_DIR, "logs/")

try:
    from .secret import *  # noqa
except ImportError:
    pass
