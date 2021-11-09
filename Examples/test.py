#!/usr/bin/env python
import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

testURL = 'http://8f4961c4f76f.ngrok.io/test'
reader = SimpleMFRC522()

try:
	id, text = reader.read()
	cleanText = text.lstrip().rstrip()

	correct_payload = {'username': cleanText, 'password': id}
	r=requests.post(testURL, data=correct_payload)
	print(r.text)
	print(correct_payload)
	time.sleep(2)
finally:
    GPIO.cleanup()