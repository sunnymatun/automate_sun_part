import configparser
import os

CONFIG_FILE = "config.ini"

def read_config(filename=CONFIG_FILE):
    config = configparser.ConfigParser()
    try:
        if not os.path.exists(filename):
            print(f"[X] ไม่พบไฟล์ config: {os.path.abspath(filename)}")
            return config

        config.read(filename, encoding='utf-8')
        return config
    except Exception as e:
        print(f"[X] อ่าน config ไม่สำเร็จ: {e}")
        return config
