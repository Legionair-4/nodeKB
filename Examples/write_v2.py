#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

reader = SimpleMFRC522()
camera = PiCamera()

test_Object_URL = 'http://93b26679e1a3.ngrok.io/test'
test_Image_URL = 'http://93b26679e1a3.ngrok.io/test/image'


try:
    text = input('New Data:')
    print("Now place your tag to write")
    reader.write(text)

    id, text = reader.read()
    cleanText = text.lstrip().rstrip()
    correct_payload = {'username': cleanText, 'password': id}
    
    camera.start_preview()
    camera.rotation = 180
    sleep(5)
    camera.capture('/home/pi/Desktop/%s.jpg' % id)
    camera.stop_preview() 
    files = {'image':open('/home/pi/Desktop/%s.jpg' % id, 'rb')}

    r = requests.post(test_Object_URL, data=correct_payload)
    r2 = requests.post(test_Image_URL, files=files)

    print("Written")
finally:
    GPIO.cleanup()
