import machine
import utime
from pico_i2c_lcd import I2cLcd

# Morse code dictionary

morse_code_dictionary = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----',
    ' ': '/'
}

# Blue LED on GP16 - dot

led_blue = machine.Pin(16, machine.Pin.OUT)

# Red LED on GP28 - dash

led_red = machine.Pin(27, machine.Pin.OUT)

# Setting uo LCD 

I2C_ADDR = 0x3f # I2C Address
I2C_SDA_PIN = 20
I2C_SCL_PIN = 21

i2c = machine.I2C(0,scl=machine.Pin(I2C_SCL_PIN),sda= machine.Pin(I2C_SDA_PIN),freq=400000)
lcd = I2cLcd(i2c,I2C_ADDR,2,16)



#Timing for morse code dot and dash 

dot_time = 0.3  # Time between dots
dash_time = 0.1# Time between dash
dot_dash_gap_time = 0.5 # Time between characters
characters_gap = 0.6 # Time between characters in a word 
word_gap = 1.0 # Time between words 


# Functions to transmit into morse code 


def dot():
    led_blue.high()
    utime.sleep(dot_time)
    led_blue.low()
    utime.sleep(dot_dash_gap_time)

def dash():
    led_red.high()
    utime.sleep(dash_time)   
    led_red.low()
    utime.sleep(dot_dash_gap_time)

def morse_transmit(symbol):
    if symbol == ".":
        dot()
    if symbol == "_":
        dash() 

def text_to_morse(text):
    lcd.clear()
    lcd.putstr("Transmitting:")
    lcd.move_to(0, 1)
    lcd.putstr(text)
    for char in text.upper():
        if char in morse_code_dictionary:
            code = morse_code_dictionary[char]
            for symbol in code:
                morse_transmit(symbol)
            utime.sleep(characters_gap)  # Pause between letters
        elif char == ' ':
            utime.sleep(word_gap)  # Pause between words

# Main transmit loop
            
while True:
    text = input("Enter text to transmit: ")
    text_to_morse(text)
    print("Transmission complete.\n")
    lcd.clear()
    lcd.putstr("Transmission Done")
    utime.sleep(2)  # Show "Transmission Done" for 2 seconds           


