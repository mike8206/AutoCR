from datetime import datetime
from os.path import exists

import json
import PySimpleGUI as sg

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from threading import Thread

from lib import sys_layout, sys_func, sys_initial, autodigisign, autoopenclinic, autosms, autocredit, autodutymodify, autogetphone
from lib.sms.google_calendar import googleRefreshToken

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
    config_dict = sys_initial.initialConfig(config_path)

try:
    with open(config_dict['url_path'], encoding="UTF-8") as file:
        s = file.read()
        url_dict = json.loads(s)
except:
    url_dict = sys_initial.initialUrl(config_dict['url_path'])

# functions
def error_log(error_msg):
    with open(error_log_path, 'a', encoding="UTF-8") as file:
        file.write(str(error_msg)+"\n")
def digisign():
    autodigisign.main(url_dict, config_dict['vs_id_path'], config_dict['list_path'], chrome_driver_path, ie_driver_path)
def openclnc():
    autoopenclinic.main(url_dict, config_dict['vs_id_path'], chrome_driver_path, ie_driver_path)
def googletoken():
    googleRefreshToken(config_dict['google_secret_path'], config_dict['google_token_path'])
def sms():
    autosms.main(url_dict, config_dict['cr_id_path'], config_dict['phone_path'], config_dict['google_secret_path'], config_dict['google_token_path'], config_dict['google_cal_id'], chrome_driver_path)
def autocred():
    autocredit.main(url_dict, config_dict['cr_id_path'], chrome_driver_path)
def dutymodify(function, data):
    autodutymodify.main(url_dict, function, data, chrome_driver_path)
