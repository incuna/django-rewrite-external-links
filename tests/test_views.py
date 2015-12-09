from django.test import TestCase


class TestExternalLink(TestCase):
    def test_no_link(self):
        """Assert it raises an error when no link is passed."""
        response = self.client.get('/external-link/')

        self.assertEqual(response.status_code, 400)
        expected = b'No link passed, or link empty.'
        self.assertEqual(response.content, expected)

    def test_link_ajax(self):
        response = self.client.get(
            '/external-link/',
            {'link': 'http2://example.com'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertTemplateUsed(
            response,
            'rewrite_external_links/external_link_ajax.html',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['next'], '')

    def test_link(self):
        response = self.client.get('/external-link/', {'link': 'http2://example.com'})
        self.assertTemplateUsed(
            response,
            'rewrite_external_links/external_link.html',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['next'], '/')

    def test_link_next(self):
        next = 'test_next'
        response = self.client.get(
            '/external-link/',
            {'link': 'http2://example.com', 'next': next},
        )
        self.assertTemplateUsed(
            response,
            'rewrite_external_links/external_link.html',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['next'], next)
