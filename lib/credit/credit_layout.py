import FreeSimpleGUI as sg

# customized functions
from lib.sys_func import currentDateTime
from lib.clinic.clinic_func import getClinicDropListEle, getClinicListEle

def clinicQuery(driver, url_dict, session_id):
    clinic_arg = {}
    date_arg = currentDateTime()
    clinic_ele_values = getClinicDropListEle(driver, url_dict, session_id)
    clinic_query_layout = [[
        [sg.Text('院區：'),sg.Combo([url_dict['hosp_name']], default_value=url_dict['hosp_name'], size=(8, 1), readonly=True, k='HOSP')],
        [sg.Text('科別：'),sg.Combo(clinic_ele_values[0], default_value=url_dict['dept_name'], size=(15, 1), readonly=True, k='DEPT')],
        [sg.Text('日期：'),
         sg.Text('西元'), sg.InputText(default_text=date_arg['year'], key = 'YEAR', size=(5, 1)), sg.Text('年'), 
         sg.InputText(default_text=date_arg['month'], key = 'MONTH', size=(3, 1)), sg.Text('月'), 
         sg.InputText(default_text=date_arg['day'], key = 'DAY', size=(3, 1)), sg.Text('日 時段'), 
         sg.InputCombo(clinic_ele_values[1], size=(4, 1), default_value=clinic_ele_values[1][0], readonly=True, key='AMPM')],
        [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()]
        ]]
    
    clinic_query_window = sg.Window('選擇變更診間日期', clinic_query_layout, keep_on_top=True)

    while True:
        event, values = clinic_query_window.read(close=True)
        if event == 'OK':
            clinic_arg.update(values)
            return clinic_arg
        else:
            sg.Popup('已停止改績效功能!')
            driver.quit()
            break
    
def chooseClinic(driver, url_dict, session_id, clinic_arg, vsiddict):
    vscredclinic = {}
    clinc_dict = getClinicListEle(driver, url_dict, session_id, clinic_arg)
    choose_clinic_layout = [[
        [sg.Text('請填入績效VS、勾選診間號碼')],
        [sg.Text('西元：'),sg.Text(str(clinic_arg['YEAR'])), sg.Text('年'),
         sg.Text(str(clinic_arg['MONTH'])),sg.Text('月'), 
         sg.Text(str(clinic_arg['DAY'])),sg.Text('日 '),
         sg.Text(clinic_arg['AMPM'])],
        [sg.Text('績效VS：'), sg.Combo(list(vsiddict.keys()), default_value=None, readonly=True, size=(15,1), key='CREDDR')],
        [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()],
        [sg.Column([
            *[[sg.Text('診間：'), sg.Checkbox(id, size=(20,1), key=value)] for id, value in clinc_dict.items()]
        ], size=(300,500), scrollable=True)]
        ]]
    
    chooseClinic_window = sg.Window('選擇變更診間號碼', choose_clinic_layout, keep_on_top=True)

    while True:
        event, values = chooseClinic_window.read(close=True)
        if event == 'OK':
            if values['CREDDR'] != '':
                credid = vsiddict[values['CREDDR']][:6]
                clinic = values
                clinic.pop('CREDDR')
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
            driver.quit()
            break