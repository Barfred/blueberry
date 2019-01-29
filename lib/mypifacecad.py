# This class is enhanced to handles updates to the piface LCD screen
# and keep track of UI state

import threading
import logging
from time import sleep
from pifacecad import PiFaceCAD
from lib.uistatemachine import UIStateMachine


LCD_SCREEN_WIDTH = 16
ARROW_BITMAP = [
    0b11000,
    0b11100,
    0b11010,
    0b11001,
    0b11010,
    0b11100,
    0b11000,
    0b00000
]

class MyPiFaceCAD(PiFaceCAD):
    lcdlock = threading.Lock()

    def __init__(self):
        """
        Initialize the LCD of the PiFace Control and Display device.
        """
        super(MyPiFaceCAD, self).__init__()

        self.state = UIStateMachine()
        self.menu = None  # will be initialized later
        self.title1 = "No title"
        self.title2 = "No title"

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

    def updatetitles(self, title1=None, title2=None):
        """
        Update player screen with title1 and title2. If one or both titles
        are given as arguments, then it's stored on the object instance for later.
        If one or both titles are not given as arguments, the stored values
        are used instead.
        """
        if title1:
            self.title1 = title1
        if title2:
            self.title2 = title2

        if self.getstate() == 'player':
            logging.debug("Display player screen \"{}\"/\"{}\"".format(self.title2, self.title1))
            self.lcdwrite(self.title1, row=1)
            self.lcdwrite(self.title2, row=0)


    def lcdwritemenu(self):
        """
        Write menu items on the LCD and highlight the selected item.
        A blank line is written if there is no menu item to write.
        :return:
        """
        for i in range(2):
            if len(self.menu.menuitems) > self.menu.cursoritem+i:
                text = self.menu.menuitems[self.menu.cursoritem+i]['@text']
            else:
                text = ""
            if self.menu.highlightitem == self.menu.cursoritem+i:
                text = "> " + text
            else:
                text = "  " + text
            logging.debug("lcdwritemenu text = {}".format(text))
            self.lcdwrite(text, row=i)

    def lcdpopup(self, text, row=0, col=0, viewport=0, duration=1.0):
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

    def getstate(self):
        return self.state.current_state_value


    def nextstate(self):
        # The menu state graph is just a simple circle with no branches.
        # Therefore there is only one allowed transition from any state.
        # Pick the first (and only) allowed transition and call that:
        self.state.allowed_transitions[0]()

    def populatemenu(self, menulist):
        # todo: should we check if self.menu already is a Menu class object
        # and if so, delete it first?
        self.menu = Menu(menulist)


class Menu():
    """
    The menu is populated with a list of menu items, and manages the viewport
    (which two lines are displayed) and the highlighted item (the one that
    is subject for selection).
        menuitems: list of menu item objects
        highlightitem: the index of the currently highlighted item
        cursoritem: the index of the menu item to be displayed on top row
    """
    def __init__(self, menuitems):
        self.highlightitem = 0
        self.cursoritem = 0
        self.menuitems = menuitems

    def highlightnext(self):
        if self.highlightitem < len(self.menuitems)-1:
            self.highlightitem += 1
        if not self.highlightisvisible():
            self.cursoritem = self.highlightitem
        logging.debug("Menu highlightnext: highlightitem={}, cursoritem={}".format(self.highlightitem, self.cursoritem))

    def highlightprevious(self):
        if self.highlightitem > 0:
            self.highlightitem -= 1
        if not self.highlightisvisible():
            self.cursoritem = self.highlightitem
        logging.debug("Menu highlightnext: highlightitem={}, cursoritem={}".format(self.highlightitem, self.cursoritem))

    def highlightisvisible(self):
        if self.highlightitem in (self.cursoritem, self.cursoritem+1):
            logging.debug("highlightisvisible: {}, cursoritem: {}, return True".format(self.highlightitem, self.cursoritem))
            return True
        else:
            logging.debug("highlightisvisible: {}, cursoritem: {}, return False".format(self.highlightitem, self.cursoritem))
            return False
