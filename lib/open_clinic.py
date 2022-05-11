from lib.wait_page_load import wait_page_load
from selenium.webdriver.support.ui import Select
from datetime import datetime
from pytz import timezone

# AMPM
taiwan_taipei = timezone('Asia/Taipei')
today = datetime.now(taiwan_taipei)
nowhour = today.strftime("%H")

def open_clinic(driver_ie, url_dict, session_id):
    # IE goto open clinic page
    driver_ie.get(url_dict['open_clinic_url'] + session_id)
    driver_ie.minimize_window()
    wait_page_load(driver_ie)

    # find all elements needed
    hosp_list_ele = Select(driver_ie.find_element_by_css_selector(url_dict['clinic_hosp_list']))
    dept_list_ele = Select(driver_ie.find_element_by_css_selector(url_dict['clinic_dept_list']))
    ampm_list_ele = Select(driver_ie.find_element_by_css_selector(url_dict['clinic_ampm_list']))
    query_input_ele = driver_ie.find_element_by_css_selector(url_dict['clinic_query_btn'])

    # select clinic & AMPM
    hosp_list_ele.select_by_visible_text(url_dict['hosp_name'])
    dept_list_ele.select_by_visible_text(url_dict['dept_name'])
    if 7 <= int(nowhour) <= 10:
        ampm_list_ele.select_by_visible_text('上午')
    elif 11 <= int(nowhour) <= 14 :
        ampm_list_ele.select_by_visible_text('下午')
    else:
        raise ValueError('不是開診時間!')

    query_input_ele.click()
    wait_page_load(driver_ie)

    # loop over all clinic
    number = 2
    while True:
        strNum = str(number).zfill(2)
        clinicID = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_list_suffix']
        try:
            clinic_tag_ele = driver_ie.find_element_by_css_selector(clinicID)
        except:
            break
        if clinic_tag_ele:
            clinic_tag_ele.click()
            wait_page_load(driver_ie)

            driver_ie.find_element_by_css_selector(url_dict['clinic_start_btn']).click()
            wait_page_load(driver_ie)

            driver_ie.find_element_by_css_selector(url_dict['clinic_nurse_btn']).click()
            wait_page_load(driver_ie)

            driver_ie.find_element_by_css_selector(url_dict['clinic_back_btn']).click()
            wait_page_load(driver_ie)
            number=number+1
    driver_ie.quit()
