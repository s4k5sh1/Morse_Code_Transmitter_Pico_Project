import machine
import utime
from pico_i2c_lcd import I2cLcd

# Initialize I2C
I2C_SDA_PIN = 20  # GP20 as SDA
I2C_SCL_PIN = 21  # GP21 as SCL

i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)

# Scan I2C bus
devices = i2c.scan()

if devices:
    print("I2C device found at address:", hex(devices[0]))
else:
    print("No I2C device found")
