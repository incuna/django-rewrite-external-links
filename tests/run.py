import sys

import dj_database_url
import django
from colour_runner.django_runner import ColourRunnerMixin
from django.conf import settings


settings.configure(
    DATABASES={
        'default': dj_database_url.config(
            default='postgres://localhost/rewrite_external_links'
        ),
    },
    DEFAULT_FILE_STORAGE='inmemorystorage.InMemoryStorage',
    INSTALLED_APPS=(
        'rewrite_external_links',
        'tests',

        'django.contrib.auth',
        'django.contrib.contenttypes',
    ),
    MIDDLEWARE_CLASSES=(),
    ROOT_URLCONF='rewrite_external_links.urls',
)


django.setup()


# DiscoverRunner requires `django.setup()` to have been called
from django.test.runner import DiscoverRunner  # noqa


class TestRunner(ColourRunnerMixin, DiscoverRunner):
    pass


test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['tests'])
if failures:
    sys.exit(1)
