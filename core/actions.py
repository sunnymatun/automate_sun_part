from pywinauto.mouse import scroll

class Actions:
    def click(self, elem):
        elem.click_input()

    def type(self, window, text):
        window.type_keys(text, with_spaces=True)

    def scroll(self, element, amount=-10):
        rect = element.rectangle()
        scroll(coords=(rect.mid_point().x, rect.mid_point().y),
               wheel_dist=amount)
