import logging


def showtitle1(cad, title=None):
    logging.debug("handleTitle1 callback called with title {}".format(title))
    cad.updatetitles(title1=title)


def showtitle2(cad, title=None):
    logging.debug("handleTitle2 callback called with title {}".format(title))
    cad.updatetitles(title2=title)


def showvolume(volume, cad):
    logging.debug("Popup display volume on first row: {}".format(volume))
    text = "Volume: {:2}%".format(volume)
    cad.lcdpopup(text)


def showstreamstate(state, cad):
    if state == "connecting":
        logging.debug("State 'connecting'. Skipping status popup")
        return
    state = state.capitalize()
    logging.debug("Popup display state on second row: {}".format(state))
    text = "[ {} ]".format(state)
    cad.lcdpopup(text, row=1)


def showsecondsintrack(sec, cad):
    logging.debug("Seconds: {}".format(sec))
