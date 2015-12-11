from incuna_test_utils.testcases.urls import URLTestCase

from rewrite_external_links.views import external_link


class TestURLs(URLTestCase):
    def test_external_link(self):
        self.assert_url_matches_view(
            view=external_link,
            expected_url='/external-link/',
            url_name='external_link',
        )
