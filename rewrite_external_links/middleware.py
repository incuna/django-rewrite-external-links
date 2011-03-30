import re
from django.conf import settings
from django.core.urlresolvers import reverse

SAFE_EXTERNAL_LINK_PATTERNS = getattr(settings, 'SAFE_EXTERNAL_LINK_PATTERNS', ())
safe_urls = ''
if SAFE_EXTERNAL_LINK_PATTERNS:
    safe_urls = '(?!('+ '|'.join(getattr(settings, 'SAFE_EXTERNAL_LINK_PATTERNS', ())) +  '))'


class RewriteExternalLinksMiddleware(object):
    '''
    Rewrite all external links to go via a message page.
    '''


    extlinks = re.compile(r'''<a(?P<before>[^>]*)href=['"]*(?P<old>http.?://'''+safe_urls+'''[^'">]*)(?P<after>[^>]*)''')

    def process_response(self, request, response):

        external_link_root = reverse('external_link', kwargs={'link': ''})

        if ("text" in response['Content-Type'] and not request.META.get('PATH_INFO').startswith(external_link_root)):
            next = str(request.path)

            response.content = self.extlinks.sub('<a \g<before>href="%(root)s\g<old>?next=%(next)s"\g<after>' % {'root': external_link_root, 'next': next}, response.content)
            return response
        else:
            return response
