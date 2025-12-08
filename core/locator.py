# ตัวโหลด element แบบ dynamic
from pywinauto.application import Application

class Locator:
    def __init__(self, env_cfg, loc_cfg):
        self.env = env_cfg
        self.loc = loc_cfg

    def connect_main(self):
        info = self.env.section("app")
        app = Application(backend="uia").connect(
            title_re=info["title_re"],
            timeout=int(info["timeout"])
        )
        return app.top_window()

    def find(self, window, key):
        config = self.loc.section(key)
        # relative element (แบบ dynamic)
        if "relative_to" in config:
            base = self.find(window, config["relative_to"])
            parent = base.parent()
            config = {k: v for k, v in config.items() if k != "relative_to"}
            return parent.child_window(**config)
        return window.child_window(**config)
