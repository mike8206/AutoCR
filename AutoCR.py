from datetime import datetime
from os.path import exists
import subprocess
import PySimpleGUI as sg
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import json
from lib import autodigisign, autoopenclinic, autosms, sysfunction

# file path
config_path = 'sys\config.txt'
log_path = 'sys\log.txt'
error_log_path = 'sys\error_log.txt'
chrome_driver_path = 'sys\chromedriver.exe'
ie_driver_path = 'sys\IEDriverServer32.exe'

# options
config_dict={}
url_dict={}
values={}

try:
    with open(config_path, encoding="UTF-8") as file:
        s = file.read()
        config_dict = json.loads(s)
except:
    config_dict = sysfunction.initialconfig(config_path)

try:
    with open(config_dict['url_path'], encoding="UTF-8") as file:
        s = file.read()
        url_dict = json.loads(s)
except:
    url_dict = sysfunction.initialurl(config_dict['url_path'])

# functions
def digisign():
    autodigisign.main(url_dict, config_dict['vs_id_path'], config_dict['list_path'], chrome_driver_path, ie_driver_path)

def openclnc():
    autoopenclinic.main(url_dict, config_dict['vs_id_path'], chrome_driver_path, ie_driver_path)

def sms():
    autosms.main(url_dict, config_dict['cr_id_path'], config_dict['phone_path'], config_dict['google_secret_path'], config_dict['google_token_path'], config_dict['google_cal_id'], chrome_driver_path)

