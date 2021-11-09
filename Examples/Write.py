#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()
camera = PiCamera()

try:
	text = input('New Data:')
	print("Now place your tag to write")
	camera.start_preview()
	reader.write(text)
	sleep(5)
	camera.stop_preview() 
	print("Written")
finally:
	GPIO.cleanup()
