import configparser
from pywinauto.application import Application
from pywinauto import mouse 
import time
import os

# ชื่อไฟล์ Config
CONFIG_FILE = "config.ini"

# ==================== CONFIG & HELPER FUNCTIONS ====================

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
# ใช้ getfloat เพื่อรองรับค่า LOAD_TIME_SEC ที่เป็นทศนิยม
SLEEP_TIME = CONFIG.getfloat('GLOBAL', 'LOAD_TIME_SEC') 


def force_scroll_down(window, config):
    """
    ฟังก์ชันช่วยเลื่อนหน้าจอลง (Scroll) โดยใช้ Mouse Wheel และดึงค่าจาก [MOUSE_SCROLL]
    """
    try:
        # ดึงค่าจาก Config และแปลงเป็น Integer/Float
        center_x_offset = config.getint('MOUSE_SCROLL', 'CENTER_X_OFFSET')
        center_y_offset = config.getint('MOUSE_SCROLL', 'CENTER_Y_OFFSET')
        wheel_dist = config.getint('MOUSE_SCROLL', 'WHEEL_DIST')
        focus_delay = config.getfloat('MOUSE_SCROLL', 'FOCUS_DELAY')
        scroll_delay = config.getfloat('MOUSE_SCROLL', 'SCROLL_DELAY')
    except ValueError:
        print("[!] Scroll Config values are not valid. Using defaults.")
        center_x_offset, center_y_offset, wheel_dist, focus_delay, scroll_delay = 300, 300, -20, 0.5, 1.0

    print(f"...กำลังเลื่อนหน้าจอลง (Mouse Wheel {wheel_dist})...")
    
    try:
        rect = window.rectangle()
        center_x = rect.left + center_x_offset
        center_y = rect.top + center_y_offset
        
        mouse.click(coords=(center_x, center_y))
        time.sleep(focus_delay)
        
        mouse.scroll(coords=(center_x, center_y), wheel_dist=wheel_dist)
        time.sleep(scroll_delay)
        print(f"[/] Scroll ลง {wheel_dist} สำเร็จ")
        
    except Exception as e:
        print(f"[!] Mouse scroll failed: {e}. ลองกดปุ่ม Page Down แทน")
        window.type_keys("{PGDN}")


# ==================== TEST FUNCTION ====================

def test_agency_barcode(config):
    """ทดสอบระบบ agency barcode"""
    print("=" * 50)
    print("[*] เริ่มทดสอบ: agency barcode")

    # ดึงค่า Config ของส่วนต่างๆ
    AB_CFG = config['agency barcode']
    ID_CFG = config['ID']
    PH_CFG = config['phone'] 

    try:
        # 1. เชื่อมต่อ App
        print("\n[*] กำลังเชื่อมต่อหน้าจอหลัก...")
        app = Application(backend="uia").connect(title_re=WINDOW_TITLE, timeout=10)
        main_window = app.top_window()
        main_window.set_focus()
        print("[/] เชื่อมต่อหน้าจอขายสำเร็จ")
        
        # 2. กด A 
        main_window.child_window(title=AB_CFG['HOTKEY_A_TITLE'], 
                                auto_id=AB_CFG['HOTKEY_A_AUTO_ID'], 
                                control_type=AB_CFG['HOTKEY_A_CONTROL_TYPE']).click_input()
        time.sleep(SLEEP_TIME)
        print("[/] เปิดหน้า agency สำเร็จ")

        # 3. กด S 
        main_window.child_window(title=AB_CFG['HOTKEY_S_TITLE'], 
                                auto_id=AB_CFG['HOTKEY_S_AUTO_ID'], 
                                control_type=AB_CFG['HOTKEY_A_CONTROL_TYPE']).click_input()
        time.sleep(SLEEP_TIME)
        print("[/] เปิดหน้า agency barcode สำเร็จ")


        # ==================== 4. LOGIC: ค้นหา-เลื่อน-ค้นหาช่องเบอร์โทรศัพท์ ====================
        
        # สร้าง Dictionary Selector ที่ถูกต้องจาก PH_CFG
        phone_selectors = {
            'auto_id': PH_CFG['PHONE_AUTO_ID'],
            'control_type': PH_CFG['PHONE_CONTROL_TYPE']
        }
        # ตรวจสอบว่ามี title หรือไม่ และเพิ่มเข้าไป
        if 'PHONE_TITLE' in PH_CFG:
            phone_selectors['title'] = PH_CFG['PHONE_TITLE']
        
        print(f"DEBUG: Selector ที่ใช้ค้นหา: {phone_selectors}")
        
        found = False
        
        # 4.1 ลองค้นหาครั้งแรก
        try:
            print("[*] 4.1. กำลังค้นหาช่องเบอร์โทรศัพท์...")
            # ใช้ timeout ที่สั้นลงในการค้นหาครั้งแรก
            phone_field = main_window.child_window(**phone_selectors).wait('ready', timeout=2) 
            found = True
        except Exception:
            # ถ้าค้นหาไม่สำเร็จ ให้ Scroll ลง
            print("[!] ช่องเบอร์โทรศัพท์ไม่พบในมุมมองปัจจุบัน. กำลังเลื่อนหน้าจอ...")
            force_scroll_down(main_window, config)
            time.sleep(SLEEP_TIME)
        
        # 4.2 ค้นหาอีกครั้งหลัง Scroll (ถ้ายังไม่พบ)
        if not found:
            try:
                print("[*] 4.2. ลองค้นหาช่องเบอร์โทรศัพท์อีกครั้งหลัง Scroll...")
                # ใช้ timeout ที่สั้นลงในการค้นหาครั้งที่สอง
                phone_field = main_window.child_window(**phone_selectors).wait('ready', timeout=2) 
                found = True
            except Exception as e_scroll:
                print(f"[X] ค้นหาไม่สำเร็จแม้จะ Scroll แล้ว: {e_scroll}")
                raise RuntimeError("ไม่สามารถเข้าถึงช่องเบอร์โทรศัพท์ได้")
        
        # 4.3 คลิกและกรอกข้อมูล (ถ้าพบ)
        if found:
            phone_field.click_input()
            time.sleep(SLEEP_TIME)
            main_window.type_keys(PH_CFG['PHONE_NUM'])
            print("[/] คลิกและกรอกเบอร์โทรศัพท์สำเร็จ")


        # ==================== 5. ขั้นตอนต่อไป ====================
        
        # 5.1 กดปุ่ม 'อ่านบัตรประชาชน'
        main_window.child_window(title=ID_CFG['ID_TITLE'], 
                                auto_id=ID_CFG['ID_AUTO_ID'], 
                                control_type=ID_CFG['ID_CONTROL_TYPE']).click_input()
        time.sleep(SLEEP_TIME)


        print("[V] จบการทดสอบ: agency barcode สำเร็จ")

    except Exception as e:
        print(f"[X] Error during agency barcode Test: {e}")


if __name__ == "__main__":
    test_agency_barcode(CONFIG)