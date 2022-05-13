from lib.wait_page_load import wait_page_load
from lib.solve_captcha import solve_captcha
from selenium.webdriver.support.ui import Select

def login(driver, url_dict, idpw): # go to NTUH portal homepage
    driver.get(url_dict['portal_url'])
    wait_page_load(driver) 
    
    # find all elements needed
    hosp_list_ele = Select(driver.find_element_by_css_selector(url_dict['hosp_list_ele']))
    quick_menu_ele = driver.find_element_by_css_selector(url_dict['quick_menu_ele'])
    username_input_ele = driver.find_element_by_css_selector(url_dict['username_input_ele'])
    password_input_ele = driver.find_element_by_css_selector(url_dict['password_input_ele'])
    captcha_img_ele = driver.find_element_by_css_selector(url_dict['captcha_img_ele'])
    captcha_input_ele = driver.find_element_by_css_selector(url_dict['captcha_input_ele'])
    submit_ele = driver.find_element_by_css_selector(url_dict['submit_ele'])
    
    retrycount = 0
    while retrycount <3:
        try:
            # solve captcha and login with credential
            hosp_list_ele.select_by_visible_text(url_dict['hosp_name'])
            wait_page_load(driver)
            username_input_ele.send_keys(idpw['id'])
            password_input_ele.send_keys(idpw['pw'])
            captcha = solve_captcha(captcha_img_ele)
            captcha_input_ele.send_keys(captcha)
            quick_menu_ele.click()
            submit_ele.click()
                        
            # return the session id
            wait_page_load(driver) 
            current_url = driver.current_url
            split_url = current_url.split("SESSION=")
            session_id = split_url[1]
            return session_id
        except:
            retrycount = retrycount +1
            continue
    raise ValueError('登入失敗已達3次!!')
