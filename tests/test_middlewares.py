from django.http.response import HttpResponse
from django.template.defaultfilters import urlencode
from django.test import TestCase
from mock import MagicMock

from rewrite_external_links.middleware import RewriteExternalLinksMiddleware


class TestRewriteExternalLinksMiddleware(TestCase):
    def setUp(self):
        self.middleware = RewriteExternalLinksMiddleware()

    def test_no_response_content(self):
        """response doesn't change if no response content."""
        request = MagicMock()
        content_type = 'application/thraud+xml'
        initial_response = HttpResponse(content_type=content_type)
        processed_response = self.middleware.process_response(
            request=request,
            response=initial_response,
        )
        self.assertEqual(processed_response.content, b'')

    def test_other_content_type(self):
        """response doesn't change if `Content-Type` is not `text/html`."""
        request = MagicMock()
        content_type = 'application/thraud+xml'
        content = b'<a href="http://example.com"></a>'
        initial_response = HttpResponse(content=content, content_type=content_type)
        processed_response = self.middleware.process_response(
            request=request,
            response=initial_response,
        )
        self.assertEqual(processed_response.content, content)

    def test_other_request_path_info(self):
        request = MagicMock()
        request.META = {'PATH_INFO': '/external-link/'}
        content_type = 'text/html'
        content = b'<a href="http://example.com"></a>'
        initial_response = HttpResponse(content=content, content_type=content_type)
        processed_response = self.middleware.process_response(
            request=request,
            response=initial_response,
        )
        self.assertEqual(processed_response.content, content)

    def test_response_content(self):
        path = 'test-path'
        link = 'http://example.com'
        request = MagicMock()
        request.META = {'PATH_INFO': '/another-url/'}
        request.path = path
        content_type = 'text/html'
        content = '<a    href="{}"></a>'.format(link)
        initial_response = HttpResponse(content=content, content_type=content_type)
        processed_response = self.middleware.process_response(
            request=request,
            response=initial_response,
        )

        expected = '<a    href="/external-link/?link={}&next={}"></a>'.format(
            urlencode(link, safe=''),
            path,
        )
        self.assertEqual(processed_response.content, expected.encode())
