import logging


def handleTitle1(title, cad):
    logging.debug("Display title1 on second row: {}".format(title))
    cad.lcdwrite(title, row=1)


def handleTitle2(title, cad):
    logging.debug("Display title1 on first row: {}".format(title))
    cad.lcdwrite(title, row=0)


def handleVolume(volume, cad):
    logging.debug("Popup display volume on first row: {}".format(volume))
    text = "Volume: {:2}%".format(volume)
    cad.lcdpopup(text)


def handleStreamState(state, cad):
    if state == "connecting":
        logging.debug("State 'connecting'. Skipping status popup")
        return
    state = state.capitalize()
    logging.debug("Popup display state on second row: {}".format(state))
    text = "[ {} ]".format(state)
    cad.lcdpopup(text, row=1)


def handleSecondsInTrack(sec, cad):
    logging.debug("Seconds: {}".format(sec))
