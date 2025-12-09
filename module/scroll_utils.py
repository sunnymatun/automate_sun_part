from pywinauto import mouse
import time

def force_scroll_down(window, config):
    try:
        center_x_offset = config.getint('MOUSE_SCROLL', 'CENTER_X_OFFSET')
        center_y_offset = config.getint('MOUSE_SCROLL', 'CENTER_Y_OFFSET')
        wheel_dist = config.getint('MOUSE_SCROLL', 'WHEEL_DIST')
        focus_delay = config.getfloat('MOUSE_SCROLL', 'FOCUS_DELAY')
        scroll_delay = config.getfloat('MOUSE_SCROLL', 'SCROLL_DELAY')
    except:
        center_x_offset, center_y_offset, wheel_dist, focus_delay, scroll_delay = 300, 300, -20, 0.5, 1.0

    rect = window.rectangle()
    center_x = rect.left + center_x_offset
    center_y = rect.top + center_y_offset

    print("...เลื่อนจอ...")

    mouse.click(coords=(center_x, center_y))
    time.sleep(focus_delay)

    mouse.scroll(coords=(center_x, center_y), wheel_dist=wheel_dist)
    time.sleep(scroll_delay)
