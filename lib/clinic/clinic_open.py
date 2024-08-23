from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from time import sleep

# customized functions
from lib.sys_web import waitPageLoad
from lib.clinic.clinic_func import clinicPageNavi
from lib.sys_func import enterCardPw, currentDateTime

def clinicOpen(driver, url_dict, session_id, config_dict, vs_id_pw):
    ampm_text = ''
    open_count = 0
    
    try:
        date_arg = currentDateTime()
        if 7 <= int(date_arg['hour']) <= 10:
            ampm_text = '上午'
        elif 11 <= int(date_arg['hour']) <= 14:
            ampm_text = '下午'
        if not ampm_text:
            raise ValueError('非開診時間!')
        
        # Prepare clinic page navigation arguments
        clinic_arg = {
            "HOSP": url_dict['hosp_name'],
            "DEPT": url_dict['dept_name'],
            "AMPM": ampm_text,
            "YEAR": date_arg['year'],
            "MONTH": date_arg['month'],
            "DAY": date_arg['day'],
        }
        
        temp_wait = WebDriverWait(driver, 30)
        clinicPageNavi(driver, url_dict, session_id, clinic_arg)
        
        # Recheck clinic open: twice
        while open_count < 2:
            # loop over all clinic
            number = 1
            while True:
                number += 1 #第一個2開始，每次增加1
                strNum = str(number).zfill(2)
                clinicBTN = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_btn_suffix']
                clinicSTATUS = url_dict['clinic_list_prefix']+strNum+'_ClinicStatusShow'
                waitPageLoad(driver)
                try:
                    clinic_tag_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, clinicBTN)))
                    clinic_status_ele = driver.find_element(By.ID, clinicSTATUS)
                    if clinic_tag_ele and clinic_status_ele.text == '未開診':
                        try:
                            clinic_tag_ele.click()
                            waitPageLoad(driver)
                            
                            temp_wait.until(EC.presence_of_element_located((By.ID, url_dict['hca_card_obj'])))

                            start_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_start_btn'])))
                            sleep(10)
                            driver.execute_script('arguments[0].click()', start_btn)
                            sleep(0.5)
                            waitPageLoad(driver)
                            
                            if number == 2:
                                sleep(5)
                                enterCardPw(config_dict['pin_window_title'], vs_id_pw['pw'])
                                sleep(0.5)
                            
                            temp_wait.until(EC.presence_of_element_located((By.ID, url_dict['hca_card_obj'])))
                            nurse_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_nurse_btn'])))
                            driver.execute_script('arguments[0].click()', nurse_btn)
                            sleep(0.5)
                            waitPageLoad(driver)
                            
                            back_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_back_btn'])))
                            back_btn.click()
                        except (TimeoutException, NoSuchElementException, ElementNotInteractableException):
                            clinicPageNavi(driver, url_dict, session_id, clinic_arg)
                            continue
                except TimeoutException:
                    break
            open_count += 1
    
    except Exception as error:
        raise ValueError(f'clinicOpen: 自動開診設定錯誤!! {error}')
    
    finally:
        try:
            driver.quit()
        except:
            pass
    