import json
import PySimpleGUI as sg
from os.path import exists, relpath

def saveFile(filename, data):
    with open(filename, 'w', encoding="UTF-8") as file:
        file.write(str(data))

def initialConfig(config_path):
    config_dict = {
        "setup": False,
        "vs_id_path": "loginID.txt",
        "cr_id_path": "CRID.txt",
        "list_path": "List.txt",
        "phone_path": "Phonelist.txt",
        "google_secret_path": "secret.json",
        "google_token_path": "token.json",
        "google_cal_id": ['primary'],
        "url_path": "sys\web_config.txt",
        "theme": "DefaultNoMoreNagging", 
        "digi_hr": 6,
        "digi_min": 0,
        "digi_repeat": 8,
        "am_clinic_hr": 8,
        "am_clinic_min": 0,
        "pm_clinic_hr": 12,
        "pm_clinic_min": 30,
        "am_sms_hr": 9,
        "am_sms_min": 0,
        "pm_sms_hr": 16,
        "pm_sms_min": 0
    }
    data = json.dumps(config_dict)
    saveFile(config_path, data)
    return config_dict

def initialUrl(url_path):
    url_dict = {
        'portal_url': 'http://portal.ntuh.gov.tw/General/Login.aspx',
        'digisign_replace_url': 'http://ihisaw.ntuh.gov.tw/WebApplication/DigitalSignature/DSExecuteEmpReplace.aspx?SESSION=',
        'digisign_background_url': 'http://ihisaw.ntuh.gov.tw/WebApplication/DigitalSignature/BackGroundDS.aspx?SESSION=',
        'open_clinic_url': "http://hisaw.ntuh.gov.tw/WebApplication/Clinics/OpenClinicsByClinicNo.aspx?SESSION=",
        'send_sms_url': "http://ihisaw.ntuh.gov.tw/WebApplication/OtherIndependentProj/CriticalVentilator/MessageSend.aspx?SESSION=",
        'hosp_name': '總院區',
        'dept_name': '家庭醫學部',
        'hosp_list_ele': 'ddlHospital',
        'quick_menu_ele': 'rdblQuickMenu_0',
        'username_input_ele': 'txtUserID',
        'password_input_ele': 'txtPass',
        'captcha_img_ele': 'imgVerifyCode',
        'captcha_input_ele': 'txtVerifyCode',
        'submit_ele': 'imgBtnSubmitNew',
        'digi_doc_id': 'NTUHWeb1_txbEmpNO',
        'digi_update_panel': 'NTUHWeb1_UpdatePanel1',
        'digi_refresh_btn': 'NTUHWeb1_btnRefresh',
        'digi_count_text': 'NTUHWeb1_lblUnDsCnts',
        'digi_new_id': 'NTUHWeb1_txbEmpNoNew',
        'digi_tran_btn': 'NTUHWeb1_btnUpdate',
        'digi_EMR_cbx': 'NTUHWeb1_dgrEmrRecord_ctl01_cbxSelectAll',
        'digi_DRUG_cbx': 'NTUHWeb1_dgrDrugGivenRecord_ctl01_cbxSelectAll',
        'digiback_pin': 'NTUHWeb1_txbPinCode',
        'digiback_btn': 'NTUHWeb1_btnBackGroundDSByPCSC',
        'digiback_ddl_reason': "reasonDDL-id > option:nth-child(1)",
        'digiback_ddl_confirm': "body > div > div.ui-dialog-buttonpane.ui-widget-content.ui-helper-clearfix > div > button:nth-child(1)",
        'clinic_hosp_list': 'NTUHWeb1_HospDropList',
        'clinic_dept_list': 'NTUHWeb1_DeptDropList',
        'clinic_year': 'NTUHWeb1_DateTextBoxYearMonthDayInputUI1_YearInput',
        'clinic_month': 'NTUHWeb1_DateTextBoxYearMonthDayInputUI1_MonthInput',
        'clinic_day': 'NTUHWeb1_DateTextBoxYearMonthDayInputUI1_DayInput',
        'clinic_ampm_list': 'NTUHWeb1_AMPMDropList',
        'clinic_query_btn': 'NTUHWeb1_QueryScheduleList',
        'clinic_list_prefix': 'NTUHWeb1_ClinicsListGrid_ctl',
        'clinic_btn_suffix': '_LinkButtonSelect',
        'clinic_num_suffix': '_ClinicNo',
        'clinic_start_btn': 'NTUHWeb1_StartClinics',
        'clinic_nurse_btn': 'NTUHWeb1_btnNurseSave',
        'clinic_back_btn': 'NTUHWeb1_BackToTopPanel',
        'clinic_all_pt_btn': 'NTUHWeb1_CheckBoxAllPatient',
        'clinic_pt_prefix': 'NTUHWeb1_PatSimpleList_ctl',
        'clinic_pt_suffix': '_VisitSeqnoPlusName',
        'clinic_ptpage_other_func':'NTUHWeb1_ClinicsOtherFunction',
        'clinic_ptpage_change_cred':'NTUHWeb1_RepeaterPageLinkList_ctl13_LinkPageName',
        'clinic_cred_input':'NTUHWeb1_RewardEmpNoTextBoxInput',
        'clinic_cred_change_btn':'NTUHWeb1_ModifyRewardEmpNoButton',
        'clinic_cred_return_pt':'NTUHWeb1_ButtonReturnConfirmDiagnosisOrder',
        'clinic_ptpage_return':'NTUHWeb1_Return',
        'sms_phone_ele': 'NTUHWeb1_PHSTelNo',
        'sms_type_btn': 'NTUHWeb1_rdbNormal',
        'sms_msg_input': 'NTUHWeb1_MessageContent',
        'sms_send_btn': 'NTUHWeb1_btnSendSMSAndEmail',
    }
    data = json.dumps(url_dict)
    saveFile(url_path, data)
    return url_dict

