#!/usr/bin/env python

import PySimpleGUI as sg
import time
import requests
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import asyncio

sg.theme('BluePurple')
reader = SimpleMFRC522()

test_Object_URL = 'http://7854e18b89ad.ngrok.io/auth'

#check docs.python.org/3/library/asyncio-task.html

async def count():
    while True:
        try:
            id, text = reader.read()
            cleanText = text.lstrip()
            cleanText = text.rstrip()

            correct_payload = {'username': cleanText, 'password': id}

            r = requests.post(test_Object_URL, data = correct_payload)

            print(r.text)
        finally:
            GPIO.cleanup()


async def buttonScan():
    await asyncio.gather(count())


dispatch_dictionary = {'Scan':buttonScan}

layout = [[sg.Text('Tap your card on the scanner to log in.'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='username')],
          [sg.Button('Show'), sg.Button('Scan'), sg.Button('Exit')]]


window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]
        asyncio.run(func_to_call())
    else:
            print('Event {} not in the dispatch dictionary'.format(event))
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

window.close()