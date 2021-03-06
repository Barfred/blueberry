from config.settings import BLUOS_VOLUME_STEP
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
    # TODO: skip event in case of double-fire (multiple events on the same
    # button in a short time interval)
    logging.debug("button_handler debug pin_num={}".format(str(event.pin_num)))
    handlers.get(event.pin_num)(event, bluos, cad)


def button0(event, bluos, cad):
    # This button cycles through UI states
    cad.nextmenustate()
    state = cad.getstate()
    logging.debug("UI State is now: {}".format(state))

    if state == 'player':
        cad.updatetitles()

    elif state == 'radioselect':
        cad.lcdpopup("Menu: Radio")
        cad.populatemenu(bluos.getRadioPresets()['item'])
        # TODO: handle case where menu is empty
        cad.lcdwritemenu()

    elif state == 'playlistselect':
        cad.lcdpopup("Menu: Playlists")
        cad.populatemenu(bluos.getPlaylists()['name'])
         # TODO: handle case where menu is empty
        cad.lcdwritemenu()

    elif state == 'queueselect':
        cad.lcdpopup("Menu: Queue")
        cad.populatemenu(bluos.getQueue()['song'])
        # TODO: handle case where menu is empty
        cad.lcdwritemenu()


def button1(event, bluos, cad):
    state = cad.getstate()
    if state == 'player':
        cad.lcdpopup("Previous track..")
        bluos.back()
    elif state in ('radioselect', 'playlistselect', 'queueselect'):
        cad.menu.highlightprevious()
        cad.lcdwritemenu()


def button2(event, bluos, cad):
    state = cad.getstate()
    if state == 'player':
        cad.lcdpopup("Next track..")
        bluos.skip()
    elif state in ('radioselect', 'playlistselect', 'queueselect'):
        cad.menu.highlightnext()
        cad.lcdwritemenu()


def button3(event, bluos, cad):
    state = cad.getstate()

    if state == 'player':
        cad.lcdpopup("Next track..")
        bluos.skip()

    elif state == 'radioselect':
        # Play the radiostation
        url = cad.menu.menuitems[cad.menu.highlightitem]['@URL']
        logging.debug("playing radiostation {} from url {}".format(cad.menu.menuitems[cad.menu.highlightitem]['@text'], url))
        cad.updatetitles(title1="", title2="")
        bluos.play(url=url)
        cad.state.playradio()

    elif state == 'playlistselect':
        name = cad.menu.menuitems[cad.menu.highlightitem]['@text']
        logging.debug("playing playlist {}".format(name))
        cad.updatetitles(title1="", title2="")
        bluos.queuePlaylist(name)
        cad.state.playplaylist()

    elif state == 'queueselect':
        logging.debug("playing song id {} from queue".format(cad.menu.highlightitem))
        cad.updatetitles(title1="", title2="")
        bluos.play(id=cad.menu.highlightitem)
        cad.state.playqueue()


def button4(event, bluos, cad):
    cad.lcdbacklight(action='toggle')


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
    newvolume = max(0, currentvolume - BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    logging.info("Volume decreased from {} to {}".format(currentvolume, newvolume))


def button7(event, bluos, cad):
    # Selector switch is pushed to the right
    # Function: Volume up
    currentvolume = int(bluos.getStatus()['volume'])
    newvolume = min(100, currentvolume + BLUOS_VOLUME_STEP)
    bluos.volume(newvolume)
    logging.info("Volume increased from {} to {}".format(currentvolume, newvolume))
