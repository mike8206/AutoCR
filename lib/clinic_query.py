import PySimpleGUI as sg
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime
from pytz import timezone

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

def chooseClinic(driver, url_dict, session_id, clinic_arg):
    clinc_dict = getClinicListEle(driver, url_dict, session_id, clinic_arg)
    while True:
        layout = [[
            [sg.Text('請填入績效VS ID、勾選診間號碼')],
            [sg.Text('績效VS ID：'), sg.InputText('', size=(15,1), key='CREDID')],
            [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()],
            [sg.Column([
                *[[sg.Text('診號：'), sg.Checkbox(id, size=(20,1), key=value)] for id, value in clinc_dict.items()]
            ], size=(300,500), scrollable=True)]
        ]]
        event, values = sg.Window('選擇變更診間號碼', layout, finalize=True, keep_on_top=True).read(close=True)
        if event == 'OK':
            if len(values['CREDID']) == 6:
                credid = values['CREDID']
                clinic = values
                clinic.pop('CREDID')
                choosenclinic = [key for key, val in clinic.items() if val != False]
                if choosenclinic:
                    vscredclinic = {'clinicarg': clinic_arg, 'credvsid': credid, 'cliniclist': choosenclinic}
                    return vscredclinic
                else:
                    sg.Popup('未選擇任何診別!')
            else:
                sg.Popup('請輸入正確VS績效ID!')
        else:
            sg.Popup('已停止改績效功能!')
            break

def clinic_query(driver, url_dict, session_id):
    taiwan_taipei = timezone('Asia/Taipei')
    today = datetime.now(taiwan_taipei)
    clinic_arg = {}
    clinic_ele_values = getClinicDropListEle(driver, url_dict, session_id)

    event, values = sg.Window('選擇變更診間日期', [
        [sg.Text('院區：'),sg.Combo([url_dict['hosp_name']], default_value=url_dict['hosp_name'], size=(8, 1), readonly=True, k='HOSP')],
        [sg.Text('科別：'),sg.Combo(clinic_ele_values[0], default_value=url_dict['dept_name'], size=(15, 1), readonly=True, k='DEPT')],
        [sg.Text('日期：'),sg.Text('西元'), sg.InputText(default_text=str(int(today.strftime("%Y"))), key = 'YEAR', size=(5, 1)), 
        sg.Text('年'), sg.InputText(default_text=str(int(today.strftime("%m"))), key = 'MONTH', size=(3, 1)),
        sg.Text('月'), sg.InputText(default_text=str(int(today.strftime("%d"))), key = 'DAY', size=(3, 1)),
        sg.Text('日 時段'), sg.InputCombo(clinic_ele_values[1], size=(4, 1), default_value=clinic_ele_values[1][0], readonly=True, key='AMPM')],
        [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()]
        ], finalize=True, keep_on_top=True).read(close=True)
    if event == 'OK':
        clinic_arg.update(values)
        vscredclinic = chooseClinic(driver, url_dict, session_id, clinic_arg)
        return vscredclinic
    else:
        sg.Popup('已停止改績效功能!')

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