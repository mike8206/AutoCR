from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# customized functions
from lib.wait_page_load import wait_page_load

def getClinicDropListEle(driver, url_dict, session_id):
    driver.get(url_dict['open_clinic_url'] + session_id)
    wait_page_load(driver)
    Dept_list = []
    Ampm_list = []
    dept_dropdown = Select(driver.find_element(By.ID, url_dict['clinic_dept_list']))
    Dept_list_options = dept_dropdown.options
    ampm_dropdown = Select(driver.find_element(By.ID, url_dict['clinic_ampm_list']))
    Ampm_list_options = ampm_dropdown.options

    # get all values
    for index in range(1, len(Dept_list_options)):
        Dept_list.append(Dept_list_options[index].text)
    for index in range(1, len(Ampm_list_options)):
        Ampm_list.append(Ampm_list_options[index].text)

    clinic_ele_values = [Dept_list, Ampm_list]
    return clinic_ele_values

def getClinicListEle(driver, url_dict, session_id, clinic_arg):
    driver.get(url_dict['open_clinic_url'] + session_id)
    wait_page_load(driver)
    clinc_dict = {}
    
    # find all elements
    Select(driver.find_element(By.ID, url_dict['clinic_hosp_list'])).select_by_visible_text(clinic_arg['HOSP'])
    Select(driver.find_element(By.ID, url_dict['clinic_dept_list'])).select_by_visible_text(clinic_arg['DEPT'])
    Select(driver.find_element(By.ID, url_dict['clinic_ampm_list'])).select_by_visible_text(clinic_arg['AMPM'])
    year_input_ele = driver.find_element(By.ID, url_dict['clinic_year'])
    month_input_ele = driver.find_element(By.ID, url_dict['clinic_month'])
    day_input_ele = driver.find_element(By.ID, url_dict['clinic_day'])
    year_input_ele.clear()
    month_input_ele.clear()
    day_input_ele.clear()
    year_input_ele.send_keys(clinic_arg['YEAR'])
    month_input_ele.send_keys(clinic_arg['MONTH'])
    day_input_ele.send_keys(clinic_arg['DAY'])
    driver.find_element(By.ID, url_dict['clinic_query_btn']).click()
    wait_page_load(driver)

    # loop over all clinic
    number = 2
    while True:
        strNum = str(number).zfill(2)
        clinicBTN = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_btn_suffix']
        clinicNUM = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_num_suffix']
        try:
            clinic_tag_ele = driver.find_element(By.ID, clinicBTN)
        except:
            break
        if clinic_tag_ele:
            clinic_num_ele = driver.find_element(By.ID, clinicNUM)
            clinc_dict.update({clinic_num_ele.text:clinicBTN})
            number=number+1
    return clinc_dict

def clinicGetPatientList(driver, url_dict, session_id, clinic_arg):
    driver.get(url_dict['open_clinic_url'] + session_id)
    driver.minimize_window()
    wait_page_load(driver)
    
    # find all elements
    Select(driver.find_element(By.ID, url_dict['clinic_hosp_list'])).select_by_visible_text(clinic_arg['HOSP'])
    Select(driver.find_element(By.ID, url_dict['clinic_dept_list'])).select_by_visible_text(clinic_arg['DEPT'])
    Select(driver.find_element(By.ID, url_dict['clinic_ampm_list'])).select_by_visible_text(clinic_arg['AMPM'])
    year_input_ele = driver.find_element(By.ID, url_dict['clinic_year'])
    month_input_ele = driver.find_element(By.ID, url_dict['clinic_month'])
    day_input_ele = driver.find_element(By.ID, url_dict['clinic_day'])
    clinic_input_ele = driver.find_element(By.ID, url_dict['clinic_num_input'])
    year_input_ele.clear()
    month_input_ele.clear()
    day_input_ele.clear()
    clinic_input_ele.clear()
    year_input_ele.send_keys(clinic_arg['YEAR'])
    month_input_ele.send_keys(clinic_arg['MONTH'])
    day_input_ele.send_keys(clinic_arg['DAY'])
    clinic_input_ele.send_keys(clinic_arg['CLINIC'])
    driver.find_element(By.ID, url_dict['clinic_query_btn']).click()
    wait_page_load(driver)

    try:
        driver.find_element(By.ID, url_dict['clinic_pt_detail_btn']).click()
        wait_page_load(driver)
        pt_detail_ele = driver.find_element(By.ID, url_dict['clinic_pt_detail']).text
        temp_list = pt_detail_ele.splitlines()
        patientlist = []
        for items in temp_list:
            patientlist.append(items.split(' ')[1])
        return patientlist
    except:
        raise ValueError('查無診間或病人!')