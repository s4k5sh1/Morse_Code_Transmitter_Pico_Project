import machine
import time
from lcd_api import LcdApi

class I2cLcd(LcdApi):
    MASK_RS = 0x01
    MASK_RW = 0x02
    MASK_E = 0x04
    SHIFT_BACKLIGHT = 3
    SHIFT_DATA = 4

    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.backlight = 1
        time.sleep(0.02)  # Wait for LCD to power up
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x03)
        self.hal_write_init_nibble(0x02)
        super().__init__(num_lines, num_columns)
        self.display_on(True)  # Ensure display is turned on
        self.clear()
        self.hal_backlight_on()

    def hal_backlight_on(self, backlight=1):
        self.backlight = backlight
        self.hal_write_command(0)

    def hal_write_init_nibble(self, nibble):
        self.hal_write_byte(nibble << self.SHIFT_DATA)
        time.sleep(0.005)

    def hal_write_command(self, cmd):
        self.hal_write_byte((cmd & 0xF0) | self.MASK_RS)
        self.hal_write_byte((cmd << self.SHIFT_DATA) & 0xF0)
        if cmd <= 3:
            time.sleep(0.005)

    def hal_write_data(self, data):
        self.hal_write_byte(self.MASK_RS | (data & 0xF0))
        self.hal_write_byte(self.MASK_RS | ((data << self.SHIFT_DATA) & 0xF0))

    def hal_write_byte(self, data):
        data |= self.backlight << self.SHIFT_BACKLIGHT
        self.i2c.writeto(self.i2c_addr, bytes([data | self.MASK_E]))
        time.sleep(0.001)
        self.i2c.writeto(self.i2c_addr, bytes([data & ~self.MASK_E]))
