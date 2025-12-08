import configparser
from pywinauto.application import Application
import time
import os

# ชื่อไฟล์ Config
CONFIG_FILE = "config.ini"

def read_config(filename=CONFIG_FILE):
    """อ่านและโหลดค่าจากไฟล์ config.ini"""
    config = configparser.ConfigParser()
    try:
        if not os.path.exists(filename):
            print(f"[X] ไม่พบไฟล์ config ที่: {os.path.abspath(filename)}")
            return configparser.ConfigParser()
            
        config.read(filename, encoding='utf-8')
        return config
    except Exception as e:
        print(f"[X] FAILED: ไม่สามารถอ่านไฟล์ {filename} ได้: {e}")
        return configparser.ConfigParser()

# โหลด Config
CONFIG = read_config()
if not CONFIG.sections():
    print("ไม่สามารถโหลด config.ini ได้ โปรดตรวจสอบไฟล์")
    exit()

# ค่า Global
WINDOW_TITLE = CONFIG['GLOBAL']['WINDOW_TITLE']
SLEEP_TIME = CONFIG.getint('GLOBAL', 'LOAD_TIME_SEC')

def test_agency_barcode(config):
    """ทดสอบระบบ agency barcode"""
    print("=" * 50)
    print("[*] เริ่มทดสอบ: agency barcode")

    # ดึงค่า Config ของส่วนคืนสินค้ามาเก็บไว้ในตัวแปรสั้นๆ
    AB_CFG = config['agency barcode']
    ID_CFG = config['ID']
    GL_CFG = config['GLOBAL']
    SCROLL_CFG = config['MOUSE_SCROLL']

    try:
        # 1. เชื่อมต่อ App
        print("\n[*] กำลังเชื่อมต่อหน้าจอหลัก...")
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        print("[/] เชื่อมต่อหน้าจอขายสำเร็จ")
        
        # 2. กด A เพื่อเข้าหน้าagency
        main_window.child_window(title=AB_CFG['HOTKEY_A_TITLE'], 
                                 auto_id=AB_CFG['HOTKEY_A_AUTO_ID'], 
                                 control_type=AB_CFG['HOTKEY_A_CONTROL_TYPE']).click_input()
        time.sleep(SLEEP_TIME)
        print("[/] เปิดหน้าagencyสำเร็จ")

        # 3. กด S เพื่อเข้าหน้าagency
        main_window.child_window(title=AB_CFG['HOTKEY_S_TITLE'], 
                                 auto_id=AB_CFG['HOTKEY_S_AUTO_ID'], 
                                 control_type=AB_CFG['HOTKEY_A_CONTROL_TYPE']).click_input()
        time.sleep(SLEEP_TIME)
        print("[/] เปิดหน้าagency barcodeสำเร็จ")

        # 4. กดปุ่ม 'อ่านบัตรประชาชน'
        main_window.child_window(title=ID_CFG['ID_TITLE'], 
                                 auto_id=ID_CFG['ID_AUTO_ID'], 
                                 control_type=ID_CFG['ID_CONTROL_TYPE']).click_input()
        time.sleep(SLEEP_TIME)
        
        print("\n[*] กำลัง Scroll หน้าจอด้วย Dynamic Config...")
        
        # ดึงค่าพิกัดและระยะการเลื่อนจาก Config (ใช้ getint/getfloat)
        center_x_offset = config.getint('MOUSE_SCROLL', 'CENTER_X_OFFSET')
        center_y_offset = config.getint('MOUSE_SCROLL', 'CENTER_Y_OFFSET')
        wheel_dist = config.getint('MOUSE_SCROLL', 'WHEEL_DIST')
        focus_delay = config.getfloat('MOUSE_SCROLL', 'FOCUS_DELAY')
        scroll_delay = config.getfloat('MOUSE_SCROLL', 'SCROLL_DELAY')

        # คำนวณพิกัด
        rect = main_window.rectangle() # ใช้ main_window แทน window
        center_x = rect.left + center_x_offset
        center_y = rect.top + center_y_offset
        
        # คลิก 1 ครั้งเพื่อ Focus (ใช้ค่าหน่วงจาก Config)
        mouse.click(coords=(center_x, center_y))
        time.sleep(focus_delay)
        
        # หมุนล้อเมาส์ลง (ใช้ระยะและค่าหน่วงจาก Config)
        mouse.scroll(coords=(center_x, center_y), wheel_dist=wheel_dist)
        time.sleep(scroll_delay)
        print(f"[/] Scroll ลง {wheel_dist} พิกัด ({center_x}, {center_y}) สำเร็จ")


        print("[V] จบการทดสอบ: agency barcode สำเร็จ")

    except Exception as e:
        print(f"[X] Error during Return Product Test: {e}")

if __name__ == "__main__":
    test_agency_barcode(CONFIG)