from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager

from requests import get
import ddddocr

def webDriverSetting(driver_type, args = 'max'):
    try:
        if driver_type == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_argument('--disable-browser-side-navigation')
            # 2024/04/17新增
            chrome_options.add_argument("--enable-chrome-browser-cloud-management")
            chrome_options.add_argument("--enable-javascript")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # 2024/08/06新增
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            if args == 'max':
                chrome_options.add_argument('--start-maximized')
            elif args == 'headless':
                chrome_options.add_argument('--headless')
            # chrome driver
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options = chrome_options)
        elif driver_type == 'edge':
            edge_options = webdriver.EdgeOptions()
            edge_options.add_argument('--no-sandbox')
            edge_options.add_argument('disable-gpu')
            edge_options.add_argument('--allow-running-insecure-content')
            edge_options.add_argument('--ignore-certificate-errors')
            # 2024/04/17新增
            edge_options.add_argument("--enable-chrome-browser-cloud-management")
            edge_options.add_argument("--remote-allow-origins=*")
            edge_options.add_argument("--enable-javascript")
            edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # 2024/08/06新增
            edge_options.add_argument('--disable-blink-features=AutomationControlled')
            if args == 'max':
                edge_options.add_argument('--start-maximized')
            elif args == 'headless':
                edge_options.add_argument('--headless')
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options= edge_options)
        elif driver_type == 'ie':
            ie_options = webdriver.IeOptions()
            ie_options.ignore_zoom_level = True
            ie_options.native_events = False
            # IE driver
            driver = webdriver.Ie(service=IEService(IEDriverManager().install()), options = ie_options)
        driver.implicitly_wait(30)
        return driver
    except Exception as error:
        raise ValueError('sys_web: webDriverSetting 錯誤!! %s' % error)

def callWebDriver(config_dict, args):
    if config_dict['hide_web']:
        args = 'headless'
    driver_type = 'edge'
    driver = webDriverSetting(driver_type, args)
    if not driver:
        driver_type = 'chrome'
        driver = webDriverSetting(driver_type, args)
        if not driver:
            driver_type = 'ie'
            driver = webDriverSetting(driver_type, args)
            if not driver:
                raise ValueError('sys_web: callWebDriver 錯誤!!')
    return driver

def callWebDriverIE(config_dict, args):
    driver_type = 'ie'
    driver = webDriverSetting(driver_type, args)
    if not driver:
        raise ValueError('sys_web: callWebDriverIE 錯誤!!')
    return driver

def waitPageLoad(driver):
    wait = WebDriverWait(driver, timeout=30)
    try:
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        return True
    except TimeoutException:
        return False

def downloadFile(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }
        response = get(url, headers=headers)
        img_bytes = response.content
        return img_bytes
    except Exception as error:
        raise ValueError('sys_web: downloadFile錯誤!! %s' % error)

def solveCaptcha(captcha_img_ele):
    try:
        img_bytes = downloadFile(captcha_img_ele.get_attribute('src'))
        ocr = ddddocr.DdddOcr(show_ad=False)
        captcha = ocr.classification(img_bytes)
        return captcha
    except Exception as error:
        raise ValueError('sys_web: solve_captcha錯誤!! %s' % error)