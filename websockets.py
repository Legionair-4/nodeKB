#!/usr/bin/env python
import asyncio
import sys
from time import sleep
from gpiozero import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import socketio
import os

GPIO.setwarnings(False)
reader = SimpleMFRC522()
sio = socketio.Client()

endpoint_Socket = 'ws://wall-walkers.herokuapp.com'

@sio.on('event')
async def message(data):
    print('I got the Data Too: ' + data)

async def Read():
    print("\t---------Wall Walkers RFID Reading-----------")
    await asyncio.sleep(1)
    id, text = reader.read()\

    if not id:
        await asyncio.sleep(2)
        pass
    else:
        print(id)
        sio.emit('AuthClimber-Scan-Voting', id)
        # sio.wait()
        await asyncio.sleep(1)
        os.system('clear')


def main():
    try:
        #Get the main loop
        loop = asyncio.get_event_loop()
        #Main looping mechanim
        while True:
            #Create the read task
            Read_Task = loop.create_task(Read())
            #Run the rad task and wait for it to complete
            loop.run_until_complete(Read_Task)
    except KeyboardInterrupt: #Make sure there is a way to kill the program if needed
        sys.ext(1) #exists the program on ctrl + C

def ConnectSocket():
    sio.connect(endpoint_Socket)
    

#Start the program
if __name__=="__main__":
    ConnectSocket()
    main()