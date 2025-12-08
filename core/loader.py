# อ่าน .ini แบบ dynamic
import configparser

class ConfigLoader:
    def __init__(self, path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(path, encoding="utf8")

    def section(self, name):
        # คืนค่า dict ของ section
        return dict(self.cfg[name])
