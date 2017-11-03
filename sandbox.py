#!/usr/bin/env python3

def handelTitle1(new_title):
    print("Title1: %s" % new_title)

def handelTitle2(new_title):
    print("Title2: %s" % new_title)


from bluesound.bluesound_subscribe import SubscriptionObject
title1 = SubscriptionObject(['status', 'title1'], handelTitle1)
title2 = SubscriptionObject(['status', 'title2'], handelTitle1)

from bluesound.bluesound_subscription_objects import secondsInTrack

def handelSecondsInTrack(sec):
    print("Seconds: %s" % sec)

secondsInTrack.setCallback(handelSecondsInTrack)

from bluesound.bluesound_control import Bluesound
bluos = Bluesound("192.168.88.23", 1.0, set([title1, title2, secondsInTrack]))
bluos.start()

input("Press enter to play..")
bluos.play()

input("Press enter to skip..")
bluos.skip()

input("Press enter to pause..")
bluos.pause()

bluos.stop()