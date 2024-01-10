from ._base import *

DEBUG = True


INSTALLED_APPS += [
    "debug_toolbar",
    # "silk",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0",
]
