import config.settings
import logging

def button_handler(event, bluos, lcd):
    handlers = {
        0: button0,
        1: button1,
        2: button2,
        3: button3,
        4: button4,
        5: button5,
        6: button6,
        7: button7,
    }
    logging.debug("button_handler debug pin_num={}".format(str(event.pin_num)))
    handlers.get(event.pin_num)(event, bluos, lcd)


def button0(event, bluos, lcd):
    logging.debug("You pressed: {}".format(str(event.pin_num)))


def button1(event, bluos, lcd):
    lcd.popup("Previous track..")
    bluos.back()
    logging.info("Skipping to previous track")


def button2(event, bluos, lcd):
    lcd.popup("Next track..")
    bluos.skip()
    logging.info("Skipping to next track")


def button3(event, bluos, lcd):
    logging.debug("You pressed: {}".format(str(event.pin_num)))


def button4(event, bluos, lcd):
    logging.debug("You pressed: {}".format(str(event.pin_num)))


def button5(event, bluos, lcd):
    # Selector switch pressed down
    # Function: Play/Pause
    if bluos.getStatus()['state'] == 'pause':
        bluos.play()
        logging.info("Play selected")
    else:
        bluos.pause()
        logging.info("Pause selected")


def button6(event, bluos, lcd):
    # Selector switch pushed to the left
    # Function: Volume down
    currentvolume = int(bluos.getStatus()['volume'])
    newvolume = max(0, currentvolume - config.settings.BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    logging.info("Volume decreased from {} to {}".format(currentvolume, newvolume))

def button7(event, bluos, lcd):
    # Selector switch is pushed to the right
    # Function: Volume up
    currentvolume = int(bluos.getStatus()['volume'])
    newvolume = min(100, currentvolume + config.settings.BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    logging.info("Volume increased from {} to {}".format(currentvolume, newvolume))
