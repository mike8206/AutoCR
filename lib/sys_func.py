import json
import subprocess
import PySimpleGUI as sg
from os.path import relpath, exists

# customized functions
from lib.sys_initial import initialUrl

def readIdPwPin(file):
    try:
        with open(file, encoding="UTF-8") as f:
            idpwlist = f.read().splitlines()
            idpwpin = {}
            # id pw (帳號 密碼)
            idpwpin['id']=idpwlist[0]
            idpwpin['pw']=idpwlist[1]
            try:
                # pin (醫事卡pin碼)
                idpwpin['pin']=idpwlist[2]
            except:
                pass
            return idpwpin
    except:
        raise ValueError(str(file)+'檔案錯誤!!')

def saveFile(filename, data):
    with open(filename, 'w', encoding="UTF-8") as file:
        file.write(str(data))

def saveConfig(config_dict, values, config_path):
    values.pop('-LOG-', None)
    config_dict.update(values)
    data = json.dumps(config_dict, ensure_ascii=False)
    saveFile(config_path, data)

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
                window.close()
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
            sg.Popup('取消Google日曆ID設定!')
            window.close()
            return googlecalid

def changeUrlElement(url_path):
    url_dict = {}
    while True:
        try:
            with open(url_path, encoding="UTF-8") as file:
                s = file.read()
                url_dict = json.loads(s)
                if url_dict != {}:
                    break
                else:
                    initialUrl(url_path)
        except:
            initialUrl(url_path)
    while True:
        layout = [[
            [sg.Push(),sg.Button('設定完成',size=(10,1),key='-OK-'), sg.Push()],
            [sg.Column([
                *[[sg.Text(key, size=(20,1)), sg.InputText(default_text=value, size=(100,1), key=key)] for key, value in url_dict.items()]
            ], scrollable=True)],
        ]]
        event, values = sg.Window('設定網頁元素', layout, size=(900,700)).read(close=True)
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
                    [sg.Text('晨科會排班: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("執行檔", "*.exe"), ), key='-monthsched-')],
                    [sg.Text('一鍵搬影片: ')],
                    [sg.Text(), sg.FileBrowse(file_types=(("執行檔", "*.exe"), ), key='-movevideo-')],
                    [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('開啟額外功能', layout).read(close=True)
        if event == 'OK':
            if values['-autoocr-'] !='':
                config_dict.update(autoocr_path = relpath(values['-autoocr-']))
            if values['-ielogin-'] !='':
                config_dict.update(login_path = relpath(values['-ielogin-']))
            if values['-monthsched-'] !='':
                config_dict.update(monthsched_path = relpath(values['-monthsched-']))
            if values['-movevideo-'] !='':
                config_dict.update(movevideo_path = relpath(values['-movevideo-']))
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

def autoOCR(autoocr_path):
    subprocess.Popen(autoocr_path)

def autoLogin(login_path, portal_url, idpwpin):
    try:
        subprocess.Popen(['wscript.exe', login_path, portal_url, idpwpin['id'], idpwpin['pw']])
    except Exception as error:
        raise ValueError('自動登入出現錯誤!! %s' % error)

def dutyModify(config_dict):
    idpw = ''
    while True:
        layout = [[
            [sg.Combo(['請假確認','異動確認','門診護長確認'], size=(15,1), readonly=True, k='DUTYFUNC'), sg.OK(), sg.Cancel()]
        ]]
        event, values = sg.Window('門診請假異動', layout).read(close=True)
        if event == 'OK':
            if values['DUTYFUNC'] !='':
                funcname = values['DUTYFUNC']
                if values['DUTYFUNC'] == '門診護長確認':
                    while True:
                        event, values = sg.Window('門診護長帳密', [[[sg.Text('請輸入門診護長帳號密碼')],
                            [sg.Text('帳號：'), sg.InputText(k='-id-', s=(15,1))],
                            [sg.Text('密碼：'), sg.InputText(k='-pw-', s=(15,1))],
                            [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]).read(close=True)
                        if event == 'OK':
                            if values['-id-'] !='' and values['-pw-'] !='':
                                idpw = {'id': values['-id-'], 'pw': values['-pw-']}
                                data = [funcname, idpw]
                                return data
                            else:
                                sg.Popup('未輸入完整帳號密碼!')
                        else:
                            sg.Popup('功能已停止!')
                            break
                else:
                    idpw = readIdPwPin(config_dict['vs_id_path'])
                    if idpw != '':
                        data = [funcname, idpw]
                        return data
                    else:
                        sg.Popup('VS帳號密碼未輸入!')
                        raise ValueError('VS帳號密碼未輸入!')
            else:
                sg.Popup('未選擇功能!')
        else:
            sg.Popup('功能已停止!')
            break