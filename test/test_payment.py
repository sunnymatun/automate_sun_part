from core.loader import ConfigLoader
from core.locator import Locator
from core.actions import Actions
import time

def test_payment():
    env = ConfigLoader("config/env.ini")
    loc = ConfigLoader("config/locator.ini")

    locator = Locator(env, loc)
    actions = Actions()

    main = locator.connect_main()
    main.set_focus()

    # menu A
    actions.click(locator.find(main, "menu_payment_agent"))
    time.sleep(1)

    # menu S
    actions.click(locator.find(main, "menu_sell_page"))
    time.sleep(1)

    # click read card
    actions.click(locator.find(main, "read_card_button"))
    time.sleep(1)

    # scroll page
    doc = main.child_window(control_type="Document")
    actions.scroll(doc)

    # phone input
    phone_input = locator.find(main, "phone_input")
    actions.click(phone_input)
    actions.type(main, "0987654321")

    print("✔ DONE")

if __name__ == "__main__":
    test_payment()
