import config.settings
import logging


def button_handler(event, bluos, cad):
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
    handlers.get(event.pin_num)(event, bluos, cad)


def button0(event, bluos, cad):
    # This button cycles through UI states
    cad.nextstate()
    logging.debug("UI State is now: {}".format(cad.getstate()))
    if cad.getstate() == 'player':
        cad.updatetitles()
    elif cad.getstate() == 'presetradioselect':
        cad.lcdpopup("Menu: Radio")
        cad.populatemenu(bluos.getRadioPresets()['item'])
        # TODO: handle case where menu is empty
        logging.debug("got radio stations")
        cad.lcdwritemenu()
        logging.debug("menu written to lcd")


def button1(event, bluos, cad):
    state = cad.getstate()
    if state == 'player':
        cad.lcdpopup("Previous track..")
        bluos.back()
    elif state == 'presetradioselect':
        cad.menu.highlightprevious()
        cad.lcdwritemenu()


def button2(event, bluos, cad):
    state = cad.getstate()
    if state == 'player':
        cad.lcdpopup("Next track..")
        bluos.skip()
    elif state == 'presetradioselect':
        cad.menu.highlightnext()
        cad.lcdwritemenu()


def button3(event, bluos, cad):
    state = cad.getstate()
    if state == 'player':
#        cad.lcdpopup("Next track..")
#        bluos.skip()
        pass
    elif state == 'presetradioselect':
        # Play the radiostation
        url = cad.menu.menuitems[cad.menu.highlightitem]['@URL']
        logging.debug("playing radiostation {} from url {}".format(cad.menu.menuitems[cad.menu.highlightitem]['@text'], url))
        bluos.play(url=url)
        cad.state.showplayer()


def button4(event, bluos, cad):
    logging.debug("You pressed: {}".format(str(event.pin_num)))


def button5(event, bluos, cad):
    # Selector switch pressed down
    # Function: Play/Pause
    if bluos.getStatus()['state'] == 'pause':
        bluos.play()
        logging.info("Play selected")
    else:
        bluos.pause()
        logging.info("Pause selected")


def button6(event, bluos, cad):
    # Selector switch pushed to the left
    # Function: Volume down
    currentvolume = int(bluos.getStatus()['volume'])
    newvolume = max(0, currentvolume - config.settings.BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    logging.info("Volume decreased from {} to {}".format(currentvolume, newvolume))

def button7(event, bluos, cad):
    # Selector switch is pushed to the right
    # Function: Volume up
    currentvolume = int(bluos.getStatus()['volume'])
    newvolume = min(100, currentvolume + config.settings.BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    logging.info("Volume increased from {} to {}".format(currentvolume, newvolume))
