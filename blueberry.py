#!/usr/bin/env python3

import logging
from time import sleep

from bluesound.bluesound_control import Bluesound
from bluesound.bluesound_subscription_objects import title1, title2, volume, secondsInTrack, streamState
from lib.bluos_handlers import showtitle1, showtitle2, showvolume, showsecondsintrack, showstreamstate
from lib.pyface_button_handlers import button_handler
from lib.mypifacecad import MyPiFaceCAD
from pifacecad import SwitchEventListener, IODIR_FALLING_EDGE
from config.settings import BLUOS_IP_ADDRESS

logging.basicConfig(filename='/var/log/blueberry.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

# Initialize the PiFace Control & Dispay device
cad = MyPiFaceCAD()
switch_listener = SwitchEventListener(chip=cad)

cad.lcdgreeting("Ready as a PI!")

# Prepare handlers for bluos events, e.g. title and volume changes
handletitle1 = lambda title: showtitle1(cad=cad, title=title)
handletitle2 = lambda title: showtitle2(cad=cad, title=title)
handlevolume = lambda volume: showvolume(volume, cad=cad)
handlesecondsintrack = lambda seconds: showsecondsintrack(seconds, cad=cad)
handlestreamstate = lambda state: showstreamstate(state, cad=cad)

# Register the bluos event handlers
title1.setCallback(handletitle1)
title2.setCallback(handletitle2)
volume.setCallback(handlevolume)
secondsInTrack.setCallback(handlesecondsintrack)
streamState.setCallback(handlestreamstate)

# Initialize the bluos device and start the thread
bluos = Bluesound(BLUOS_IP_ADDRESS, 1.0, set([title1, title2, volume, secondsInTrack, streamState]))
bluos.start()

# Prepare the event handler wrapper for the piface cad button events
cad_button_handler = lambda event: button_handler(event, bluos=bluos, cad=cad)
# Register the piface cad event handlers
for i in range(8):
    switch_listener.register(i, IODIR_FALLING_EDGE, cad_button_handler)
switch_listener.activate()

logging.info('Blueberry ready')

while True:
    sleep(10)
    logging.debug("Heartbeat")

# TODO: cleanup threads on exit?
# e.g. bluos.stop()
