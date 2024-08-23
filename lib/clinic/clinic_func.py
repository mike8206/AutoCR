from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

# customized functions
from lib.sys_web import waitPageLoad

def clinicPageNavi(driver, url_dict, session_id, clinic_arg):
    try:        
        # set timeout limit
        temp_wait = WebDriverWait(driver, 30)

        # navigate to clinic page
        driver.get(url_dict['open_clinic_url'] + session_id)
        waitPageLoad(driver)

        # select clinic
        hosp_list_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_hosp_list'])))
        Select(hosp_list_ele).select_by_visible_text(clinic_arg['HOSP'])
        dept_list_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_dept_list'])))
        Select(dept_list_ele).select_by_visible_text(clinic_arg['DEPT'])
        ampm_list_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_ampm_list'])))
        Select(ampm_list_ele).select_by_visible_text(clinic_arg['AMPM'])
        waitPageLoad(driver)
        
        year_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_year'])))
        year_input_ele.clear()
        year_input_ele.send_keys(clinic_arg['YEAR'])
        month_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_month'])))
        month_input_ele.clear()
        month_input_ele.send_keys(clinic_arg['MONTH'])
        day_input_ele = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_day'])))
        day_input_ele.clear()
        day_input_ele.send_keys(clinic_arg['DAY'])
        clinic_query_btn = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_query_btn'])))
        clinic_query_btn.click()
        waitPageLoad(driver)
    except Exception as error:
        raise ValueError('clinic_func: clinicPageNavi error!! %s' % error)

def getClinicDropListEle(driver, url_dict, session_id):
    try:
        # set timeout limit
        temp_wait = WebDriverWait(driver, 60)

        # go to clinic page
        driver.get(url_dict['open_clinic_url'] + session_id)
        waitPageLoad(driver)
        Dept_list = []
        Ampm_list = []
        dept_dropdown = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_dept_list'])))
        Dept_list_options = Select(dept_dropdown).options
        ampm_dropdown = temp_wait.until(EC.element_to_be_clickable((By.ID, url_dict['clinic_ampm_list'])))
        Ampm_list_options = Select(ampm_dropdown).options

        # get all values
        for index in range(1, len(Dept_list_options)):
            Dept_list.append(Dept_list_options[index].text)
        for index in range(1, len(Ampm_list_options)):
            Ampm_list.append(Ampm_list_options[index].text)

        clinic_ele_values = [Dept_list, Ampm_list]
        return clinic_ele_values
    except Exception as error:
        driver.quit()
        raise ValueError('clinic_func: getClinicDropListEle: An error occurred: %s' % error)

def getClinicListEle(driver, url_dict, session_id, clinic_arg):
    try:
        clinc_dict = {}
        clinicPageNavi(driver, url_dict, session_id, clinic_arg)

        # loop over all clinic
        number = 2
        while True:
            strNum = str(number).zfill(2)
            clinicBTN = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_btn_suffix']
            clinicNUM = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_num_suffix']
            clinicDrNAME = url_dict['clinic_list_prefix']+strNum+url_dict['clinic_dr_suffix']
            try:
                clinic_tag_ele = driver.find_element(By.ID, clinicBTN)
            except:
                break
            if clinic_tag_ele:
                clinic_num_ele = driver.find_element(By.ID, clinicNUM)
                clinic_dr_ele = driver.find_element(By.ID, clinicDrNAME)
                clinc_dict.update({clinic_num_ele.text + ' '+ clinic_dr_ele.text:clinicBTN})
                number=number+1
        return clinc_dict
    except Exception as error:
        driver.quit()
        raise ValueError('clinic_func: getClinicListEle: An error occurred: %s' % error)