# main function
def main():
    switch_digisign = False
    switch_clinic = False
    switch_sms = False

    def listener(event):
        job_id = event.job_id
        try:
            job_time = scheduler.get_job(job_id=job_id).next_run_time
        except:
            job_time = "無"
        if event.exception:
            logstring = str(datetime.now().strftime("%m/%d %H:%M:%S"))+" "+ job_id+' 失敗! 已儲存錯誤紀錄!'
            error_msg = str(datetime.now().strftime("%m/%d %H:%M:%S"))+" "+ str(event.exception)
            error_log(error_msg)
        else:
            logstring = str(datetime.now().strftime("%m/%d %H:%M:%S"))+" "+ job_id+' 成功執行! 下次執行時間: '+ str(job_time)
        update_log(logstring)

    def update_log(logstring):
        with open(log_path, 'a', encoding="UTF-8") as file:
            file.write(logstring+"\n")
        with open(log_path, 'r', encoding="UTF-8") as file: 
            console_log = file.read()
            window1['-LOG-'].update(console_log)

    def error_log(error_msg):
        with open(error_log_path, 'a', encoding="UTF-8") as file:
            file.write(error_msg+"\n")
        
    def schdlr_cron_format(hr, min, hrrepeat):
        hr = hr % 24
        min = min % 60
        if hrrepeat != 24:
            hr = (hr + hrrepeat) % 24
            hr = hr % hrrepeat
            cronhr = str(int(hr))+'/'+str(int(hrrepeat))
        else:
            cronhr = str(int(hr))
        cron_format = str(int(min))+" "+cronhr+" * * *"
        return cron_format

    def digisign_switch_schdlr(onoff, digihr, digimin, digirepeat):
        if onoff == True:
            sg.Popup('自動簽章已開啟!')
            cron_format = schdlr_cron_format(digihr, digimin, digirepeat)
            scheduler.add_job(digisign, CronTrigger.from_crontab(cron_format, timezone='Asia/Taipei'), id='自動簽章', replace_existing=True)
        else:
            sg.Popup('自動簽章已關閉!')
            scheduler.remove_job(job_id='自動簽章')

    def openclnc_switch_schdlr(onoff, amhr, ammin, pmhr, pmmin):
        if onoff == True:
            sg.Popup('自動開診已開啟!')
            scheduler.add_job(openclnc, trigger='cron', id='上午自動開診', day_of_week='mon-fri', hour=amhr, minute=ammin, timezone='Asia/Taipei', replace_existing=True)
            scheduler.add_job(openclnc, trigger='cron', id='下午自動開診', day_of_week='mon-fri', hour=pmhr, minute=pmmin, timezone='Asia/Taipei', replace_existing=True)
        else:
            sg.Popup('自動開診已關閉!')
            scheduler.remove_job(job_id='上午自動開診')
            scheduler.remove_job(job_id='下午自動開診')

    def sms_switch_schdlr(onoff, amhr, ammin, pmhr, pmmin):
        if onoff == True:
            sg.Popup('自動寄簡訊已開啟!')
            scheduler.add_job(sms, trigger='cron', id='上午自動寄簡訊', day_of_week='mon-fri', hour=amhr, minute=ammin, timezone='Asia/Taipei', replace_existing=True)
            scheduler.add_job(sms, trigger='cron', id='下午自動寄簡訊', day_of_week='mon-fri', hour=pmhr, minute=pmmin, timezone='Asia/Taipei', replace_existing=True)
        else:
            sg.Popup('自動寄簡訊已關閉!')
            scheduler.remove_job(job_id='上午自動寄簡訊')
            scheduler.remove_job(job_id='下午自動寄簡訊')

    # GUI layout
    def make_window(config_dict):
        sg.theme(config_dict["theme"])    

        # layout part
        digisign_col = sg.Column([
            [sg.Frame('自動簽章', layout=[
                [sg.Push(), sg.Image("sys/digisign.png"), sg.Push()],
                [sg.Push(), sg.Button('手動執行', key='-RUNDIGISIGN-')],
                [sg.Frame('定時器',layout=[
                    [sg.Text('每日執行')],
                    [sg.InputCombo([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22], size=(3, 3), default_value=config_dict['digi_hr'], readonly=True, key='digi_hr'), sg.Text('時'),
                    sg.InputCombo([0, 15, 30, 45], size=(3, 3), default_value=config_dict['digi_min'], readonly=True, key='digi_min'), sg.Text('分')],
                    [sg.Text('每'),sg.InputCombo([2, 4, 6, 8, 12, 24], size=(3, 3), default_value=config_dict['digi_repeat'], readonly=True, key='digi_repeat'),sg.Text('小時重複')],
                    [sg.Push(), sg.Button('加入排程', button_color=('white', 'green'), key='-DIGISIGNSWITCH-'), sg.Push()],
                    ])]
            ])]
        ])

        open_clinic_col = sg.Column([
            [sg.Frame('自動開診', layout=[
                [sg.Push(), sg.Image("sys/clinic.png"), sg.Push()],
                [sg.Push(), sg.Button('手動執行', key='-RUNOPENCLNC-')],
                [sg.Frame('定時器',layout=[
                    [sg.Text('每周一至每周五')],
                    [sg.InputCombo([7, 8, 9], size=(3, 3), default_value=config_dict['am_clinic_hr'], readonly=True, key='am_clinic_hr'), sg.Text('時'),
                    sg.InputCombo([0, 15, 30, 45], size=(3, 3), default_value=config_dict['am_clinic_min'], readonly=True, key='am_clinic_min'), sg.Text('分')],
                    [sg.InputCombo([11, 12, 13], size=(3, 3), default_value=config_dict['pm_clinic_hr'], readonly=True, key='pm_clinic_hr'), sg.Text('時'),
                    sg.InputCombo([0, 15, 30, 45], size=(3, 3), default_value=config_dict['pm_clinic_min'], readonly=True, key='pm_clinic_min'), sg.Text('分')],
                    [sg.Push(), sg.Button('加入排程', button_color=('white', 'green'), key='-CLINICSWITCH-'), sg.Push()],
                    ])]
            ])]
        ])

        sms_col = sg.Column([
            [sg.Frame('自動寄簡訊', layout=[
                [sg.Push(),sg.Image("sys/sms.png"),sg.Push()],
                [sg.Push(),sg.Button('手動執行', key='-RUNSMS-')],
                [sg.Frame('定時器',layout=[
                    [sg.Text('每周一至每周五')],
                    [sg.InputCombo([8, 9], size=(3, 3), default_value=config_dict['am_sms_hr'], readonly=True, key='am_sms_hr'), sg.Text('時'),
                    sg.InputCombo([0, 15, 30, 45], size=(3, 3), default_value=config_dict['am_sms_min'], readonly=True, key='am_sms_min'), sg.Text('分')],
                    [sg.InputCombo([16, 17], size=(3, 3), default_value=config_dict['pm_sms_hr'], readonly=True, key='pm_sms_hr'), sg.Text('時'),
                    sg.InputCombo([0, 15, 30, 45], size=(3, 3), default_value=config_dict['pm_sms_min'], readonly=True, key='pm_sms_min'), sg.Text('分')],
                    [sg.Push(), sg.Button('加入排程', button_color=('white', 'green'), key='-SMSSWITCH-'),sg.Push()],
                    ])]
            ])]
        ])

        sys_col = sg.Column([
            [sg.Frame('系統設定', layout=[
                [sg.Button('變更設定', key='-CHANGESYS-')],
                [sg.Button('儲存設定', key='-SAVECONFIG-')],
                [sg.Button('結束程式', key='-EXIT-')],
            ]),
            sg.Frame('執行結果', layout=[
                [sg.Multiline(size=(80, 4), disabled=True, autoscroll=True , auto_refresh=True, key='-LOG-')],
                [sg.Push(), sg.Text('Version: 1.0.2, Credit by: 吳璨宇, 2022/05/10')]
            ])]
        ])

        other_col = sg.Column([
            [sg.Frame('常用功能', layout=[
                [sg.Button('自動驗證碼', key='-AUTOOCR-', size=(10,1))],
                [sg.Button('小ＣＲ登入', key='-CRLOGIN-', size=(10,1))],
                [sg.Button('ＶＳ登入', key='-VSLOGIN-', size=(10,1))],
                [sg.Button('自動改績效', key='-AUTOCREDIT-', size=(10,1))],
            ])],
            [sg.Frame('其他功能', layout=[
                [sg.Button('查診間電話', key='-FINDPHONECLINIC-', size=(10,1))],
                [sg.Button('查超音波電話', key='-FINDPHONEECHO-', size=(10,1))],
            ])],
        ], vertical_alignment='t')

        layout = [[[digisign_col,open_clinic_col,sms_col,other_col],[sys_col]]]
        return sg.Window('全自動小CR', layout, finalize=True)

    # initial setup
    if config_dict['setup'] == False:
        sysfunction.check_file_exist(config_dict)
        config_dict.update(setup = True)

    scheduler = BackgroundScheduler()
    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    window1, window2 = make_window(config_dict), None

    while True:
        window, event, values = sg.read_all_windows(timeout=100)
        if event == '-EXIT-':
            window.close()
            if window == window2:
                window2 = None
                window1 = make_window(config_dict)
            elif window == window1:
                sysfunction.save_config(config_dict, values, config_path)
                break
        if scheduler.running != True:
            scheduler.start()
        if event == '-RUNDIGISIGN-':
            scheduler.add_job(digisign, id='手動執行自動簽章')
        if event == '-RUNOPENCLNC-':
            scheduler.add_job(openclnc, id='手動執行自動開診')
        if event == '-RUNSMS-':
            scheduler.add_job(sms, id='手動執行自動寄簡訊')
        if event == '-DIGISIGNSWITCH-':
            switch_digisign = not switch_digisign
            window.Element('-DIGISIGNSWITCH-').Update(('加入排程','刪除排程')[switch_digisign], button_color=(('white', ('green','red')[switch_digisign])))
            digisign_switch_schdlr(switch_digisign, values['digi_hr'], values['digi_min'], values['digi_repeat'])
        if event == '-CLINICSWITCH-':
            switch_clinic = not switch_clinic
            window.Element('-CLINICSWITCH-').Update(('加入排程','刪除排程')[switch_clinic], button_color=(('white', ('green','red')[switch_clinic])))
            openclnc_switch_schdlr(switch_clinic, values['am_clinic_hr'], values['am_clinic_min'], values['pm_clinic_hr'], values['pm_clinic_min'])
        if event == '-SMSSWITCH-':
            switch_sms = not switch_sms
            window.Element('-SMSSWITCH-').Update(('加入排程','刪除排程')[switch_sms], button_color=(('white', ('green','red')[switch_sms])))
            sms_switch_schdlr(switch_sms, values['am_sms_hr'], values['am_sms_min'], values['pm_sms_hr'], values['pm_sms_min'])
        if event == '-AUTOOCR-':
            try:
                if exists(config_dict['autoocr_path']):
                    subprocess.Popen([config_dict['autoocr_path']])
            except:
                sg.Popup('尚未實裝!')
        if event in ('-VSLOGIN-', '-CRLOGIN-'):
            try:
                if exists(config_dict['login_path']):
                    idpwpin = []
                    if event == '-VSLOGIN-':
                        with open(config_dict['vs_id_path'], encoding="UTF-8") as f:
                            idpwpin = f.read().splitlines()
                    if event == '-CRLOGIN-':
                        with open(config_dict['cr_id_path'], encoding="UTF-8") as f:
                            idpwpin = f.read().splitlines()
                    subprocess.Popen(['wscript.exe', config_dict['login_path'], url_dict['portal_url'], idpwpin[0], idpwpin[1] ])
            except:
                sg.Popup('尚未實裝!')
        if event == '-AUTOCREDIT-':
            try:
                if exists(config_dict['autocredit_path']):
                    subprocess.Popen([config_dict['autocredit_path']])
            except:
                sg.Popup('尚未實裝!')
        if event == '-FINDPHONECLINIC-':
            try:
                if exists(config_dict['findphoneclinic_path']):
                    subprocess.Popen([config_dict['findphoneclinic_path']])
            except:
                sg.Popup('尚未實裝!')
        if event == '-FINDPHONEECHO-':
            try:
                if exists(config_dict['findphoneecho_path']):
                    subprocess.Popen([config_dict['findphoneecho_path']])
            except:
                sg.Popup('尚未實裝!')
        if event == '-SAVECONFIG-':
            sysfunction.save_config(config_dict, values, config_path)
            sg.Popup("已成功儲存設定!")
        if event == '-CHANGESYS-' and not window2:
            window2 = sysfunction.change_sys()
            window.close()
        if event == '-CHANGEVS-':
            sysfunction.saveidpw('VS', config_dict['vs_id_path'])
        if event == '-CHANGECR-':
            sysfunction.saveidpw('CR', config_dict['cr_id_path'])
        if event == '-CHANGESIGN-':
            sysfunction.savelist("sign", config_dict['list_path'])
        if event == '-CHANGESMS-':
            sysfunction.savelist("phone", config_dict['phone_path'])
        if event == '-CHANGECALID-':
            config_dict.update(google_cal_id = sysfunction.savegooglecalid())
        if event == '-CHANGECERT-':
            sysfunction.savegooglefile(config_dict['google_secret_path'], config_dict['google_token_path'])
        if event == '-CHANGETHEME-':
            event, values = sg.Window('變更風格', [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME LIST-'), sg.OK(), sg.Cancel()]], finalize=True).read(close=True)
            if values['-THEME LIST-'] !='' and values['-THEME LIST-'] != sg.theme():
                config_dict['theme'] = sg.theme(values['-THEME LIST-'])
        if event == '-OPENFUNCTION-':
            sysfunction.openotherfunction(config_dict)
        if event == '-CHECKFILE-':
            sg.Popup("重新檢測檔案!")
            sysfunction.check_file_exist(config_dict)
        if event == '-CHANGEURL-':
            sysfunction.changeurl(config_dict['url_path'])
        if event == sg.WIN_CLOSED:
            sysfunction.save_config(config_dict, values, config_path)
            break
    scheduler.shutdown()

if __name__ == '__main__':    
    main()
