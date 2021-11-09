#!/usr/bin/env python

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

reader = SimpleMFRC522()
camera = PiCamera()

test_Image_URL = 'https://wall-walkers.herokuapp.com/uploadImage_V2'


try:
    text = "WallWalkers-unit 10,6 Jones Rd,Capalaba,4157"
    print("Now place your tag to take picture")
    reader.write(text)

    camera.start_preview()
    camera.rotation = 180
    #sleep(5)
    camera.capture('/home/pi/Desktop/%s.jpg' % id)
    camera.stop_preview() 
    files = {'image':open('/home/pi/Desktop/%s.jpg' % id, 'rb')}

    r2 = requests.post(test_Image_URL, files=files)

    print(r2)
finally:
    GPIO.cleanup()
