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
        self.backlight_on = True

        # Clear and initialize the LCD if we can get a lock.
        with MyPiFaceCAD.lcdlock:
            self.lcd.clear()
            self.lcd.blink_off()
            self.lcd.cursor_off()
            self.lcd.backlight_on()

    def lcdbacklight(self, action='toggle'):
        """
        Control the LCD backlight according to mode.
        :param action:
            'toggle' (default): Toggle the backlight
            'on': Switch the backlight on
            'off': Switch the backlight off
        """
        if action == 'toggle':
            if self.backlight_on:
                with MyPiFaceCAD.lcdlock:
                    self.lcd.backlight_off()
                self.backlight_on = False
            else:
                with MyPiFaceCAD.lcdlock:
                    self.lcd.backlight_on()
                self.backlight_on = True
        elif action == 'on':
            with MyPiFaceCAD.lcdlock:
                self.lcd.backlight_on()
            self.backlight_on = True
        elif action == 'off':
            with MyPiFaceCAD.lcdlock:
                self.lcd.backlight_off()
            self.backlight_on = False
        else:
            logging.warning("lcdbacklight method does not support mode {}".format(action))

    def lcdwrite(self, text, row=0, col=0, viewport=0):
        with MyPiFaceCAD.lcdlock:
            self.lcd.set_cursor(0, row)
            self.lcd.viewport_corner = 0
            # Make the text exactly same width as the LCD screen
            # and pre-pad and post-pad with spaces as needed
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
        Write menu items on the LCD and highlight the currently selected item.
        A blank line is written if there is no menu item to write.
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
        Show a text for a limited time duration and then restore LCD content.
        The text is shown on either first or second row. It can not span
        both rows.
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
        """
        Display a text running into the LCD from right to left, leave it there
        for 0.5 seconds and clear the row.
        """
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
        """
        Get the current UI state. See uistatemachine.py for possible
        states.
        """
        return self.state.current_state_value

    def nextmenustate(self):
        """
        Transition the UI state to to the next menu state.

        By convention there is just one transition from one menu state
        to the next menu state, and it's identifier ends with 'nextmenu'.
        """
        for transition in self.state.allowed_transitions:
            ident = transition.identifier
            if ident.endswith('nextmenu'):
                logging.debug("State transition to next menu: {}".format(ident))
                transition()
                return True
        return False

    def populatemenu(self, menulist):
        """
        Create a new instance of the menu and populate it with the specified
        content.
        """
        # todo: should this check if self.menu already is a Menu class object?
        # and if so, delete it first?
        self.menu = Menu(menulist)


class Menu():
    """
    The menu is populated with a list of menu items, and keeps track of an
    index of the the viewport (which two lines are displayed on the LCD) and
    an index of the currently highlighted item (the one that is subject for
    selection).
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

    def highlightprevious(self):
        if self.highlightitem > 0:
            self.highlightitem -= 1
        if not self.highlightisvisible():
            self.cursoritem = self.highlightitem

    def highlightisvisible(self):
        if self.highlightitem in (self.cursoritem, self.cursoritem+1):
            return True
        else:
            return False
