import logging


def handleTitle1(title, lcd):
    logging.debug("Display title1 on second row: {}".format(title))
    lcd.write(title, row=1)


def handleTitle2(title, lcd):
    logging.debug("Display title1 on first row: {}".format(title))
    lcd.write(title, row=0)


def handleVolume(volume, lcd):
    logging.debug("Popup display volume on first row: {}".format(volume))
    text = "Volume: {:2}%".format(volume)
    lcd.popup(text)


def handleStreamState(state, lcd):
    if state == "connecting":
        logging.debug("State 'connecting'. Skipping status popup")
        return
    state = state.capitalize()
    logging.debug("Popup display state on second row: {}".format(state))
    text = "[ {} ]".format(state)
    lcd.popup(text, row=1)


def handleSecondsInTrack(sec, lcd):
    logging.debug("Seconds: {}".format(sec))
