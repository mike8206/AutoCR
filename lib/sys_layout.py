import FreeSimpleGUI as sg
from os.path import join

# in-system file
def resourcePath(relative_path):
    return join("sys", relative_path)

def mainSysLayout(config_dict):
    sg.theme(config_dict["theme"])    

    # layout part
    digisign_col = sg.Column([
        [sg.Frame('自動簽章', layout=[
            [sg.Push(), sg.Image(resourcePath("digisign.png")), sg.Push()],
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
            [sg.Push(), sg.Image(resourcePath("clinic.png")), sg.Push()],
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
            [sg.Push(),sg.Image(resourcePath("sms.png")),sg.Push()],
            [sg.Push(),sg.Button('更新Token', key='-REFRESHTOKEN-'),sg.Button('手動執行', key='-RUNSMS-')],
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
            [sg.Button('儲存設定', key='-SAVECONFIG-')],
            [sg.Button('變更設定', key='-CHANGESYS-')],
            [sg.Button('結束程式', key='-EXIT-')],
        ]),
        sg.Frame('執行結果 (每15秒更新)', layout=[
            [sg.Multiline(size=(80, 4), disabled=True, autoscroll=True , auto_refresh=True, key='-LOG-')],
            [sg.Push(), sg.Text('Version: 1.5.1.1, Designed by: 吳璨宇, 2024/08/08')]
        ])]
    ])

    other_col = sg.Column([
        [sg.Frame('常用功能', layout=[
            [sg.Button('自動驗證碼', key='-AUTOOCR-', size=(10,1))],
            [sg.Button('小ＣＲ登入', key='-CRLOGIN-', size=(10,1))],
            [sg.Button('ＶＳ登入', key='-VSLOGIN-', size=(10,1))],
            [sg.Button('診間改績效', key='-AUTOCREDIT-', size=(10,1))],
            [sg.Button('請假異動', key='-DUTYMOD-', size=(10,1))],
        ])],
        [sg.Frame('其他功能', layout=[
            #[sg.Button('更新瀏覽器', key='-UPDATEBROWSER-', size=(10,1))],
        ])],
        [sg.Checkbox('自啟動排程', config_dict['resume_switch'], key='resume_switch', size=(10,1))],
        [sg.Checkbox('隱藏瀏覽器', config_dict['hide_web'], key='hide_web', size=(10,1))],
    ], vertical_alignment='t')

    layout = [[[digisign_col,open_clinic_col,sms_col,other_col],[sys_col]]]
    return sg.Window('全自動小CR', layout, finalize=True)

def changeSysFunction():
    layout = [[[sg.Push(), sg.Text('請選擇下列功能'),sg.Push()],
                [sg.Button('變更ＣＲ帳密', key='-CHANGECR-'),sg.Button('變更簽章清單', key='-CHANGESIGN-')],
                [sg.Button('變更ＶＳ帳密', key='-CHANGEVS-'),sg.Button('變更簡訊清單', key='-CHANGEGSM-')],
                [sg.Button('變更日曆ＩＤ', key='-CHANGECALID-'),sg.Button('變更績效清單', key='-CHANGECRED-'),],
                [sg.Button('變更授權檔案', key='-CHANGECERT-'),sg.Button('變更簡訊內容', key='-CHANGESMS-')],
                [sg.Button('檢查系統檔案', key='-CHECKFILE-'),sg.Button('變更網頁元素', key='-CHANGEURL-')],
                [sg.Button('升級系統檔案', key='-UPGRADE-'),sg.Button('變更風格樣式', key='-CHANGETHEME-')],
                [sg.Button('開啟額外功能', key='-OPENFUNCTION-')],
                [sg.Push(),sg.Button('設定完成',size=(10,1),key='-EXIT-'), sg.Push()]]]
    return sg.Window('更新系統設定', layout, finalize=True)