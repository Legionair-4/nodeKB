#!/usr/bin/env python
from signal import pause
import RPi.GPIO as GPIO
from gpiozero import Button
from mfrc522 import SimpleMFRC522
import requests
import sys

GPIO.setwarnings(False)

#Buttons
button = Button(26)

#Read/Writer
reader = SimpleMFRC522()
#Endpoint
endpoint = 'http://7854e18b89ad.ngrok.io/register'

def message():
    try:
        text = input('New Data:')
        print("Now place your tag to write")
        reader.write(text)

        id, text = reader.read()
        cleanText = text.lstrip().rstrip()
        
        print(id)
        print(text)
        # correct_payload = {'username': cleanText, 'password': id}
        
        # r = requests.post(endpoint, data=correct_payload)

        # print(r.text)
    finally:
        # GPIO.cleanup()
        print("Button pushed")


try:
    button.when_activated = message
    pause()

# except KeyboardInterrupt:
#     GPIO.cleanup()
#     raise

finally:
    pass