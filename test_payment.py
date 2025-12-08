from pywinauto.application import Application
from pywinauto import mouse
import configparser
import os 

# ================= 1. Config Loader (ใช้ INI) =================

def load_ini_config(file_path='element_config.ini'):
    """โหลดและจัดระเบียบข้อมูลจากไฟล์ INI ให้เป็นโครงสร้าง Dict ที่ใช้งานง่าย"""
    config = configparser.ConfigParser()
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
        
    # อ่านไฟล์ INI
    config.read(file_path, encoding='utf-8')
    
    # 1. โหลดส่วน APP_CONFIG และ SCROLL_CONFIG
    app_config = dict(config.items('APP_CONFIG'))
    scroll_config = dict(config.items('SCROLL_CONFIG'))
    
    # 2. จัดกลุ่ม Elements: แปลง key-value ของ Elements ให้เป็น dict ของแต่ละ Element
    elements_config = {}
    element_map = config.items('ELEMENTS')
    
    # Logic ในการจัดกลุ่ม key-value (เช่น A_title, A_auto_id) เข้าด้วยกัน
    for key, value in element_map:
        parts = key.rsplit('_', 1)
        # ถ้ามี selector type (เช่น title, auto_id) เป็นส่วนสุดท้าย
        if len(parts) > 1 and parts[-1] in ['title', 'auto_id', 'control_type', 'keys']:
            element_name = "_".join(parts[:-1]) 
            selector_type = parts[-1] 
            
            if element_name not in elements_config:
                elements_config[element_name] = {}
            
            elements_config[element_name][selector_type] = value
        # ถ้าเป็นข้อมูลที่ไม่ใช่ selector (เช่น type_phone_number_keys)
        elif key.endswith('_keys'): 
             elements_config[key] = value

    return app_config, elements_config, scroll_config

# โหลด config เมื่อเริ่มต้น (Global Access)
try:
    APP_CONFIG, ELEMENT_CONFIG, SCROLL_CONFIG = load_ini_config()
    print("[/] Configuration loaded successfully from element_config.ini")
except FileNotFoundError as e:
    print(f"[CRITICAL ERROR] {e}")
    exit(1)


# ================= 2. Helper Functions =================

# สมมติฐาน: ฟังก์ชัน Log ที่ใช้ใน force_scroll_down()
def log(message):
    print(message) 

def force_scroll_down(window):
    """
    ฟังก์ชันช่วยเลื่อนหน้าจอลง (Scroll) โดยใช้ Mouse Wheel
    ดึงค่าทั้งหมดจาก SCROLL_CONFIG
    """
    try:
        # ดึงค่าจาก Config
        scroll_dist = int(SCROLL_CONFIG.get('scroll_distance', -5))
        center_x_offset = int(SCROLL_CONFIG.get('scroll_center_x_offset', 300))
        center_y_offset = int(SCROLL_CONFIG.get('scroll_center_y_offset', 300))
    except ValueError:
        log("[!] Scroll Config values are not valid integers. Using defaults.")
        scroll_dist, center_x_offset, center_y_offset = -5, 300, 300

    log(f"...กำลังเลื่อนหน้าจอลง (Mouse Wheel {scroll_dist})...")
    
    try:
        rect = window.rectangle()
        
        # คำนวณจุดกลางหน้าจอตาม Offset จาก Config
        center_x = rect.left + center_x_offset
        center_y = rect.top + center_y_offset
        
        # คลิกเพื่อให้หน้าจอ Focus ก่อนเลื่อน
        mouse.click(coords=(center_x, center_y))
        time.sleep(0.5)
        
        # สั่งเลื่อนเมาส์
        mouse.scroll(coords=(center_x, center_y), wheel_dist=scroll_dist)
        time.sleep(1)
        
    except Exception as e:
        log(f"[!] Mouse scroll failed: {e}")
        # Fallback: ถ้าใช้เมาส์ไม่ได้ ให้ลองกดปุ่ม Page Down แทน
        window.type_keys("{PGDN}")


# ================= 3. Test Function หลัก =================

def test_paymentagent_scanagentbarcode():
    print("[*] 1. กำลังเช็คว่าอยู่หน้าหลักไหม...")

    # ใช้ค่าจาก APP_CONFIG
    WINDOW_TITLE = APP_CONFIG.get("window_title")
    BACKEND = APP_CONFIG.get("backend")
    # ต้องแปลงค่าตัวเลขเป็น int
    TIMEOUT = int(APP_CONFIG.get("timeout", 10)) 

    try:
        app = Application(backend=BACKEND).connect(title_re=WINDOW_TITLE, timeout=TIMEOUT)
        print("Debug: App connected.") # เพิ่มบรรทัดนี้

        main_window = app.top_window()
        main_window.set_focus()
        print("Debug: Main window focused.") # เพิ่มบรรทัดนี้
        print("[/] เชื่อมต่อสำเร็จ")

        # เพิ่ม print selector ตรงนี้อีกครั้ง
        menu_A_selectors = ELEMENT_CONFIG['click_menu_A']
        print(f"Debug: Trying to click with selectors: {menu_A_selectors}") 

        main_window.child_window(**menu_A_selectors).click_input()

        # ========= ขั้นตอนคลิกเมนู S =========
        main_window.child_window(**ELEMENT_CONFIG['click_menu_S']).click_input()
        time.sleep(1)

        # ========= Scroll ลง (ใช้ฟังก์ชันและ Config) =========
        force_scroll_down(main_window)

        # ========= คลิกช่องเบอร์โทร =========
        main_window.child_window(**ELEMENT_CONFIG['click_phone_number_field']).click_input()
        time.sleep(1)

        # กรอกเบอร์โทร (ใช้ค่าจาก Config)
        phone_keys = ELEMENT_CONFIG['type_phone_number_keys']
        main_window.type_keys(phone_keys)
        time.sleep(1)

        # ========= คลิกอ่านบัตรประชาชน =========
        main_window.child_window(**ELEMENT_CONFIG['click_read_id_card']).click_input()
        time.sleep(1)

        # ========= คลิกถัดไป =========
        main_window.child_window(**ELEMENT_CONFIG['click_next_button']).click_input()
        time.sleep(1)

        print("[/] กรอกข้อมูลสำเร็จ")

    except Exception as e:
        print(f"[X] Error: {e}")


if __name__ == "__main__":
    test_paymentagent_scanagentbarcode()