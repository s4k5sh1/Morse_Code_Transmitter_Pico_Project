from machine import Pin 
from time import sleep 

# Digital Inputs 

push_button = Pin(21, Pin.IN,Pin.PULL_DOWN) #Creates a Pin object called push_button 


# Digital Outputs

blue_led = Pin(20, Pin.OUT)

while True:
    blue_led.value(push_button())
    sleep(0.1)
    print(push_button.value())



 