# PWM - by modulating the duty cycle (on-off cycle) we can fade an LED 
from machine import Pin, PWM 
from time import sleep 

# Setting up the PWM pin 

led = Pin(20)
pwm_led = PWM(led)
duty_step= 129 

# Setting PWM frequency 
frequency = 50
pwm_led.freq(frequency)

try:
    while True:
        for duty_cycle in range(0,65536,duty_step):
            pwm_led.duty_u16(duty_cycle)
            sleep(0.005)

        for duty_cycle in range(65536,0,-duty_step):
            pwm_led.duty_u16(duty_cycle)
            sleep(0.005)  

except KeyboardInterrupt :
    print("Inturrupted") 
    pwm_led.duty_u16(0)   
    print(pwm_led)   
    pwm_led.deinit()   







