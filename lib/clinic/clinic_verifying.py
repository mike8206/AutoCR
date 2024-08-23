from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# customized functions
from lib.sys_web import waitPageLoad

def clinicVerifying(driver, session_id, args):
    temp_wait = WebDriverWait(driver, 30)
    try:
        # args = {'url', 'list_ele', 'apply_btn', 'back_btn'}
        driver.get(args['url'] + session_id)
        driver.minimize_window()
        waitPageLoad(driver)
        
        while True:
            try:
                list_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, args['list_ele'])))
                if list_ele:
                    click_ele = temp_wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '選')))
                    if click_ele:
                        click_ele.click()
                        waitPageLoad(driver)

                        apply_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, args['apply_btn'])))
                        apply_btn.click()
                        waitPageLoad(driver)

                        back_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, args['back_btn'])))
                        driver.execute_script('arguments[0].click()', back_btn)
                        waitPageLoad(driver)
                    else:
                        break
                else:
                    break
            except Exception as e:
                print(f"An error occurred during element interaction: {e}")
                break
    
    except Exception as error:
        raise ValueError(f'請假異動失敗!! {error}')
    
    finally:
        try:
            driver.quit()
        except:
            pass