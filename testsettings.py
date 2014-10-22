DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

INSTALLED_APPS = (
    'validate_on_save',
)

SECRET_KEY = 'stub-value-for-django'

MIDDLEWARE_CLASSES = []
