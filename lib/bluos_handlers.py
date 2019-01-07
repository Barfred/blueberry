import config.settings
import logging


def handleTitle1(title, cad):
    logging.debug("Set title1 to {}".format(title))
    cad.lcd.viewport_corner = 0
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write("{:16}".format(title))


def handleTitle2(title, cad):
    logging.debug("Set title2 to {}".format(title))
    cad.lcd.viewport_corner = 0
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write("{:16}".format(title))


def handleVolume(volume, cad):
    logging.debug("Set volume to {}".format(volume))
    cad.lcd.viewport_corner = 0
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write("Volume: {:2}%     ".format(volume))


def handleSecondsInTrack(sec, cad):
    logging.debug("Seconds: {}".format(sec))
