# controls.py

import config.settings


def switch_handler(event, bluos):
    handlers = {
        0: button0,
        1: button1,
        2: button2,
        3: button3,
        4: button4,
        5: button6,
        6: button6,
        7: button7,
    }
    print("Switch_handler debug pin_num={}".format(str(event.pin_num)))
    handlers.get(event.pin_num, lambda: "Invalid button")(event, bluos)


def button0(event, bluos):
    event.chip.cad.lcd.clear()
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("You pressed: {}".format(str(event.pin_num)))


def button1(event, bluos):
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("You pressed: {}".format(str(event.pin_num)))


def button2(event, bluos):
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("You pressed: {}".format(str(event.pin_num)))


def button3(event, bluos):
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("You pressed: {}".format(str(event.pin_num)))


def button4(event, bluos):
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("You pressed: {}".format(str(event.pin_num)))


def button5(event, bluos):
    # Selector switch is pressed
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("You pressed: {}".format(str(event.pin_num)))


def button6(event, bluos):
    # Selector switch pushed to the left
    # Function: Volume down
    currentvolume = int(bluos.getStatus()['volume'])
    newvolume = max(0, currentvolume - config.settings.BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("Volume: {:2}%     ".format(newvolume))


def button7(event, bluos):
    # Selector switch is pushed to the right
    # Function: Volume up
    """

    :type bluos: object
    """
    print("Button7 pressed")
    currentvolume = int(bluos.getStatus()['volume'])
    print("Got old volume {}".format(currentvolume))
    newvolume = min(100, currentvolume + config.settings.BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    event.chip.lcd.set_cursor(0, 0)
    event.chip.lcd.write("Volume: {:2}%     ".format(newvolume))

