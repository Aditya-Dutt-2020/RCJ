#first wire goes into pin 11
#second wire goes into ground

import RPi.GPIO as GPIO
import time

def initPin():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getPin():
    input_state = GPIO.input(11)
    return not input_state

# Example
initPin()
while True:
    if(getPin()):
        print("silver detected")

