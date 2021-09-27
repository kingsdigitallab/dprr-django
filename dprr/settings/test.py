from .base import *  # noqa

DEBUG = True

SECRET_KEY = "test"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache",
    }
}

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "test.db"},
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": (
            "promrep.solr_backends." "solr_backend_field_collapsing.GroupedSolrEngine"
        ),
        "URL": "http://127.0.0.1:8080/solr",
    },
}
