# -*- coding: utf-8 -*-
from django.http.response import FileResponse, HttpResponse
from django.template.defaultfilters import urlencode
from django.test import TestCase
from mock import MagicMock

from rewrite_external_links.middleware import RewriteExternalLinksMiddleware


class TestRewriteExternalLinksMiddleware(TestCase):
    def setUp(self):
        self.middleware = RewriteExternalLinksMiddleware()
        self.request = MagicMock()
        self.content_type = 'text/html'
        self.link = 'http://ΣxamplΣ.com'  # get some unicode in there
        self.content = '<a    href="{}"></a>'.format(self.link).encode('utf-8')

    def test_no_response_content(self):
        """When response has no content the middleware does nothing."""
        response = HttpResponse(content_type=self.content_type)
        processed_response = self.middleware.process_response(
            request=self.request,
            response=response,
        )
        self.assertEqual(processed_response.content, b'')

    def test_streamed_response(self):
        """Streamed response should not change."""
        response = FileResponse()
        processed_response = self.middleware.process_response(
            request=self.request,
            response=response,
        )
        self.assertEqual(processed_response.getvalue(), b'')

    def test_other_content_type(self):
        """When response `Content-Type` is not `text/html` the middleware does nothing."""
        content_type = 'application/thraud+xml'
        response = HttpResponse(content=self.content, content_type=content_type)
        processed_response = self.middleware.process_response(
            request=self.request,
            response=response,
        )
        self.assertEqual(processed_response.content, self.content)

    def test_missing_content_type(self):
        """When response `Content-Type` is missing, the middleware does nothing."""
        response = HttpResponse(content=self.content)
        del response['content-type']
        processed_response = self.middleware.process_response(
            request=self.request,
            response=response,
        )
        self.assertEqual(processed_response.content, self.content)

    def test_other_request_path_info(self):
        """The middleware should not process the external link view."""
        self.request.META = {'PATH_INFO': '/external-link/'}
        response = HttpResponse(
            content=self.content,
            content_type=self.content_type,
        )
        processed_response = self.middleware.process_response(
            request=self.request,
            response=response,
        )
        self.assertEqual(processed_response.content, self.content)

    def test_response_content(self):
        """The middleware should rewrite html url links."""
        path = 'test-path'
        self.request.META = {'PATH_INFO': '/another-url/'}
        self.request.path = path
        response = HttpResponse(
            content=self.content,
            content_type=self.content_type,
        )
        processed_response = self.middleware.process_response(
            request=self.request,
            response=response,
        )

        expected = '<a    href="/external-link/?link={}&next={}"></a>'.format(
            urlencode(self.link, safe=''),
            path,
        )
        self.assertEqual(processed_response.content, expected.encode())
