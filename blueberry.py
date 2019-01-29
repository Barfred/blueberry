#!/usr/bin/env python3

import logging
from time import sleep

from bluesound.bluesound_control import Bluesound
from bluesound.bluesound_subscription_objects import title1, title2, volume, secondsInTrack, streamState
import lib.bluos_handlers
import lib.pyface_button_handlers
from lib.mypifacecad import MyPiFaceCAD
from pifacecad import SwitchEventListener
import pifacecad

logging.basicConfig(filename='/var/log/blueberry.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


# Initialize the PiFace Control & Dispay device
cad = MyPiFaceCAD()
switch_listener = SwitchEventListener(chip=cad)


logging.debug("State machine state: {}".format(cad.getstate()))
cad.lcdgreeting("Ready as a PI!")

# Prepare handlers for bluos events, e.g. title and volume changes
handleTitle1 = lambda title: lib.bluos_handlers.handleTitle1(cad=cad, title=title)
handleTitle2 = lambda title: lib.bluos_handlers.handleTitle2(cad=cad, title=title)
handleVolume = lambda volume: lib.bluos_handlers.handleVolume(volume, cad=cad)
handleSecondsInTrack = lambda seconds: lib.bluos_handlers.handleSecondsInTrack(seconds, cad=cad)
handleStreamState = lambda state: lib.bluos_handlers.handleStreamState(state, cad=cad)

# Register the bluos event handlers
title1.setCallback(handleTitle1)
title2.setCallback(handleTitle2)
volume.setCallback(handleVolume)
secondsInTrack.setCallback(handleSecondsInTrack)
streamState.setCallback(handleStreamState)

# Initialize the bluos device and start the thread
bluos = Bluesound("192.168.88.25", 1.0, set([title1, title2, volume, secondsInTrack, streamState]))
bluos.start()

# Prepare the event handler wrapper for the piface cad button events
button_handler = lambda event: lib.pyface_button_handlers.button_handler(event, bluos=bluos, cad=cad)
# Register the piface cad event handlers
for i in range(8):
    switch_listener.register(i, pifacecad.IODIR_FALLING_EDGE, button_handler)
switch_listener.activate()

logging.info('Blueberry ready')

while True:
    sleep(10)
    logging.debug("Heartbeat")

# TODO: cleanup on exit?
# bluos.stop()
