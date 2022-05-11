from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

TIMEOUT = 5

def wait_page_load(driver):
    wait = WebDriverWait(driver, timeout=TIMEOUT)
    try:
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        return True
    except TimeoutException:
        return False