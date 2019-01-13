# This class is enhanced to handles updates to the piface LCD screen

import threading
from time import sleep
from pifacecad import PiFaceCAD

LCD_SCREEN_WIDTH = 16


class MyPiFaceCAD(PiFaceCAD):
    lcdlock = threading.Lock()

    def __init__(self):
        """
        Initialize the LCD of the PiFace Control and Display device.
        """
        super(MyPiFaceCAD, self).__init__()

        # Clear and initialize the LCD if we can get a lock.
        with MyPiFaceCAD.lcdlock:
            self.lcd.clear()
            self.lcd.blink_off()
            self.lcd.cursor_off()
            self.lcd.backlight_on()

    def lcdwrite(self, text, row=0, col=0, viewport=0):
        with MyPiFaceCAD.lcdlock:
            self.lcd.set_cursor(0, row)
            self.lcd.viewport_corner = 0
            # Make the text exactly same width as the LCD screen
            # and pre-pad and post-pad as needed
            text = " " * col + "{:<{width}.{width}}".format(text, width=LCD_SCREEN_WIDTH - col)
            self.lcd.write(text)

    def lcdpopup(self, text, row=0, col=0, viewport=0, duration=2):
        """
        Show a message for a limited time duration and then restore LCD content.

        :param text:
        :param row:
        :param col:
        :param viewport:
        :param duration:
        :return:
        """
        with MyPiFaceCAD.lcdlock:
            self.lcd.set_cursor(LCD_SCREEN_WIDTH + 1 + col, row)
            self.lcd.write(text)
            self.lcd.viewport_corner = LCD_SCREEN_WIDTH + 1
            sleep(duration)
            self.lcd.set_cursor(LCD_SCREEN_WIDTH + 1 + col, row)
            self.lcd.write(" " * len(text))
            self.lcd.viewport_corner = 0

    def lcdgreeting(self, text):
        with MyPiFaceCAD.lcdlock:
            self.lcd.set_cursor(LCD_SCREEN_WIDTH, 0)
            self.lcd.write(text)
            for i in range(16):
                self.lcd.move_left()
                sleep(0.1)
            sleep(0.5)
            self.lcd.set_cursor(LCD_SCREEN_WIDTH, 0)
            self.lcd.write(" " * len(text))
