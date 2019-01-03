#!/usr/bin/env python3

from time import sleep
from bluesound.bluesound_subscription_objects import secondsInTrack, title1, title2, volume
from bluesound.bluesound_control import Bluesound
import pifacecad
import lib.controls
import logging

logging.basicConfig(filename='/var/log/blueberry.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s')

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
#    sleep(1)


def handleTitle1(new_title):
    logging.debug("Set title1 to {}".format(new_title))
    cad.lcd.viewport_corner = 0
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write("{:16}".format(new_title))


def handleTitle2(new_title):
    logging.debug("Set title2 to {}".format(new_title))
    cad.lcd.viewport_corner = 0
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write("{:16}".format(new_title))


def handleSecondsInTrack(sec):
    logging.debug("Seconds: {}".format(sec))


# Initialize the PiFace Control & Dispay
cad = pifacecad.PiFaceCAD()
switch_listener = pifacecad.SwitchEventListener(chip=cad)
welcome_lcd(cad)

title1.setCallback(handleTitle1)
title2.setCallback(handleTitle2)
secondsInTrack.setCallback(handleSecondsInTrack)

bluos = Bluesound("192.168.88.25", 1.0, set([title1, title2, secondsInTrack]))
bluos.start()

switch_handler = lambda event: lib.controls.switch_handler(event, bluos=bluos)
for i in range(8):
    switch_listener.register(i, pifacecad.IODIR_FALLING_EDGE, switch_handler)
switch_listener.activate()

logging.info('Blueberry ready')

while True:
    sleep(10)
    logging.debug("Heartbeat")

input("Press enter to play..")
bluos.play()

input("Press enter to skip..")
bluos.skip()

input("Press enter to pause..")
bluos.pause()

bluos.stop()
