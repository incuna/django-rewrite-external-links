from django.conf.urls import url, patterns


urlpatterns = patterns(
    'rewrite_external_links.views',
    url(r'^external-link/$', 'external_link', name='external_link'),
)
