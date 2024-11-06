import pytest
import json
from playwright.sync_api import sync_playwright

# Load configuration data from config.json
with open("config.json") as config_file:
    config = json.load(config_file)

@pytest.fixture(scope="session")
def browser_context():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="session")
def config_data():
    # Make the configuration data available as a fixture
    return config
