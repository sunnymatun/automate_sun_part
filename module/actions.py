from pywinauto.application import Application
import time
from scroll_utils import force_scroll_down


def connect_app(window_title):
    print("[*] Connecting to window...")
    app = Application(backend="uia").connect(title_re=window_title, timeout=10)
    win = app.window(title_re=window_title)
    win.set_focus()
    print("[/] Connected OK")
    return win


def open_agency(win, AB, delay):
    win.child_window(
        title=AB['HOTKEY_AGENCY_TITLE'],
        auto_id=AB['HOTKEY_AGENCY_AUTO_ID'],
        control_type=AB['HOTKEY_AGENCY_CONTROL_TYPE']
    ).click_input()

    time.sleep(delay)
    print("[/] กด A สำเร็จ")


def open_SAB(win, AB, delay):
    win.child_window(
        title=AB['HOTKEY_SAB_TITLE'],
        auto_id=AB['HOTKEY_SAB_AUTO_ID'],
        control_type=AB['HOTKEY_SAB_CONTROL_TYPE']
    ).click_input()

    time.sleep(delay)
    print("[/] กด S สำเร็จ")


def fill_phone_number(win, PH, delay, config):
    print("[*] ค้นหาเบอร์โทร...")

    try:
        phone_custom = win.child_window(
            auto_id="PhoneNumber_UserControlBase",
            control_type="Custom"
        ).wait("ready", timeout=3)
    except:
        print("[!] ไม่พบ ต้อง scroll ลง")
        force_scroll_down(win, config)
        phone_custom = win.child_window(
            auto_id="PhoneNumber_UserControlBase",
            control_type="Custom"
        ).wait("ready", timeout=3)

    phone_edit = phone_custom.child_window(
        auto_id="PhoneNumber",
        control_type="Edit"
    ).wait("ready", timeout=3)

    phone_edit.click_input()
    time.sleep(0.2)
    phone_edit.type_keys("^a{BACKSPACE}")
    time.sleep(0.2)
    phone_edit.type_keys(PH['PHONE_NUM'], with_spaces=True)

    print("[/] กรอกเบอร์โทรเสร็จ")


def click_read_id(win, ID, delay):
    win.child_window(
        title=ID['ID_TITLE'],
        auto_id=ID['ID_AUTO_ID'],
        control_type=ID['ID_CONTROL_TYPE']
    ).click_input()
    time.sleep(delay)

    print("[/] อ่านบัตรสำเร็จ")


def click_next(win, NX, delay):
    win.child_window(
        title=NX['NEXT_TITLE'],
        auto_id=NX['NEXT_AUTO_ID'],
        control_type=NX['NEXT_CONTROL_TYPE']
    ).click_input()
    time.sleep(delay)

    print("[/] กดปุ่มถัดไปสำเร็จ")
