#!/usr/bin/env python3

from bluesound.bluesound_subscribe import SubscriptionObject
from bluesound.bluesound_subscription_objects import secondsInTrack
from bluesound.bluesound_control import Bluesound
import pifacecad

def handelTitle1(new_title):
    print("Title1: %s" % new_title)
    cad.lcd.write("Title1:{}".format(new_title))


def handelTitle2(new_title):
    print("Title2: %s" % new_title)
    cad.lcd.write("Title2:{}".format(new_title))


title1 = SubscriptionObject(['status', 'title1'], handelTitle1)
title2 = SubscriptionObject(['status', 'title2'], handelTitle2)


def handelSecondsInTrack(sec):
    print("Seconds: %s" % sec)


cad = pifacecad.PiFaceCAD()
cad.lcd.blink_off()
cad.lcd.cursor_off()
cad.lcd.backlight_on()

secondsInTrack.setCallback(handelSecondsInTrack)

bluos = Bluesound("192.168.88.25", 1.0, set([title1, title2, secondsInTrack]))
bluos.start()

input("Press enter to play..")
bluos.play()

input("Press enter to skip..")
bluos.skip()

input("Press enter to pause..")
bluos.pause()

bluos.stop()
