# Morse Code LED Transmitter

This project converts text input into Morse code and transmits it using a Raspberry Pi Pico with LEDs. The project also displays the text being transmitted on an LCD.

## Components
- Raspberry Pi Pico
- LEDs (Blue and Red)
- 16x2 I2C LCD Display
- Resistors (220Ω)
- Breadboard and Jumper Wires

## Setup
- Connect the blue LED to GPIO 15.
- Connect the red LED to GPIO 28.
- Connect the LCD to the Pico using GP20 (SDA) and GP21 (SCL).
- Power the Raspberry Pi Pico and upload the code using Thonny or VSCode.

## How It Works
- The script converts input text into Morse code.
- Blue LED flashes for dots, and red LED flashes for dashes.
- The LCD displays the word being transmitted.

## Usage
- Enter text via the serial monitor in VSCode or Thonny.
- The LEDs will blink the corresponding Morse code, and the LCD will show the text.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
