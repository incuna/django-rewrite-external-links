from setuptools import setup

from rewrite_external_links import get_version


description = (
    'Rewrite all external (off-site) links to go via a message page, '
    + 'using a middleware class.'
)

setup(
    name="django-rewrite-external-links",
    packages=["rewrite_external_links"],
    include_package_data=True,
    version=get_version(),
    description=description,
    author="Incuna Ltd",
    author_email="admin@incuna.com",
    url="https://github.com/incuna/django-rewrite-external-links",
)
