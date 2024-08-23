from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# customized functions
from lib.sys_web import waitPageLoad, solveCaptcha

def login(driver, url_dict, id_pw):
    session_id = None
    retry_count = 0
    max_retries = 3
    try:
        # Set timeout limit
        temp_wait = WebDriverWait(driver, 60)

        # Go to NTUH portal homepage
        driver.get(url_dict['portal_url'])
        driver.minimize_window()
        waitPageLoad(driver) 

        # Retry mechanism
        while retry_count < max_retries:
            try:
                # Select branch
                hosp_list_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['hosp_list_ele'])))
                Select(hosp_list_ele).select_by_visible_text(url_dict['hosp_name'])
                waitPageLoad(driver)
            
                # Find all elements needed
                quick_menu_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['quick_menu_ele'])))
                username_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['username_input_ele'])))
                password_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['password_input_ele'])))
                captcha_img_ele = temp_wait.until(EC.visibility_of_element_located((By.ID, url_dict['captcha_img_ele'])))
                captcha_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['captcha_input_ele'])))
                submit_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['submit_ele'])))

                # Fill id & pw
                if username_input_ele.text != id_pw['id']:
                    username_input_ele.clear()
                    username_input_ele.send_keys(id_pw['id'])
                if password_input_ele.text != id_pw['pw']:
                    password_input_ele.clear()
                    password_input_ele.send_keys(id_pw['pw'])

                # Solve captcha and input
                captcha = solveCaptcha(captcha_img_ele)
                if captcha_input_ele.text != captcha:
                    captcha_input_ele.clear()
                    captcha_input_ele.send_keys(captcha)
                
                quick_menu_ele.click()
                submit_ele.click()
                            
                # Return the session id
                waitPageLoad(driver) 
                current_url = driver.current_url
                session_id = current_url.split("SESSION=")[1]
                return session_id
            except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as error:
                print(f"Attempt {retry_count + 1}/{max_retries} failed: {error}")
                retry_count += 1
        raise ValueError('Login failed after 3 attempts.')
    
    except Exception as error:
        raise ValueError('Login: An error occurred: %s' % error)
    
    finally:
        if retry_count >= max_retries or session_id is None:
            driver.quit()