def autophone(origin_type):
    autogetphone.main(url_dict, config_dict['cr_id_path'], origin_type, chrome_driver_path)

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
            logstring = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+ job_id+' 失敗! 已儲存錯誤紀錄!'
            error_msg = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+ str(event.exception)
            error_log(error_msg)
        else:
            logstring = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+ job_id+' 成功執行! 下次執行時間: '+ str(job_time)
        update_log(logstring)

    def update_log(logstring):
        with open(log_path, 'a', encoding="UTF-8") as file:
            file.write(logstring+"\n")
        with open(log_path, 'r', encoding="UTF-8") as file: 
            console_log = file.read()
            window1['-LOG-'].update(console_log)
        
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

    # initial setup
    if config_dict['setup'] == False:
        sys_func.checkFileExist(config_dict)
        config_dict.update(setup = True)

    scheduler = BackgroundScheduler()
    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    window1, window2 = sys_layout.mainSysLayout(config_dict), None

    while True:
        window, event, values = sg.read_all_windows(timeout=100)
        if event == '-EXIT-' or event == sg.WIN_CLOSED:
            window.close()
            if window == window2:
                window2 = None
                window1 = sys_layout.mainSysLayout(config_dict)
                window1.Element('-DIGISIGNSWITCH-').Update(('加入排程','刪除排程')[switch_digisign], button_color=(('white', ('green','red')[switch_digisign])))
                window1.Element('-CLINICSWITCH-').Update(('加入排程','刪除排程')[switch_clinic], button_color=(('white', ('green','red')[switch_clinic])))
                window1.Element('-SMSSWITCH-').Update(('加入排程','刪除排程')[switch_sms], button_color=(('white', ('green','red')[switch_sms])))
            elif window == window1:
                sys_func.saveConfig(config_dict, values, config_path)
                break
        if scheduler.running != True:
            scheduler.start()
        if event == '-RUNDIGISIGN-':
            Thread(target=scheduler.add_job, args=[digisign, None, None, None, '手動執行自動簽章'], daemon=True).start()
        if event == '-RUNOPENCLNC-':
            Thread(target=scheduler.add_job, args=[openclnc, None, None, None, '手動執行自動開診'], daemon=True).start()
        if event == '-REFRESHTOKEN-':
            refreshtoken =  Thread(target=googletoken, daemon=True).start()
            if refreshtoken:
                print('finish!')
            else:
                print('failed')
        if event == '-RUNSMS-':
            Thread(target=scheduler.add_job, args=[sms, None, None, None, '手動執行自動寄簡訊'], daemon=True).start()
        if event == '-DIGISIGNSWITCH-':
            switch_digisign = not switch_digisign
            window1.Element('-DIGISIGNSWITCH-').Update(('加入排程','刪除排程')[switch_digisign], button_color=(('white', ('green','red')[switch_digisign])))
            digisign_switch_schdlr(switch_digisign, values['digi_hr'], values['digi_min'], values['digi_repeat'])
        if event == '-CLINICSWITCH-':
            switch_clinic = not switch_clinic
            window1.Element('-CLINICSWITCH-').Update(('加入排程','刪除排程')[switch_clinic], button_color=(('white', ('green','red')[switch_clinic])))
            openclnc_switch_schdlr(switch_clinic, values['am_clinic_hr'], values['am_clinic_min'], values['pm_clinic_hr'], values['pm_clinic_min'])
        if event == '-SMSSWITCH-':
            switch_sms = not switch_sms
            window1.Element('-SMSSWITCH-').Update(('加入排程','刪除排程')[switch_sms], button_color=(('white', ('green','red')[switch_sms])))
            sms_switch_schdlr(switch_sms, values['am_sms_hr'], values['am_sms_min'], values['pm_sms_hr'], values['pm_sms_min'])
        if event == '-AUTOOCR-':
            try:
                if exists(config_dict['autoocr_path']):
                    Thread(target=sys_func.autoOCR, args=[config_dict['autoocr_path']], daemon=True).start()
            except:
                sg.Popup('尚未實裝! 請至變更設定開啟額外功能!')
        if event in ('-VSLOGIN-', '-CRLOGIN-'):
            try:
                if exists(config_dict['login_path']):
                    idpwpin = []
                    if event == '-VSLOGIN-':
                        idpwpin = sys_func.readIdPwPin(config_dict['vs_id_path'])
                    if event == '-CRLOGIN-':
                        idpwpin = sys_func.readIdPwPin(config_dict['cr_id_path'])
                    Thread(target=sys_func.autoLogin, args=[config_dict['login_path'], url_dict['portal_url'], idpwpin], daemon=True).start()
            except:
                sg.Popup('尚未實裝! 請至變更設定開啟額外功能!')
        if event == '-AUTOCREDIT-':
            Thread(target=scheduler.add_job, args=[autocred, None, None, None, '手動執行自動改績效'], daemon=True).start()
        if event == '-DUTYMOD-':
            duty_arg = sys_func.dutyModify(config_dict)
            if duty_arg:
                Thread(target=scheduler.add_job, args=[dutymodify, None, duty_arg, None, '手動執行'+duty_arg[0]], daemon=True).start()
        if event == '-MONTHSCHED-':
            sg.Popup('尚未實裝! 請至變更設定開啟額外功能!')
        if event == '-FINDPHONECLINIC-':
            Thread(target=scheduler.add_job(autophone, args=['clinic'], id='手動執行診間查電話'), daemon=True).start()
        if event == '-FINDPHONEEXAM-':
            Thread(target=scheduler.add_job(autophone, args=['exam'], id='手動執行檢查查電話'), daemon=True).start()
        if event == '-MOVEVIDEO-':
            sg.Popup('尚未實裝! 請至變更設定開啟額外功能!')
        if event == '-SAVECONFIG-':
            sys_func.saveConfig(config_dict, values, config_path)
            sg.Popup("已成功儲存設定!")
        if event == '-CHANGESYS-' and not window2:
            window2 = sys_layout.changeSysFunction()
            window.close()
        if event == '-CHANGEVS-':
            sys_func.saveIdPw('VS', config_dict['vs_id_path'])
        if event == '-CHANGECR-':
            sys_func.saveIdPw('CR', config_dict['cr_id_path'])
        if event == '-CHANGESIGN-':
            sys_func.saveList("sign", config_dict['list_path'])
        if event == '-CHANGESMS-':
            sys_func.saveList("phone", config_dict['phone_path'])
        if event == '-CHANGECALID-':
            config_dict.update(google_cal_id = sys_func.saveGoogleCalnId(config_dict['google_cal_id']))
        if event == '-CHANGECERT-':
            sys_func.saveGoogleFile(config_dict['google_secret_path'], config_dict['google_token_path'])
        if event == '-CHANGETHEME-':
            event, values = sg.Window('變更風格', [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME LIST-'), sg.OK(), sg.Cancel()]], finalize=True).read(close=True)
            if values['-THEME LIST-'] !='' and values['-THEME LIST-'] != sg.theme():
                config_dict['theme'] = sg.theme(values['-THEME LIST-'])
                sg.theme(values['-THEME LIST-'])
                window2 = sys_layout.changeSysFunction()
                window.close()
        if event == '-OPENFUNCTION-':
            sys_func.openOtherFunction(config_dict)
        if event == '-CHECKFILE-':
            sg.Popup("重新檢測檔案!")
            sys_func.checkFileExist(config_dict)
        if event == '-CHANGEURL-':
            sys_func.changeUrlElement(config_dict['url_path'])
    scheduler.shutdown()

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        error_log(datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+str(error))