def saveIdPw(person, filename):
    while True:
        layout = [[[sg.Text('請輸入'+person+'帳號密碼')],
                    [sg.Text(person+'帳號'), sg.InputText(k='-id-', s=(15,1))],
                    [sg.Text(person+'密碼'), sg.InputText(k='-pw-', s=(15,1))],
                    [sg.Text('醫事卡pin碼'), sg.InputText(k='-pin-', s=(11,1))],
                    [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('設定'+person+'帳號密碼', layout).read(close=True)
        if event == 'OK':
            if values['-id-'] !='' and values['-pw-'] !='' and values['-pin-'] !='':
                data = values['-id-'] + '\n' + values['-pw-'] + '\n' + values['-pin-']
                saveFile(filename, data)
                sg.Popup(person+'帳號密碼設定完成!')
                break
            else:
                sg.Popup('輸入資訊不完整!')
        else:
            sg.Popup('設定未完成!')
            break

def saveList(type, filename):
    try:
        with open(filename, 'r', encoding='UTF-8') as file:
            defaulttext = file.read()
    except:
        defaulttext = ''
    if type == 'sign':
        text = '簽章'
        example = '00xx55 程主任'+'\n'+'11xx73 吳大宇'
        multilinesize = (40,15)
    else:
        text = '簡訊'
        example = '097265xxx0,097265xxx1,097265xxx2,097265xxx3'
        multilinesize = (50,5)
    while True:
        layout = [[[sg.Text('請參考下列格式輸入'+text+'清單')],
                    [sg.Text(example)],
                    [sg.Multiline(defaulttext, size=multilinesize, autoscroll=True, key='-list-')],
                    [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('設定'+text+'清單', layout).read(close=True)
        if event == 'OK':
            if values['-list-'] !='':
                data = values['-list-']
                saveFile(filename, data)
                sg.Popup(text+'清單設定完成!')
                break
        else:
            sg.Popup('設定未完成!')
            break

def saveGoogleFile(google_secret_path, google_token_path):
    while True:
        layout = [[[sg.Text('請選擇Google授權檔案(至少擇一)')],
                    [sg.Text('Google Secret File: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("JSON_FILETYPE", "*.json"), ), key='-secret-')],
                    [sg.Text('Google Token File: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("JSON_FILETYPE", "*.json"), ), key='-token-')],
                    [sg.Push(),sg.OK(size=(10,1)), sg.Cancel(),sg.Push()]]]
        event, values = sg.Window('設定簽章清單', layout).read(close=True)
        if event == 'OK':
            if values['-secret-'] =='' and values['-token-'] =='':
                sg.Popup('未選擇任何檔案!!')
            else:
                if values['-secret-'] !='':
                    with open(values['-secret-']) as file:
                        data = file.readline()
                    saveFile(google_secret_path, data)
                if values['-token-'] !='':
                    with open(values['-token-']) as file:
                        data = file.readline()
                    saveFile(google_token_path, data)
                sg.Popup('Google授權檔案設定完成!')
                break
        else:
            sg.Popup('設定未完成!')
            break

def saveGoogleCalnId(googlecalid):
    if len(googlecalid)==0:
        googlecalid = ['primary']
    layout = [[[sg.Text('請輸入Google日曆ID')],
        [sg.Text('已輸入：'+str(googlecalid), key='-CALID-')],
        [sg.Text('Google日曆ID'), sg.Input(default_text=googlecalid[0], key='-googleid-', s=(20,1), do_not_clear=False)],
        [sg.Push(),sg.Button('Next', key='ADD', size=(10,1)), sg.OK(size=(10,1)), sg.Cancel(),sg.Push()]]]
    window = sg.Window('設定Google日曆ID', layout)
    while True:
        event, values = window.read()
        if event == 'OK':
            if values['-googleid-']:
                googlecalid.append(values['-googleid-'])
            if googlecalid:
                googlecalid = list(dict.fromkeys(googlecalid))
                sg.Popup('設定已完成!\n已輸入以下ID：\n'+str(googlecalid))
                return googlecalid
            else:
                sg.Popup('輸入資訊不完整!')
        if event == 'ADD':
            if values['-googleid-']:
                googlecalid.append(values['-googleid-'])
                googlecalid = list(dict.fromkeys(googlecalid))
                window['-CALID-'].update('已輸入：'+str(googlecalid))
            else:
                sg.Popup('輸入資訊不完整!')
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            return googlecalid

def changeUrlElement(url_path):
    url_dict = {}
    while True:
        try:
            with open(url_path, encoding="UTF-8") as file:
                s = file.read()
                url_dict = json.loads(s) 
        except:
            initialUrl(url_path)
        break
    while True:
        layout = [[
            [sg.Text('下列為網頁設定')],
            [sg.Column([
                *[[sg.Text(key, size=(20,1)), sg.InputText(default_text=value, size=(100,1), key=key)] for key, value in url_dict.items()]
            ], scrollable=True)],
            [sg.Push(),sg.Button('設定完成',size=(10,1),key='-OK-'), sg.Push()]
        ]]
        event, values = sg.Window('設定網頁元素', layout).read(close=True)
        if event == '-OK-':
            url_dict.update(values)
            saveFile(url_path, url_dict)
            sg.Popup('網頁元素設定完成!')
            break
        else:
            sg.Popup('設定未完成!')
            break

def openOtherFunction(config_dict):
    while True:
        layout = [[[sg.Text('請選擇檔案以開啟功能')],
                    [sg.Text('IE自動填入驗證碼: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("執行檔", "*.exe"), ), key='-autoocr-')],
                    [sg.Text('IE自動登入: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("VBS檔", "*.vbs"), ), key='-ielogin-')],
                    [sg.Text('自動改績效: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("執行檔", "*.exe"), ), key='-autocredit-')],
                    [sg.Text('查診間電話: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("執行檔", "*.exe"), ), key='-findphoneclinic-')],
                    [sg.Text('查超音波電話: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("執行檔", "*.exe"), ), key='-findphoneecho-')],
                    [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('開啟額外功能', layout).read(close=True)
        if event == 'OK':
            if values['-autoocr-'] !='':
                config_dict.update(autoocr_path = relpath(values['-autoocr-']))
            if values['-ielogin-'] !='':
                config_dict.update(login_path = relpath(values['-ielogin-']))
            if values['-autocredit-'] !='':
                config_dict.update(autocredit_path = relpath(values['-autocredit-']))
            if values['-findphoneclinic-'] !='':
                config_dict.update(findphoneclinic_path = relpath(values['-findphoneclinic-']))
            if values['-findphoneecho-'] !='':
                config_dict.update(findphoneecho_path = relpath(values['-findphoneecho-']))
            sg.Popup('額外功能設定完成!')
            break
        else:
            sg.Popup('設定未完成!')
            break

def checkFileExist(config_dict):
    if exists(config_dict['vs_id_path']) != True:
        sg.Popup('未設定VS帳號密碼!!')
        saveIdPw('VS', config_dict['vs_id_path'])
    if exists(config_dict['cr_id_path']) != True:
        sg.Popup('未設定CR帳號密碼!!')
        saveIdPw('CR', config_dict['cr_id_path'])
    if exists(config_dict['list_path']) != True:
        sg.Popup('未設定簽章清單!!')
        saveList("sign", config_dict['list_path'])
    if exists(config_dict['phone_path']) != True:
        sg.Popup('未設定簡訊清單!!')
        saveList("phone", config_dict['phone_path'])
    if (exists(config_dict['google_secret_path']) or exists(config_dict['google_token_path'])) != True:
        sg.Popup('未檢查到Google授權檔案!!')
        saveGoogleFile(config_dict['google_secret_path'], config_dict['google_token_path'])
    if len(config_dict['google_cal_id']) == 0:
        sg.Popup('未檢查到Google日曆ID!!')
        config_dict.update(google_cal_id = saveGoogleCalnId(config_dict['google_cal_id']))
    if exists(config_dict['url_path']) != True:
        sg.Popup('未檢查到網頁設定!!')
        initialUrl(config_dict['url_path'])
    sg.Popup('檢查檔案已完成!!')

def changeSysFunction():
    layout = [[[sg.Push(), sg.Text('請選擇下列功能'),sg.Push()],
                [sg.Button('變更ＣＲ帳密', key='-CHANGECR-'),sg.Button('變更簽章清單', key='-CHANGESIGN-')],
                [sg.Button('變更ＶＳ帳密', key='-CHANGEVS-'),sg.Button('變更簡訊清單', key='-CHANGESMS-')],
                [sg.Button('變更日曆ＩＤ', key='-CHANGECALID-'),sg.Button('變更授權檔案', key='-CHANGECERT-'),],
                [sg.Button('變更風格樣式', key='-CHANGETHEME-'),sg.Button('開啟額外功能', key='-OPENFUNCTION-')],
                [sg.Button('檢查系統檔案', key='-CHECKFILE-'),sg.Button('變更網址指標', key='-CHANGEURL-'),],
                [sg.Push(),sg.Button('設定完成',size=(10,1),key='-EXIT-'), sg.Push()]]]
    return sg.Window('更新系統設定', layout, finalize=True)

def saveConfig(config_dict, values, config_path):
    values.pop('-LOG-', None)
    config_dict.update(values)
    data = json.dumps(config_dict)
    saveFile(config_path, data)