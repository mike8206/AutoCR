from pytz import timezone
from datetime import datetime
import chardet
import json
import psutil
import pygetwindow as gw
import pyautogui as pg
import pyperclip as pc
import FreeSimpleGUI as sg
import subprocess
from os.path import relpath, exists

# customized functions
from lib.sys_initial import initialConfig, initialUrl, initialSMS

def currentDateTime():
    time_zone = timezone('Asia/Taipei')
    time_now = datetime.now(time_zone)
    date_arg = {
        'now': time_now,
        'year': str(time_now.year),
        'month': str(time_now.month).zfill(2),
        'day': str(time_now.day).zfill(2),
        'weekday': time_now.weekday(),
        'hour': str(time_now.hour).zfill(2)
    }
    return date_arg

def readFile(file_path):
    try:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        file_status = chardet.detect(file_content)
        with open(file_path, encoding=file_status['encoding']) as f:
            file_data = f.read()
        return file_data
    except Exception as error:
        raise ValueError(f"{file_path}檔案錯誤!!: {str(error)}")

def updateFile(file_path, string):
    # For log and error_log
    try:
        with open(file_path, 'a', encoding='UTF-8') as f:
            f.write(f"{string}"+"\n")
    except Exception as error:
        raise ValueError(f"Failed to update {file_path}: {str(error)}")

def saveFile(file_path, data):
    try:
        with open(file_path, 'w', encoding='UTF-8') as f:
            f.write(str(data))
    except Exception as error:
        raise ValueError(f"Failed to save {file_path}: {str(error)}")

def loadConfig(load_type, file_path):
    try:
        temp = readFile(file_path)
        config_dict = json.loads(temp)
        del temp
    except:
        if load_type == 'config':
            config_dict = initialConfig()
        elif load_type == 'url':
            config_dict = initialUrl()
        elif load_type == 'sms':
            config_dict = initialSMS()
        config_data = json.dumps(config_dict, ensure_ascii=False)
        saveFile(file_path, config_data.encode('utf-8'))
    return config_dict

def saveConfig(config_dict, values, config_path):
    try:
        values.pop('-LOG-', None)
        config_dict.update(values)
        config_data = json.dumps(config_dict, ensure_ascii=False)
        saveFile(config_path, config_data)
    except Exception as error:
        raise ValueError(f"Failed to save configuration: {str(error)}")

def checkIfProcessRunning(processName):
    try:
        #Iterate over the all the running process
        for proc in psutil.process_iter():
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        return False
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as error:
        raise ValueError(f"Failed to check running processes: {str(error)}")

def checkIfWindowTitle(title):
    try:
        window_with_title = gw.getAllTitles() #list
        if title.lower() in [t.lower() for t in window_with_title]:
            return True
    except Exception as error:
        raise ValueError(f"Failed to get window titles: {str(error)}")
    return False

def activeWindowTitle(title, number = 0):
    try:
        windows = gw.getWindowsWithTitle(title)
        if len(windows) > 0 and number < len(windows):
            window = windows[number]
            window.activate()
        else:
            pass
    except Exception as error:
        raise ValueError(f"Failed to get or activate window: {str(error)}")

def enterCardPw(window_title, pin):
    try:
        if checkIfWindowTitle(window_title):
            pc.copy(pin)
            activeWindowTitle(window_title, 0)
            pg.hotkey('ctrl','v')
            pg.press('enter')
    except Exception as error: 
        raise ValueError(f"Failed to enter card PIN: {str(error)}")


def readIdPwPin(file_path):
    try:
        id_pw_list = readFile(file_path).splitlines()
        id_pw_pin = {}
        # id pw (帳號 密碼)
        id_pw_pin['id']=id_pw_list[0]
        id_pw_pin['pw']=id_pw_list[1]
        try:
            # pin (醫事卡pin碼)
            id_pw_pin['pin']=id_pw_list[2].strip()
        except IndexError:
            id_pw_pin['pin']=''
        return id_pw_pin
    except Exception as error:
        raise ValueError(str(file_path) + " file read error: " + str(error))

def readDigiList(file_path):
    try:
        digi_list = readFile(file_path).splitlines()
        digi_dict = {}
        for line in digi_list:
            (key, val) = line.split(' ',1)
            digi_dict[key] = val
        return digi_dict
    except Exception as error:
        raise ValueError("Digital signature list file read error: " + str(error))

def readGSM(file_path):
    try:
        gsm_list = readFile(file_path).strip().removesuffix(',')
        return gsm_list
    except Exception as error:
        raise ValueError("GSM file read error: " + str(error))

def readSMStext(file_path):
    try:
        temp = readFile(file_path)
        sms_text_dict = json.loads(temp)
    except:
        sms_text_dict = initialSMS()
        temp = json.dumps(sms_text_dict, ensure_ascii=False)
        saveFile(file_path, temp)
    return sms_text_dict

def callOtherFunction(file_path):
    subprocess.Popen(file_path, cwd='func/')

def autoLogin(login_path, portal_url, id_pw_pin):
    subprocess.Popen(['wscript.exe', login_path, portal_url, id_pw_pin['id'], id_pw_pin['pw']])

