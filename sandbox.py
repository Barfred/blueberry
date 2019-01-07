#!/usr/bin/env python3

from time import sleep
from bluesound.bluesound_subscription_objects import title1, title2, volume, secondsInTrack
from bluesound.bluesound_control import Bluesound
import pifacecad
import lib.lcd_handlers
import lib.bluos_handlers
import logging


def welcome_lcd(cad):
    cad.lcd.clear()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()
    cad.lcd.backlight_on()
    cad.lcd.set_cursor(16, 0)
    cad.lcd.write("Ready as a PI!")
    for i in range(16):
        cad.lcd.move_left()
        sleep(0.1)


logging.basicConfig(filename='/var/log/blueberry.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')


# Initialize the PiFace Control & Dispay
cad = pifacecad.PiFaceCAD()
switch_listener = pifacecad.SwitchEventListener(chip=cad)
welcome_lcd(cad)

# Prepare handlers for bluos events
handleTitle1 = lambda title: lib.bluos_handlers.handleTitle1(title, cad=cad)
handleTitle2 = lambda title: lib.bluos_handlers.handleTitle2(title, cad=cad)
handleVolume = lambda volume: lib.bluos_handlers.handleVolume(volume, cad=cad)
handleSecondsInTrack = lambda seconds: lib.bluos_handlers.handleSecondsInTrack(seconds, cad=cad)

# Register the bluos event handlers in the relevant events
title1.setCallback(handleTitle1)
title2.setCallback(handleTitle2)
volume.setCallback(handleVolume)
secondsInTrack.setCallback(handleSecondsInTrack)

# Initialize the bluos object
bluos = Bluesound("192.168.88.25", 1.0, set([title1, title2, volume, secondsInTrack]))
bluos.start()

# Prepare the event handler wrapper for the piface cad switch events
switch_handler = lambda event: lib.lcd_handlers.switch_handler(event, bluos=bluos)

# Register the piface cad event handlers
for i in range(8):
    switch_listener.register(i, pifacecad.IODIR_FALLING_EDGE, switch_handler)
switch_listener.activate()

logging.info('Blueberry ready')

while True:
    sleep(10)
    logging.debug("Heartbeat")

# TODO: cleanup on exit?
# bluos.stop()
