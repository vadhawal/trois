
DEBUG = True

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "saumishr",
        # Not used with sqlite3.
        "USER": "saumishr",
        # Not used with sqlite3.
        "PASSWORD": "hello123",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "www.demoapp.com",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "5432",
    }
}
