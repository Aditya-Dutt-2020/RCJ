import RPi.GPIO as GPIO
import time

def initButton():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def getButton():
    input_state = GPIO.input(18)
    return not input_state

# Example
'''
import buttonStopper as bs
bs.initButton()
if bs.getButton():
    print("BUTTON PRESSED YAY")
'''
    
