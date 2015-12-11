from django.conf.urls import url

from rewrite_external_links.views import external_link


urlpatterns = [
    url(r'^external-link/$', external_link, name='external_link'),
]
