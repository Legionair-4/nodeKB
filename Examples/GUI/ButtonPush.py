#!/usr/bin/env python
from signal import pause
from gpiozero import Button
#import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

# GPIO.setwarnings(False)
reader = SimpleMFRC522()
button = Button(26)

test_Object_URL = 'http://7854e18b89ad.ngrok.io/register'

def message():
    try:
        text = input('New Data:')
        print("Now place your tag to write")
        reader.write(text)

        id, text = reader.read()
        cleanText = text.lstrip().rstrip()
        correct_payload = {'username': cleanText, 'password': id}
        
        r = requests.post(test_Object_URL, data=correct_payload)

        print(r.text)
    finally:
        # GPIO.cleanup()
        print("Button pushed")


