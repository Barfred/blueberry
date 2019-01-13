import threading
from time import sleep

LCD_SCREEN_WIDTH = 16

class Lcd:
    lock = threading.Lock()

    def __init__(self, cad):
        """
        Initialize the LCD of the PiFace Control and Display unit.
        An instance of pifacecad.PiFaceCAD must be given as argument.
        """

        # Clear and initialize the LCD if we can get a lock.
        self.cad = cad
        with Lcd.lock:
            cad.lcd.clear()
            cad.lcd.blink_off()
            cad.lcd.cursor_off()
            cad.lcd.backlight_on()

    def write(self, text, row=0, col=0, viewport=0):
        with Lcd.lock:
            self.cad.lcd.set_cursor(0, row)
            self.cad.lcd.viewport_corner = 0
            # Make the text exactly same width as the LCD screen
            # and pre-pad and post-pad as needed
            text = " "*col + "{:<{width}.{width}}".format(text, width=LCD_SCREEN_WIDTH-col)
            self.cad.lcd.write(text)

    def popup(self, text, row=0, col=0, viewport=0, duration=2):
        """
        Show a message for a limited time duration and then restore LCD content.

        :param text:
        :param row:
        :param col:
        :param viewport:
        :param duration:
        :return:
        """
        with Lcd.lock:
            self.cad.lcd.set_cursor(LCD_SCREEN_WIDTH+1+col, row)
            self.cad.lcd.write(text)
            self.cad.lcd.viewport_corner = LCD_SCREEN_WIDTH+1
            sleep(duration)
            self.cad.lcd.set_cursor(LCD_SCREEN_WIDTH+1+col, row)
            self.cad.lcd.write(" " * len(text))
            self.cad.lcd.viewport_corner = 0


    def greeting(self, text):
        with Lcd.lock:
            self.cad.lcd.set_cursor(LCD_SCREEN_WIDTH, 0)
            self.cad.lcd.write(text)
            for i in range(16):
                self.cad.lcd.move_left()
                sleep(0.1)
            sleep(0.5)
            self.cad.lcd.set_cursor(LCD_SCREEN_WIDTH, 0)
            self.cad.lcd.write(" "*len(text))
