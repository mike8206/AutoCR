from selenium.webdriver.common.by import By

# customized functions
from lib.wait_page_load import wait_page_load

def clinic_verifying(driver, session_id, args):
    # args = {'url', 'list_ele', 'apply_btn', 'back_btn'}
    driver.get(args['url'] + session_id)
    driver.minimize_window()
    wait_page_load(driver)
    
    while True:
        try:
            wait_page_load(driver)
            list_ele = driver.find_element(By.ID, args['list_ele'])
            if list_ele:
                click_ele = driver.find_element(By.LINK_TEXT, '選')
                if click_ele:
                    click_ele.click()
                    wait_page_load(driver)
                    driver.find_element(By.ID, args['apply_btn']).click()
                    wait_page_load(driver)
                    backbtn = driver.find_element(By.ID, args['back_btn'])
                    driver.execute_script('arguments[0].click()', backbtn)
                    wait_page_load(driver)
                else:
                    break
            else:
                break
        except:
            break