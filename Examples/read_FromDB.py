#!/usr/bin/env python

# import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

test_Object_URL = 'http://eea33e2fed34.ngrok.io/auth'

try:
    id, text = reader.read()
    cleanText = text.lstrip()
    cleanText = text.rstrip()

    correct_payload = {'username': cleanText, 'password': id}

    r = requests.post(test_Object_URL, data = correct_payload)

    print(r.text)
finally:
	GPIO.cleanup()
