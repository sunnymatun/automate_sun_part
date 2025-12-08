from pywinauto.application import Application
from pywinauto.mouse import wheel_mouse_input
import time
# ใช้ configparser แทน json
import configparser 
import os 

# ================= Config Loader =================

def load_ini_config(file_path):
    """โหลดและจัดระเบียบข้อมูลจากไฟล์ INI ให้เป็นโครงสร้าง Dict ที่ใช้งานง่าย"""
    config = configparser.ConfigParser()
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file not found: {file_path}")
        
    config.read(file_path, encoding='utf-8')
    
    # แปลง INI data ให้เป็น Dict เพื่อให้เข้าถึงได้ง่ายเหมือน JSON เดิม
    app_config = dict(config.items('APP_CONFIG'))
    test_data = dict(config.items('DATA'))
    elements_config = {}
    
    # จัดกลุ่ม key-value ของ Elements เข้าด้วยกัน (เช่น A_title, A_auto_id)
    element_map = config.items('ELEMENTS')
    
    current_element_name = None
    current_element_dict = {}

    for key, value in element_map:
        # แยกชื่อ Element (เช่น 'click_menu_A') และ Selector Type (เช่น 'title')
        parts = key.rsplit('_', 1)
        element_name = "_".join(parts[:-1]) # click_menu_A
        selector_type = parts[-1]          # title, auto_id, control_type

        if element_name != current_element_name:
            if current_element_name is not None:
                elements_config[current_element_name] = current_element_dict
            
            current_element_name = element_name
            current_element_dict = {}

        current_element_dict[selector_type] = value
    
    # เพิ่ม element สุดท้าย
    if current_element_name is not None:
         elements_config[current_element_name] = current_element_dict

    return app_config, elements_config, test_data

# โหลด config ตั้งแต่แรก
try:
    APP_CONFIG, ELEMENT_CONFIG, TEST_DATA = load_ini_config('element_config.ini')
except FileNotFoundError as e:
    print(f"[CRITICAL ERROR] {e}")
    exit(1)


# ================= Test Function (Using INI Config) =================

def test_paymentagent_scanagentbarcode():
    print("[*] 1. กำลังเช็คว่าอยู่หน้าหลักไหม...")

    # ใช้ค่าจาก Config (INI อ่านค่ามาเป็น string ทั้งหมด)
    WINDOW_TITLE = APP_CONFIG["window_title"]
    BACKEND = APP_CONFIG["backend"]
    # ต้องแปลงค่าตัวเลขให้เป็น int
    TIMEOUT = int(APP_CONFIG["timeout"]) 

    try:
        # เชื่อมต่อ
        app = Application(backend=BACKEND).connect(title_re=WINDOW_TITLE, timeout=TIMEOUT)
        main_window = app.top_window()
        main_window.set_focus()
        print("[/] เชื่อมต่อสำเร็จ")

        # ========= ขั้นตอนคลิกเมนู A =========
        # ใช้ Dict unpack ** ในการส่งค่าจาก Config เข้าไปใน child_window()
        main_window.child_window(**ELEMENT_CONFIG['click_menu_A']).click_input()
        time.sleep(1)

        # ========= ขั้นตอนคลิกเมนู S =========
        main_window.child_window(**ELEMENT_CONFIG['click_menu_S']).click_input()
        time.sleep(1)

        # ========= Scroll ลง =========
        print("[*] Scroll ลง...")
        wheel_mouse_input(wheel_dist=-5)

        # ========= คลิกช่องเบอร์โทร =========
        main_window.child_window(**ELEMENT_CONFIG['click_phone_number_field']).click_input()
        time.sleep(1)

        # กรอกเบอร์โทร (ใช้ค่าจาก DATA Section)
        phone_keys = TEST_DATA['type_phone_number_keys']
        main_window.type_keys(phone_keys)
        time.sleep(1)
        
        # ... ส่วนที่เหลือของโค้ดที่ยังไม่ได้แปลงเป็น Config ในตัวอย่างด้านบน ...
        
        print("[/] กรอกข้อมูลสำเร็จ")

    except Exception as e:
        print(f"[X] Error: {e}")

if __name__ == "__main__":
    test_paymentagent_scanagentbarcode()