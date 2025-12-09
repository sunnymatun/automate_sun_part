from pywinauto.application import Application
import time
from module.scroll_utils import force_scroll_down


def _ensure_spec(window):
    """Return a WindowSpecification for the given window-like object.

    Many pywinauto wrapper objects (UIAWrapper) don't provide
    child_window. Convert them to a WindowSpecification using the
    parent Application so the rest of the code can call
    child_window(...) reliably.
    """
    # If it already supports child_window, return as-is
    if hasattr(window, "child_window"):
        return window

    # Try to construct a WindowSpecification from wrapper's app and handle
    try:
        app = getattr(window, "app", None)
        handle = getattr(window, "handle", None)
        if app is not None and handle is not None:
            return app.window(handle=handle)
    except Exception:
        pass

    # Fallback: return original object (will raise if unsupported)
    return window


def connect_app(window_title):
    print("[*] Connecting to window...")
    app = Application(backend="uia").connect(title_re=window_title, timeout=10)
    win = app.window(title_re=window_title)
    win.set_focus()
    print("[/] Connected OK")
    return win


def open_agency(win, AB, delay):
    spec = _ensure_spec(win)

    spec.child_window(
        title=AB['HOTKEY_AGENCY_TITLE'],
        auto_id=AB['HOTKEY_AGENCY_AUTO_ID'],
        control_type=AB['HOTKEY_AGENCY_CONTROL_TYPE']
    ).click_input()

    time.sleep(delay)
    print("[/] กด A สำเร็จ")


def open_SAB(win, AB, delay):
    spec = _ensure_spec(win)

    spec.child_window(
        title=AB['HOTKEY_SAB_TITLE'],
        auto_id=AB['HOTKEY_SAB_AUTO_ID'],
        control_type=AB['HOTKEY_SAB_CONTROL_TYPE']
    ).click_input()

    time.sleep(delay)
    print("[/] กด S สำเร็จ")


def fill_phone_number(win, PH, delay, config):
    print("[*] ค้นหาเบอร์โทร...")

    try:
        spec = _ensure_spec(win)

        phone_custom = spec.child_window(
            auto_id="PhoneNumber_UserControlBase",
            control_type="Custom"
        )

        phone_custom.wait("ready", timeout=5)
    except:
        print("[!] ไม่พบ ต้อง scroll ลง")
        force_scroll_down(win, config)
        spec = _ensure_spec(win)
        phone_custom = spec.child_window(
            auto_id="PhoneNumber_UserControlBase",
            control_type="Custom"
        )

        phone_custom.wait("ready", timeout=5)

    phone_edit = phone_custom.child_window(
        auto_id="PhoneNumber",
        control_type="Edit"
    )

    phone_edit.wait("ready", timeout=5)

    phone_edit.click_input()
    time.sleep(0.2)
    phone_edit.type_keys("^a{BACKSPACE}")
    time.sleep(0.2)
    phone_edit.type_keys(PH['PHONE_NUM'], with_spaces=True)

    print("[/] กรอกเบอร์โทรเสร็จ")


def click_read_id(win, ID, delay):
    spec = _ensure_spec(win)

    spec.child_window(
        title=ID['ID_TITLE'],
        auto_id=ID['ID_AUTO_ID'],
        control_type=ID['ID_CONTROL_TYPE']
    ).click_input()
    time.sleep(delay)

    print("[/] อ่านบัตรสำเร็จ")


def click_next(win, NX, delay):
    spec = _ensure_spec(win)

    spec.child_window(
        title=NX['NEXT_TITLE'],
        auto_id=NX['NEXT_AUTO_ID'],
        control_type=NX['NEXT_CONTROL_TYPE']
    ).click_input()
    time.sleep(delay)

    print("[/] กดปุ่มถัดไปสำเร็จ")