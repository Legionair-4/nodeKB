#!/usr/bin/env python
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

#This registers a new customer

GPIO.setwarnings(False)

reader = SimpleMFRC522()
camera = PiCamera()

endpoint = 'http://81e72d30b7c2.ngrok.io/register'

async def Write():
    try:
        text = "WallWalkers"
        reader.write(text)
        # print("Now place your tag to write")
        id, text = reader.read()

        cleanText = text.lstrip().rstrip()

        payload = {'cardID': id}
        print(payload)
        
        r = requests.post(endpoint, data=payload)
        print(r.text)

    finally:
        GPIO.cleanup()

#Write() #uncomment for testing
