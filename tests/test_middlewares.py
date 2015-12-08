from django.http.response import HttpResponse
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
        self.assertEqual(processed_response, initial_response)

    def test_other_content_type(self):
        """response doesn't change if `Content-Type` is not `text/html`."""
        request = MagicMock()
        content_type = 'application/thraud+xml'
        initial_response = HttpResponse(content=b'0x0', content_type=content_type)
        processed_response = self.middleware.process_response(
            request=request,
            response=initial_response,
        )
        self.assertEqual(processed_response, initial_response)

    def test_other_request_path_info(self):
        request = MagicMock()
        request.META['PATH_INFO'] = '/another-url/'
        content_type = 'text/html'
        initial_response = HttpResponse(content=b'0x0', content_type=content_type)
        processed_response = self.middleware.process_response(
            request=request,
            response=initial_response,
        )
        self.assertEqual(processed_response, initial_response)
