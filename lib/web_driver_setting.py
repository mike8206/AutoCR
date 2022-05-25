from selenium import webdriver

def web_driver_setting(browser, driver_path, arg):
    # options
    TIMEOUT = 5

    if browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        if arg == 'max':
            chrome_options.add_argument('--start-maximized')
        # chrome driver
        driver = webdriver.Chrome(driver_path, options = chrome_options)
    elif browser == 'ie':
        ie_options = webdriver.IeOptions()
        ie_options.ignore_zoom_level = True
        if arg == '':
            pass
        # IE driver
        driver = webdriver.Ie(driver_path, options = ie_options)
    elif browser == 'edge':
        edge_option = webdriver.EdgeOptions()
        if arg == 'max':
            edge_option.add_argument('--start-maximized')
        driver = webdriver.Edge(driver_path, options= edge_option)
    driver.implicitly_wait(TIMEOUT)
    return driver