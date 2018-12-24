import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption('--browser', action='store', default="firefox",
                     help="Choose the browser: geckodriver, firefox, chrome, ie11, safari")

    parser.addoption('--domain_staging', action='store', default="https://stepik.org",
                     help="Pages on this domain will be considered experimental, and will be compared to production")

    parser.addoption('--domain_production', action='store', default="https://stepik.org",
                     help="Pages on this domain will be considered reference, and will be compared to staging")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    rep = outcome.get_result()
    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    extra = getattr(rep, 'extra', [])

    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call" and rep.failed:
        _gather_screenshot(item, driver, extra)
        rep.extra = extra
    return rep


@pytest.yield_fixture(scope="function")
def driver(browser):
    if browser == 'chrome':
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        capabilities = webdriver.DesiredCapabilities().CHROME
        driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capabilities)
        logger.info("browser version: %s" % driver.capabilities['version'])

    elif browser == 'firefox':
        fp = webdriver.FirefoxProfile()
        fp.set_preference("dom.disable_beforeunload", True)
        capabilities = webdriver.DesiredCapabilities().FIREFOX.copy()
        capabilities['elementScrollBehavior'] = 1
        driver = webdriver.Firefox(firefox_profile=fp, capabilities=capabilities)

    yield driver
    driver.delete_all_cookies()
    driver.quit()
    logger.info('close driver now')


@pytest.fixture(scope='module')
def browser(request):
    browser_name = request.config.getoption('browser')
    return browser_name

@pytest.fixture(scope='module')
def domain_staging(request):
    current_domain = request.config.getoption('domain_staging')
    return current_domain


@pytest.fixture(scope='module')
def domain_production(request):
    current_domain = request.config.getoption('domain_production')
    return current_domain


@pytest.fixture(scope='function')
def screenshots_cache(request):
    request.config.screenshots_cache = {"production": None, "staging": None, "diff": None}
    return request.config.screenshots_cache


def _gather_screenshot(item, driver, extra):
    request = getattr(item, '_request', None)
    pytest_html = item.config.pluginmanager.getplugin('html')
    diff = item.config.screenshots_cache['diff'].decode()
    prod = item.config.screenshots_cache['production'].decode()
    staging = item.config.screenshots_cache['staging'].decode()

    if pytest_html is not None:
        extra.append(pytest_html.extras.image(prod, 'Screenshot of production'))
        extra.append(pytest_html.extras.image(staging, 'Screenshot of staging'))
        extra.append(pytest_html.extras.image(diff, 'Difference'))
