#!/usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

#This checks a customer is a current member and checks them in

GPIO.setwarnings(False)
reader = SimpleMFRC522()

endpoint = 'http://8873b2e55670.ngrok.io/auth'

sleepTimer = 1

async def Check():
    try:
        #Read the RFID card
        id, text = reader.read()
        #Clean any text found
        cleanText = text.lstrip().rstrip()
        #create the payload for the server
        payload = {'cardID': id}
        #Send the payload to the server for verification
        r = requests.post(endpoint, data=payload)
        #print a response code - 202 Accepted
        print(r.text)
        #Sleep so this is not immediately called again
        sleep(sleepTimer)

    finally:
        print('Done')
        #GPIO.cleanup()

#Write() #uncomment for testing
