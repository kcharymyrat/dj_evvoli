from ._base import *

DEBUG = True
LOG_LEVEL = "INFO"


if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
]


COMPRESS_ENABLED = True
