import PySimpleGUI as sg
from datetime import datetime
from pytz import timezone

# customized functions
from lib.clinic.clinic_element import getClinicDropListEle, clinicGetPatientList
from lib.phone.exam_query import getExamDropListEle, examGetPatientList

def clinic_patient_query(driver, url_dict, session_id):
    taiwan_taipei = timezone('Asia/Taipei')
    today = datetime.now(taiwan_taipei)
    clinic_arg = {}
    clinic_ele_values = getClinicDropListEle(driver, url_dict, session_id)

    event, values = sg.Window('查詢診間日期', [
        [sg.Text('院區：'),sg.Combo([url_dict['hosp_name']], default_value=url_dict['hosp_name'], size=(8, 1), readonly=True, k='HOSP')],
        [sg.Text('科別：'),sg.Combo(clinic_ele_values[0], default_value=url_dict['dept_name'], size=(15, 1), readonly=True, k='DEPT'), sg.Text('診號：'), sg.InputText('', size=(8,1), k='CLINIC')],
        [sg.Text('日期：'),sg.Text('西元'), sg.InputText(default_text=str(int(today.strftime("%Y"))), key = 'YEAR', size=(5, 1)), 
        sg.Text('年'), sg.InputText(default_text=str(int(today.strftime("%m"))), key = 'MONTH', size=(3, 1)),
        sg.Text('月'), sg.InputText(default_text=str(int(today.strftime("%d"))), key = 'DAY', size=(3, 1)),
        sg.Text('日 時段'), sg.InputCombo(clinic_ele_values[1], size=(4, 1), default_value=clinic_ele_values[1][0], readonly=True, key='AMPM')],
        [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()]
        ], finalize=True, keep_on_top=True).read(close=True)
    if event == 'OK':
        clinic_arg.update(values)
        patientlist = clinicGetPatientList(driver, url_dict, session_id, clinic_arg)
        return patientlist
    else:
        sg.Popup('已停止查詢病人功能!')

def exam_patient_query(driver, url_dict, session_id):
    taiwan_taipei = timezone('Asia/Taipei')
    today = datetime.now(taiwan_taipei)
    exam_arg = {}
    # [Ampm_list, Unit_list, Origin_list, Item_list]
    exam_ele_values = getExamDropListEle(driver, url_dict, session_id)

    event, values = sg.Window('查詢檢查日期', [
        [sg.Text('時段：'),sg.Combo(exam_ele_values[0], default_value=exam_ele_values[0][0], size=(8, 1), readonly=True, k='AMPM'),sg.Text('科室：'),sg.Combo(exam_ele_values[1],default_value=exam_ele_values[0][0],size=(50,1), readonly=True, k='UNIT')],
        [sg.Text('來源：'),sg.Combo(exam_ele_values[2], default_value=exam_ele_values[2][0], size=(8, 1), readonly=True, k='ORIGIN'),sg.Text('項目：'),sg.Combo(exam_ele_values[3],default_value=exam_ele_values[3][0],size=(50,1), readonly=True, k='ITEM')],
        [sg.Text('起日：'),sg.InputText(default_text=today.strftime("%Y/%m/%d"), key='DATE')],
        [sg.Push(), sg.OK(), sg.Cancel(), sg.Push()]
        ], finalize=True, keep_on_top=True).read(close=True)
    if event == 'OK':
        exam_arg.update(values)
        patientlist = examGetPatientList(driver, url_dict, session_id, exam_arg)
        return patientlist
    else:
        sg.Popup('已停止查詢病人功能!')