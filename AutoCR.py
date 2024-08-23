from os import makedirs
from os.path import exists
from datetime import datetime
from threading import Thread

# FreeSimpleGUI + apscheduler
import FreeSimpleGUI as sg
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# customized functions
from lib import sys_layout, sys_func, sys_update
from lib import autocredit, autodigisign, autoopenclinic, autosms, autodutymodify
from lib.sms.google_calendar import googleRefreshToken

# sys file path
makedirs("sys", exist_ok=True)
CONFIG_PATH = 'sys\\config.json'

# main function
def main():
    # read settings
    config_dict = sys_func.loadConfig('config', CONFIG_PATH)
    url_dict = sys_func.loadConfig('url', config_dict['url_path'])

    # update configs if new key&value added
    config_dict, url_dict = sys_update.updateConfigKey(config_dict, url_dict)

    # log functions
    def updateLog(logstring):
        sys_func.updateFile(config_dict['log_path'], logstring)
    def updateErrorLog(error_msg):
        sys_func.updateFile(config_dict['error_log_path'], error_msg)

    # in-window function
    def digisign():
        autodigisign.main(config_dict, url_dict)
    
    def openclnc():
        autoopenclinic.main(config_dict, url_dict)
    
    def sms():
        autosms.main(config_dict, url_dict)
    
    def credit():
        try:
            autocredit.main(config_dict, url_dict)
            logstring = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" 修改績效 成功!"
            updateLog(logstring)
        except Exception as error:
            logstring = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" 修改績效 失敗! 已儲存錯誤紀錄!"
            updateErrorLog(datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+str(error))
            updateLog(logstring)
            sg.Popup("修改績效失敗!請手動確認績效!", title="修改績效失敗")
            pass
    
    def dutymodify(func_string, id_pw):
        autodutymodify.main(config_dict, url_dict, func_string, id_pw)

    def listener(event):
        job_id = event.job_id
        try:
            job_time = scheduler.get_job(job_id=job_id).next_run_time
        except:
            job_time = "無"
        if event.exception:
            logstring = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+ job_id+' 失敗! 已儲存錯誤紀錄!'
            error_msg = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+ str(event.exception)
            updateErrorLog(error_msg)
        else:
            logstring = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+ job_id+' 成功執行! 下次執行時間: '+ str(job_time)
        updateLog(logstring)
        
    def schdlrCronFormat(hr, min, hrrepeat):
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

    def digisignSwitchSchdlr(onoff, digihr, digimin, digirepeat):
        if onoff:
            sg.popup_auto_close('自動簽章已開啟!', auto_close_duration=2)
            cron_format = schdlrCronFormat(digihr, digimin, digirepeat)
            scheduler.add_job(digisign, CronTrigger.from_crontab(cron_format, timezone='Asia/Taipei'), id='自動簽章', replace_existing=True)
        else:
            sg.popup_auto_close('自動簽章已關閉!', auto_close_duration=2)
            scheduler.remove_job(job_id='自動簽章')

    def openclncSwitchSchdlr(onoff, amhr, ammin, pmhr, pmmin):
        if onoff:
            sg.popup_auto_close('自動開診已開啟!', auto_close_duration=2)
            scheduler.add_job(openclnc, trigger='cron', id='上午自動開診', day_of_week='mon-fri', hour=amhr, minute=ammin, timezone='Asia/Taipei', replace_existing=True)
            scheduler.add_job(openclnc, trigger='cron', id='下午自動開診', day_of_week='mon-fri', hour=pmhr, minute=pmmin, timezone='Asia/Taipei', replace_existing=True)
        else:
            sg.popup_auto_close('自動開診已關閉!', auto_close_duration=2)
            scheduler.remove_job(job_id='上午自動開診')
            scheduler.remove_job(job_id='下午自動開診')

    def smsSwitchSchdlr(onoff, amhr, ammin, pmhr, pmmin):
        if onoff:
            sg.popup_auto_close('自動寄簡訊已開啟!', auto_close_duration=2)
            scheduler.add_job(sms, trigger='cron', id='上午自動寄簡訊', day_of_week='mon-fri', hour=amhr, minute=ammin, timezone='Asia/Taipei', replace_existing=True)
            scheduler.add_job(sms, trigger='cron', id='下午自動寄簡訊', day_of_week='mon-fri', hour=pmhr, minute=pmmin, timezone='Asia/Taipei', replace_existing=True)
        else:
            sg.popup_auto_close('自動寄簡訊已關閉!', auto_close_duration=2)
            scheduler.remove_job(job_id='上午自動寄簡訊')
            scheduler.remove_job(job_id='下午自動寄簡訊')

    def updateWindow1(config_dict):
        window1.Element('-DIGISIGNSWITCH-').Update(('加入排程','刪除排程')[config_dict['digi_switch']], button_color=(('white', ('green','red')[config_dict['digi_switch']])))
        window1.Element('-CLINICSWITCH-').Update(('加入排程','刪除排程')[config_dict['clinic_switch']], button_color=(('white', ('green','red')[config_dict['clinic_switch']])))
        window1.Element('-SMSSWITCH-').Update(('加入排程','刪除排程')[config_dict['sms_switch']], button_color=(('white', ('green','red')[config_dict['sms_switch']])))

    def window1Log():
        try:
            console_log = sys_func.readFile(config_dict['log_path'])
            window1['-LOG-'].update(console_log)
        except:
            pass
    
    # initial setup
    if config_dict['setup'] == False:
        sys_func.checkFileExist(config_dict)
        config_dict['setup'] = True

    # start scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_listener(listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.start()

    # resume scheduler
    if config_dict['resume_switch']:
        if config_dict['digi_switch']:
            digisignSwitchSchdlr(config_dict['digi_switch'], config_dict['digi_hr'], config_dict['digi_min'], config_dict['digi_repeat'])
        if config_dict['clinic_switch']:
            openclncSwitchSchdlr(config_dict['clinic_switch'], config_dict['am_clinic_hr'], config_dict['am_clinic_min'], config_dict['pm_clinic_hr'], config_dict['pm_clinic_min'])
        if config_dict['sms_switch']:
            smsSwitchSchdlr(config_dict['sms_switch'], config_dict['am_sms_hr'], config_dict['am_sms_min'], config_dict['pm_sms_hr'], config_dict['pm_sms_min'])
    else:
        config_dict['digi_switch'] = False
        config_dict['clinic_switch'] = False
        config_dict['sms_switch'] = False

    # show window1 UI
    window1, window2 = sys_layout.mainSysLayout(config_dict), None
    updateWindow1(config_dict)
    window1Log()

    while True:
        window, event, values = sg.read_all_windows(timeout=15000)
        window1Log()
        if event == '-EXIT-' or event == sg.WIN_CLOSED:
            window.close()
            if window == window2:
                window1, window2 = sys_layout.mainSysLayout(config_dict), None
                updateWindow1(config_dict)
            elif window == window1:
                sys_func.saveConfig(config_dict, values, CONFIG_PATH)
                break
        if scheduler.running != True:
            scheduler.start()
        if event == '-RUNDIGISIGN-':
            config_dict['hide_web'] = values['hide_web']
            Thread(target=scheduler.add_job, args=[digisign, None, None, None, '手動執行自動簽章'], daemon=True).start()
        if event == '-RUNOPENCLNC-':
            config_dict['hide_web'] = values['hide_web']
            Thread(target=scheduler.add_job, args=[openclnc, None, None, None, '手動執行自動開診'], daemon=True).start()
        if event == '-RUNSMS-':
            config_dict['hide_web'] = values['hide_web']
            Thread(target=scheduler.add_job, args=[sms, None, None, None, '手動執行自動寄簡訊'], daemon=True).start()
        if event == '-REFRESHTOKEN-':
            Thread(target=googleRefreshToken, args=[config_dict['google_secret_path'], config_dict['google_token_path']], daemon=True).start()
        if event == '-DIGISIGNSWITCH-':
            config_dict['digi_switch'] = not config_dict['digi_switch']
            window1.Element('-DIGISIGNSWITCH-').Update(('加入排程','刪除排程')[config_dict['digi_switch']], button_color=(('white', ('green','red')[config_dict['digi_switch']])))
            digisignSwitchSchdlr(config_dict['digi_switch'], values['digi_hr'], values['digi_min'], values['digi_repeat'])
        if event == '-CLINICSWITCH-':
            config_dict['clinic_switch'] = not config_dict['clinic_switch']
            window1.Element('-CLINICSWITCH-').Update(('加入排程','刪除排程')[config_dict['clinic_switch']], button_color=(('white', ('green','red')[config_dict['clinic_switch']])))
            openclncSwitchSchdlr(config_dict['clinic_switch'], values['am_clinic_hr'], values['am_clinic_min'], values['pm_clinic_hr'], values['pm_clinic_min'])
        if event == '-SMSSWITCH-':
            config_dict['sms_switch'] = not config_dict['sms_switch']
            window1.Element('-SMSSWITCH-').Update(('加入排程','刪除排程')[config_dict['sms_switch']], button_color=(('white', ('green','red')[config_dict['sms_switch']])))
            smsSwitchSchdlr(config_dict['sms_switch'], values['am_sms_hr'], values['am_sms_min'], values['pm_sms_hr'], values['pm_sms_min'])
        if event == '-AUTOOCR-':
            try:
                if exists(config_dict['autoocr_path']):
                    Thread(target=sys_func.callOtherFunction, args=[config_dict['autoocr_path']], daemon=True).start()
            except:
                sg.Popup('尚未實裝! 請至變更設定開啟額外功能!', title="尚未實裝!")
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
                sg.Popup('尚未實裝! 請至變更設定開啟額外功能!', title="尚未實裝!")
        if event == '-AUTOCREDIT-':
            sg.popup_auto_close("準備修改績效，主畫面將暫停更新(背景排程會繼續執行)", title="準備修改績效...")
            credit()
        if event == '-DUTYMOD-':
            duty_arg = sys_func.dutyModifyFunction(config_dict['vs_id_path'])
            if duty_arg:
                Thread(target=scheduler.add_job, args=[dutymodify, None, duty_arg, None, '手動執行'+duty_arg[0]], daemon=True).start()
        if event == '-UPDATEBROWSER-':
            sg.Popup("更新瀏覽器檔案!")
            config_dict = sys_update.updateWebDriver(config_dict)
            sg.Popup('瀏覽器檔案更新完成!!')
        if event == '-SAVECONFIG-':
            sys_func.saveConfig(config_dict, values, CONFIG_PATH)
            sg.Popup("已成功儲存設定!")
        if event == '-CHANGESYS-' and not window2:
            window2 = sys_layout.changeSysFunction()
            window.close()
        if event == '-CHANGECR-':
            sys_func.saveIdPw('CR', config_dict['cr_id_path'])
        if event == '-CHANGEVS-':
            sys_func.saveIdPw('VS', config_dict['vs_id_path'])
        if event == '-OPENFUNCTION-':
            sys_func.openOtherFunction(config_dict)
        if event == '-CHANGETHEME-':
            event, values = sg.Window('變更風格', [[sg.Combo(sg.theme_list(), readonly=True, k='-THEME LIST-'), sg.OK(), sg.Cancel()]], finalize=True).read(close=True)
            if values['-THEME LIST-'] !='' and values['-THEME LIST-'] != sg.theme():
                config_dict['theme'] = sg.theme(values['-THEME LIST-'])
                sg.theme(values['-THEME LIST-'])
                window2 = sys_layout.changeSysFunction()
                window.close()
        if event == '-CHECKFILE-':
            sg.Popup("重新檢測檔案!")
            sys_func.checkFileExist(config_dict)
        if event == '-UPGRADE-':
            sg.Popup("升級設定檔!")
            sys_update.updateConfigKey(config_dict, url_dict)
            sg.Popup("設定檔已升級完成!")
        if event == '-CHANGESIGN-':
            sys_func.saveList("sign", config_dict['list_path'])
        if event == '-CHANGEGSM-':
            sys_func.saveList("sms", config_dict['phone_path'])
        if event == '-CHANGECRED-':
            sys_func.saveList("credit", config_dict['vslist_path'])
        if event == '-CHANGECERT-':
            sys_func.saveGoogleFile(config_dict['google_secret_path'], config_dict['google_token_path'])
        if event == '-CHANGECALID-':
            config_dict.update(google_cal_id = sys_func.saveGoogleCalnId(config_dict['google_cal_id']))
        if event == '-CHANGESMS-':
            sys_func.changeDictElement("sms", config_dict['sms_path'])
        if event == '-CHANGEURL-':
            sys_func.changeDictElement("url", config_dict['url_path'])
            url_dict = sys_func.loadConfig('url', config_dict['url_path'])
    scheduler.shutdown()

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        error_msg = datetime.now().strftime("%Y/%m/%d %H:%M:%S")+" "+str(error)
        config_dict = sys_func.loadConfig('config', CONFIG_PATH)
        sys_func.updateFile(config_dict['error_log_path'], error_msg)