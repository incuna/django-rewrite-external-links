import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode


SAFE_EXTERNAL_LINK_PATTERNS = getattr(settings, 'SAFE_EXTERNAL_LINK_PATTERNS', ())
safe_urls = ''
if SAFE_EXTERNAL_LINK_PATTERNS:
    safe_urls = '(?!(' + '|'.join(SAFE_EXTERNAL_LINK_PATTERNS) + '))'


class RewriteExternalLinksMiddleware(object):
    """
    Rewrite all external links to go via a message page.
    Rewrite:
        <a href="http://www.xxx.com">
    To:
        <a href="/external_link/?link=http://www.xxx.com&next=...">
    """

    #                            <a ... href="                www.xxx.com                                " ... />
    extlinks = re.compile(r'''(?P<before><a[^>]*href=['"]?)(?P<link>http.?://'''+safe_urls+'''[^'">]*)(?P<after>[^>]*)''')
    external_link_root = reverse('external_link')

    def process_response(self, request, response):
        if (response.content
                and "text/html" in response['Content-Type']
                and not request.META.get('PATH_INFO').startswith(self.external_link_root)):

            next = request.path
            def linkrepl(m):
                a = str('''%(before)s%(root)s?link=%(link)s&next=%(next)s%(after)s''' % {
                    'root': self.external_link_root,
                    'next': next,
                    'before': m.group('before'),
                    'link': urlencode(m.group('link'), safe=''),
                    'after': m.group('after'),
                    })
                return a
            response.content = self.extlinks.sub(linkrepl, response.content)
            return response
        else:
            return response