def saveIdPw(person, file_path):
    try:
        id_pw_pin = readIdPwPin(file_path)
    except:
        id_pw_pin = {'id':'', 'pw':'', 'pin':''}
    while True:
        layout = [[[sg.Text('請輸入'+person+'帳號密碼')],
                    [sg.Text(person+'帳號'), sg.InputText(default_text=id_pw_pin['id'], k='-id-', s=(15,1))],
                    [sg.Text(person+'密碼'), sg.InputText(default_text=id_pw_pin['pw'], k='-pw-', s=(15,1))],
                    [sg.Text('醫事卡pin碼'), sg.InputText(default_text=id_pw_pin['pin'], k='-pin-', s=(11,1))],
                    [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('設定'+person+'帳號密碼', layout).read(close=True)
        if event == 'OK':
            if values['-id-'] !='' and values['-pw-'] !='' and values['-pin-'] !='':
                data = values['-id-'] + '\n' + values['-pw-'] + '\n' + values['-pin-']
                saveFile(file_path, data)
                sg.Popup(person+'帳號密碼設定完成!')
                break
            else:
                sg.Popup('輸入資訊不完整!')
        else:
            sg.Popup('設定未完成!')
            break

def saveList(type, file_path):
    try:
        with open(file_path, 'r', encoding='UTF-8') as file:
            defaulttext = file.read()
    except:
        defaulttext = ''
    if type == 'sign':
        text = '簽章'
        example = '00xx55 程主任'+'\n'+'11xx73 吳小宇'
        multilinesize = (40,15)
    elif type == 'sms':
        text = '簡訊'
        example = '097265xxx0,097265xxx1,097265xxx2,097265xxx3'
        multilinesize = (50,5)
    elif type == 'credit':
        text = '改績效'
        example = '程主任 00xx55'+'\n'+'蔡主任 00xx36'
        multilinesize = (40,15)
    while True:
        layout = [[[sg.Text('請參考下列格式輸入'+text+'清單')],
                    [sg.Text(example)],
                    [sg.Multiline(defaulttext, size=multilinesize, autoscroll=True, key='-list-')],
                    [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('設定'+text+'清單', layout).read(close=True)
        if event == 'OK':
            if values['-list-'] !='':
                data = values['-list-']
                saveFile(file_path, data)
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

def changeDictElement(load_type, file_path):
    temp_dict = loadConfig(load_type, file_path)
    if load_type == "url":
        window_title = '網頁元素'
    elif load_type == "sms":
        window_title = '簡訊內容'
    
    while True:
        layout = [[
            [sg.Push(),sg.Button('設定完成',size=(10,1),key='-OK-'), sg.Push()],
            [sg.Column([
                *[[sg.Text(key, size=(20,1)), sg.InputText(default_text=value, size=(100,1), key=key)] for key, value in temp_dict.items()]
            ], scrollable=True)],
        ]]
        event, values = sg.Window("設定"+window_title, layout, size=(900,700)).read(close=True)
        if event == '-OK-':
            temp_dict.update(values)
            urldata = json.dumps(temp_dict, ensure_ascii=False)
            saveFile(file_path, urldata)
            sg.Popup(window_title+'設定完成!')
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
                   [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]
        event, values = sg.Window('開啟額外功能', layout).read(close=True)
        if event == 'OK':
            if values['-autoocr-'] !='':
                config_dict.update(autoocr_path = relpath(values['-autoocr-']))
            if values['-ielogin-'] !='':
                config_dict.update(login_path = relpath(values['-ielogin-']))
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
    if exists(config_dict['vslist_path']) != True:
        sg.Popup('未設定改績效清單!!')
        saveList("credit", config_dict['vslist_path'])
    if exists(config_dict['phone_path']) != True:
        sg.Popup('未設定簡訊清單!!')
        saveList("sms", config_dict['phone_path'])
    if (exists(config_dict['google_secret_path']) or exists(config_dict['google_token_path'])) != True:
        sg.Popup('未檢查到Google授權檔案!!')
        saveGoogleFile(config_dict['google_secret_path'], config_dict['google_token_path'])
    if len(config_dict['google_cal_id']) == 0:
        sg.Popup('未檢查到Google日曆ID!!')
        config_dict.update(google_cal_id = saveGoogleCalnId(config_dict['google_cal_id']))
    sg.Popup('檢查檔案已完成!!')

def dutyModifyFunction(vs_id_path):
    id_pw = ''
    while True:
        layout = [[
            [sg.Combo(['請假確認','異動確認','門診護長確認'], size=(15,1), readonly=True, k='DUTYFUNC'), sg.OK(), sg.Cancel()]
        ]]
        event, values = sg.Window('門診請假異動', layout).read(close=True)
        if event == 'OK':
            if values['DUTYFUNC'] !='':
                func_name = values['DUTYFUNC']
                if values['DUTYFUNC'] == '門診護長確認':
                    while True:
                        event, values = sg.Window('門診護長帳密', [[[sg.Text('請輸入門診護長帳號密碼')],
                            [sg.Text('帳號：'), sg.InputText(k='-id-', s=(15,1))],
                            [sg.Text('密碼：'), sg.InputText(k='-pw-', s=(15,1))],
                            [sg.Push(), sg.OK(size=(10,1)), sg.Cancel(), sg.Push()]]]).read(close=True)
                        if event == 'OK':
                            if values['-id-'] !='' and values['-pw-'] !='':
                                id_pw = {'id': values['-id-'], 'pw': values['-pw-']}
                                duty_arg = [func_name, id_pw]
                                return duty_arg
                            else:
                                sg.Popup('未輸入完整帳號密碼!')
                        else:
                            sg.Popup('功能已停止!')
                            break
                else:
                    id_pw = readIdPwPin(vs_id_path)
                    if id_pw != '':
                        duty_arg = [func_name, id_pw]
                        return duty_arg
                    else:
                        sg.Popup('VS帳號密碼未輸入!')
                        raise ValueError('VS帳號密碼未輸入!')
            else:
                sg.Popup('未選擇功能!')
        else:
            sg.Popup('功能已停止!')
            break