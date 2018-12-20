import pytest
from screenshots_processing import ImageComparer

BASIC_GUEST_URLS = ['/login']

class TestLayouts(object):
    @pytest.mark.parametrize('url', BASIC_GUEST_URLS)
    @pytest.mark.layout_test
    def test_basic_url_test(self, url, driver, domain_staging, domain_production, screenshots_cache):
        production_url = domain_production + url
        staging_url = domain_staging + url
        comparator = ImageComparer()
        comparator.compare_pages(driver, screenshots_cache, production_url, staging_url)