import PySimpleGUI as sg
from datetime import datetime
from pytz import timezone

# customized functions
from lib.clinic.clinic_element import getClinicListEle, getClinicDropListEle

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
        event, values = sg.Window('選擇變更診間號碼', layout, keep_on_top=True).read(close=True)
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
    while True:
        layout = [[
        [sg.Text('院區：'),sg.Combo([url_dict['hosp_name']], default_value=url_dict['hosp_name'], size=(8, 1), readonly=True, k='HOSP')],
        [sg.Text('科別：'),sg.Combo(clinic_ele_values[0], default_value=url_dict['dept_name'], size=(15, 1), readonly=True, k='DEPT')],
        [sg.Text('日期：'),sg.Text('西元'), sg.InputText(default_text=str(int(today.strftime("%Y"))), key = 'YEAR', size=(5, 1)), 
        sg.Text('年'), sg.InputText(default_text=str(int(today.strftime("%m"))), key = 'MONTH', size=(3, 1)),
        sg.Text('月'), sg.InputText(default_text=str(int(today.strftime("%d"))), key = 'DAY', size=(3, 1)),
        sg.Text('日 時段'), sg.InputCombo(clinic_ele_values[1], size=(4, 1), default_value=clinic_ele_values[1][0], readonly=True, key='AMPM')],
        [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()]
        ]]
        event, values = sg.Window('選擇變更診間日期', layout, keep_on_top=True).read(close=True)
        if event == 'OK':
            clinic_arg.update(values)
            vscredclinic = chooseClinic(driver, url_dict, session_id, clinic_arg)
            return vscredclinic
        else:
            sg.Popup('已停止改績效功能!')
            break