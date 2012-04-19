import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode

import lxml


SAFE_EXTERNAL_LINK_PATTERNS = getattr(settings, 'SAFE_EXTERNAL_LINK_PATTERNS', ())
safe_urls = ''
if SAFE_EXTERNAL_LINK_PATTERNS:
    safe_urls = '(' + '|'.join(SAFE_EXTERNAL_LINK_PATTERNS) + ')'


class RewriteExternalLinksMiddleware(object):
    """
    Rewrite all external links to go via a message page.
    """
    def process_response(self, request, response):

        external_link_root = reverse('external_link', kwargs={'link': ''})

        if "text" in response['Content-Type'] and not request.META.get('PATH_INFO').startswith(external_link_root):
            next = str(request.path)

            html = lxml.html.document_fromstring(response.content)
            for element, attribute, link, pos in html.iterlinks():
                # I only care about a tags with an href that is external
                if element.tag == "a" and attribute == "href" and re.match(r'^http(s?):\/\/', link):
                    if re.match(safe_urls, link):
                        continue
                    element.set('href', '%(root)s%(link)s?next=%(next)s' % {'root': external_link_root, 'link': urlencode(link, safe=''), 'next': next})

            response.content = lxml.html.tostring(html)
            return response
        else:
            return response
