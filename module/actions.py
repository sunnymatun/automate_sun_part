import time
from pywinauto import Application
from scroll_utils import force_scroll_down

def connect_app(WINDOW_TITLE):
    print("[*] เชื่อมต่อ APP...")
    app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
    win = app.window(title_re=WINDOW_TITLE)
    win.set_focus()
    print("[/] เชื่อมต่อสำเร็จ")
    return win


# ---------------------------- ACTION: กด A ----------------------------
def open_agency(win, AB, delay):
    print("[*] กดปุ่ม A (Agency)")
    win.child_window(title=AB['HOTKEY_AGENCY_TITLE'],
                     auto_id=AB['HOTKEY_AGENCY_AUTO_ID'],
                     control_type=AB['HOTKEY_AGENCY_CONTROL_TYPE']).click_input()
    time.sleep(delay)


# ---------------------------- ACTION: กด S ----------------------------
def open_SAB(win, AB, delay):
    print("[*] กดปุ่ม S (SAB)")
    win.child_window(title=AB['HOTKEY_SAB_TITLE'],
                     auto_id=AB['HOTKEY_SAB_AUTO_ID'],
                     control_type=AB['HOTKEY_SAB_CONTROL_TYPE']).click_input()
    time.sleep(delay)


# ---------------------------- ACTION: กรอกเบอร์ ----------------------------
def fill_phone_number(win, phone_cfg, delay, config):
    try:
        phone_custom = win.child_window(auto_id="PhoneNumber_UserControlBase", control_type="Custom")
        phone_custom.wait("ready", timeout=3)
    except:
        print("[!] ไม่เจอ PhoneNumber — Scroll")
        force_scroll_down(win, config)
        time.sleep(delay)
        phone_custom = win.child_window(auto_id="PhoneNumber_UserControlBase", control_type="Custom")
        phone_custom.wait("ready", timeout=3)

    # Edit
    phone_edit = phone_custom.child_window(auto_id="PhoneNumber", control_type="Edit").wait("ready", timeout=3)

    phone_edit.click_input()
    phone_edit.type_keys("^a{BACKSPACE}")
    phone_edit.type_keys(phone_cfg['PHONE_NUM'], with_spaces=True)
    print("[/] กรอกเบอร์สำเร็จ")


# ---------------------------- ACTION: อ่านบัตร ----------------------------
def click_read_id(win, ID, delay):
    win.child_window(title=ID['ID_TITLE'],
                     auto_id=ID['ID_AUTO_ID'],
                     control_type=ID['ID_CONTROL_TYPE']).click_input()
    time.sleep(delay)
    print("[/] อ่านบัตรสำเร็จ")


# ---------------------------- ACTION: ถัดไป ----------------------------
def click_next(win, NX, delay):
    win.child_window(title=NX['NEXT_TITLE'],
                     auto_id=NX['NEXT_AUTO_ID'],
                     control_type=NX['NEXT_CONTROL_TYPE']).click_input()
    time.sleep(delay)
    print("[/] กดถัดไปสำเร็จ")
