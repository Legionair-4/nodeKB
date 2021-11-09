#!/usr/bin/env python

import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


reader = SimpleMFRC522()

try:
	id, text = reader.read()
	cleanText = text.lstrip()
	cleanText = text.rstrip()

	#correct_payload = {'username': cleanText, 'password': id}
	correct_payload = {'username': 't', 'password': 'p'}

	print(correct_payload)
finally:
	GPIO.cleanup()
