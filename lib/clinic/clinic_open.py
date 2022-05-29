from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from pytz import timezone

# customized functions
from lib.wait_page_load import wait_page_load

def clinic_open(driver_ie, url_dict, session_id):
    tempWait = WebDriverWait(driver_ie, 60)
    # IE goto open clinic page
    driver_ie.get(url_dict['open_clinic_url'] + session_id)
    driver_ie.minimize_window()
    wait_page_load(driver_ie)

    hosp_list_ele = Select(driver_ie.find_element(By.ID, url_dict['clinic_hosp_list']))
    hosp_list_ele.select_by_visible_text(url_dict['hosp_name'])
    dept_list_ele = Select(driver_ie.find_element(By.ID, url_dict['clinic_dept_list']))
    dept_list_ele.select_by_visible_text(url_dict['dept_name'])
    wait_page_load(driver_ie)

    # AMPM
    ampm_list_ele = Select(driver_ie.find_element(By.ID, url_dict['clinic_ampm_list']))
    timeZone = timezone('Asia/Taipei')
    nowhour = datetime.now(timeZone).strftime('%H')
    if 7 <= int(nowhour) <= 10:
        ampm_text = '上午'
    elif 11 <= int(nowhour) <= 14 :
        ampm_text = '下午'
    else:
        raise ValueError('不是開診時間!')
    
    while ampm_list_ele.first_selected_option.text != ampm_text:
        ampm_list_ele.select_by_visible_text(ampm_text)

    query_input_ele = driver_ie.find_element(By.ID, url_dict['clinic_query_btn'])
    query_input_ele.click()
    wait_page_load(driver_ie)

    # loop over all clinic
    number = 2
    while True:
        strNum = str(number).zfill(2)
        clinicBTN = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_btn_suffix']
        try:
            wait_page_load(driver_ie)
            clinic_tag_ele = driver_ie.find_element(By.ID, clinicBTN)
            if clinic_tag_ele:
                clinic_tag_ele.click()
                wait_page_load(driver_ie)
                start_btn = tempWait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_start_btn'])))
                start_btn.click()
                wait_page_load(driver_ie)
                nurse_btn = tempWait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_nurse_btn'])))
                nurse_btn.click()
                wait_page_load(driver_ie)
                back_btn = tempWait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_back_btn'])))
                back_btn.click()
                number+=1
        except:
            break