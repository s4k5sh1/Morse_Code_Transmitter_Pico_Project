# lcd_api.py
"""Implements the API for talking with HD44780 compatible character LCDs."""

import time

# lcd_api.py

class LcdApi:
    # Command constants from the HD44780U datasheet
    LCD_CLR = 0x01               # DB0: clear display
    LCD_HOME = 0x02              # DB1: return to home position
    LCD_ENTRY_MODE = 0x04        # DB2: set entry mode
    LCD_ENTRY_INC = 0x02         # DB1: increment
    LCD_ENTRY_SHIFT = 0x01       # DB0: shift
    LCD_ON_CTRL = 0x08           # DB3: turn lcd/cursor on
    LCD_ON_DISPLAY = 0x04        # DB2: turn display on
    LCD_ON_CURSOR = 0x02         # DB1: turn cursor on
    LCD_ON_BLINK = 0x01          # DB0: blinking cursor
    LCD_MOVE = 0x10              # DB4: move cursor/display
    LCD_MOVE_DISP = 0x08         # DB3: move display (0-> move cursor)
    LCD_MOVE_RIGHT = 0x04        # DB2: move right (0-> left)
    LCD_FUNCTION = 0x20          # DB5: function set
    LCD_FUNCTION_8BIT = 0x10     # DB4: set 8BIT mode (0->4BIT mode)
    LCD_FUNCTION_2LINES = 0x08   # DB3: two lines (0->one line)
    LCD_FUNCTION_10DOTS = 0x04   # DB2: 5x10 font (0->5x7 font)
    LCD_CGRAM = 0x40             # DB6: set CG RAM address
    LCD_DDRAM = 0x80             # DB7: set DD RAM address

    LCD_RS_CMD = 0
    LCD_RS_DATA = 1

    LCD_CMD_INIT = 0x33
    LCD_CMD_INIT_4BIT = 0x02
    LCD_CMD_DISPLAY_CONTROL = 0x08

    def __init__(self, num_lines, num_columns):
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.cursor_x = 0
        self.cursor_y = 0
        self.display_control = self.LCD_ON_DISPLAY

        self.init_lcd()

    def init_lcd(self):
        # Initialization sequence
        self.hal_write_command(self.LCD_CMD_INIT)
        self.hal_write_command(self.LCD_CMD_INIT)
        self.hal_write_command(self.LCD_CMD_INIT)
        self.hal_write_command(self.LCD_CMD_INIT_4BIT)
        self.hal_write_command(self.LCD_FUNCTION | self.LCD_FUNCTION_2LINES)
        self.hal_write_command(self.LCD_ENTRY_MODE | self.LCD_ENTRY_INC)
        self.hal_write_command(self.LCD_CMD_DISPLAY_CONTROL | self.display_control)
        self.hal_write_command(self.LCD_CLR)

    def clear(self):
        self.hal_write_command(self.LCD_CLR)
        self.hal_sleep_us(2000)

    def home(self):
        self.hal_write_command(self.LCD_HOME)
        self.hal_sleep_us(2000)

    def set_cursor(self, col, row):
        if row >= self.num_lines:
            row = self.num_lines - 1
        self.cursor_x = col
        self.cursor_y = row
        addr = col + self.LCD_DDRAM + row * 0x40
        self.hal_write_command(addr)

    def putstr(self, string):
        for char in string:
            if char == '\n':
                self.cursor_y += 1
                if self.cursor_y >= self.num_lines:
                    self.cursor_y = 0
                self.set_cursor(0, self.cursor_y)
            else:
                self.hal_write_data(ord(char))
                self.cursor_x += 1
                if self.cursor_x >= self.num_columns:
                    self.cursor_x = 0
                    self.cursor_y += 1
                    if self.cursor_y >= self.num_lines:
                        self.cursor_y = 0
                    self.set_cursor(self.cursor_x, self.cursor_y)

    def move_to(self, col, row):
        self.set_cursor(col, row)

    def display_on(self, enable):
        if enable:
            self.display_control |= self.LCD_ON_DISPLAY
        else:
            self.display_control &= ~self.LCD_ON_DISPLAY
        self.hal_write_command(self.LCD_CMD_DISPLAY_CONTROL | self.display_control)

    def hal_write_command(self, cmd):
        raise NotImplementedError

    def hal_write_data(self, data):
        raise NotImplementedError

    def hal_sleep_us(self, usecs):
        time.sleep(usecs / 1000000.0)
