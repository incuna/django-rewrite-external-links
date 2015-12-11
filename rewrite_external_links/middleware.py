import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode
from django.utils.html_parser import HTMLParser


SAFE_EXTERNAL_LINK_PATTERNS = getattr(settings, 'SAFE_EXTERNAL_LINK_PATTERNS', ())
safe_urls = ''
if SAFE_EXTERNAL_LINK_PATTERNS:
    safe_urls = '(?!(' + '|'.join(SAFE_EXTERNAL_LINK_PATTERNS) + '))'


class RewriteExternalLinksMiddleware(object):
    """
    Rewrite all external links to go via a message page.
    Rewrite:
        <a href="http://www.example.com">
    To:
        <a href="/external_link/?link=http://www.example.com&next=...">
    """

    extlinks = re.compile(r'''
        (?P<before><a[^>]*href=['"]?)  # content from `<a` to `href='`
        (?P<link>https?://{}[^'">]*)  # href link
        (?P<after>[^>]*)  # content after the href attribute to the closing bracket `>`
    '''.format(safe_urls), re.VERBOSE)
    external_link_root = reverse('external_link')

    def process_response(self, request, response):
        h = HTMLParser()
        html_content_type = "text/html" in response['Content-Type']
        start_link = request.META.get('PATH_INFO').startswith(self.external_link_root)
        if (response.content and html_content_type and not start_link):
            next = request.path

            def linkrepl(m):
                return '{before}{root}?link={link}&next={next}{after}'.format(
                    root=self.external_link_root,
                    next=next,
                    before=m.group('before'),
                    # unescape the link before encoding it to ensure entities
                    # such as '&' don't get double escaped
                    link=urlencode(h.unescape(m.group('link')), safe=''),
                    after=m.group('after'),
                )
            response.content = self.extlinks.sub(linkrepl, response.content.decode())
            return response
        else:
            return response
