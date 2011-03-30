from django.conf.urls.defaults import *


urlpatterns = patterns(
    'rewrite_external_links.views',
    url(r'^external-link/(?P<link>.*)$', 'external_link', name='external_link'),
)
