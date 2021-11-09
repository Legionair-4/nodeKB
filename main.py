#!/usr/bin/env python
import asyncio
import sys
from time import sleep
from gpiozero import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import socketio

GPIO.setwarnings(False)
keepReading = True
lastID =""
foundID = ""
button = Button(26)
reader = SimpleMFRC522()
sio = socketio.Client()

endpoint_Auth = 'https://wall-walkers.herokuapp.com/auth'
endpoint_Socket = 'ws://wall-walkers.herokuapp.com'
#endpoint_Register = 'http://wall-walkers.herokuapp.com/register'

async def Read():
    """
    Function: Read from the database every 1 second
    if a card has not been scanned then there will be no call to the database
    """
    # while True:
    global lastID
    global foundID

    print('Reading')
    await asyncio.sleep(1)

    #Read the RFID card
    id, text = reader.read()
    #Check if found anything
    if not id:
        await asyncio.sleep(2)
        pass
    else:
        #not empty
        #create the payload for the server
        lastID = id
        foundID = id
        cleanText = text.lstrip().rstrip()
        payload = {'cardID': id}
        print(payload, cleanText)
        #Send the payload to the server for verification
        sio.emit('AuthClimber', id)
        #r = requests.post(endpoint_Auth, data=payload)
        #print a response code - 202 Accepted - 401 UnAuthorized 503 Service Unavailable
        #print(r.status_code, r.text)

async def Write():
    #Print placeholder text to console
    print('Waiting for Write: Hold card close to scanner')
    #Register the global variable
    global keepReading
    #Make sure each card has the wallwalkers address on it
    text = "WallWalkers-unit 10,6 Jones Rd,Capalaba,4157"
    #Write the information to the card
    reader.write(text)
    #Read the card information and get the ID to send to the sever
    id, text = reader.read()
    #Clean the text to ensure it is as small as possible
    #cleanText = text.lstrip().rstrip()
    #Create the server payload to be sent
    payload = {'cardID': id}
    #Tell the program to start reading loop once again
    keepReading = True
    #Emit to server socket
    sio.emit('ClimberRegistrationRecieved', id)
    # #Send the post request to the server using the register endoint and created payload
    # r = requests.post(endpoint_Register, data=payload)
    # #Give correct feedback to the console based on server response
    # if r.status_code==201: #card id does not already exist in the server and was now created correctly
    #     print('Written:', r.text)
    # elif r.status_code==401: #Card ID already exists in the server and account cannot be created
    #     print('Unauthorized, Card ID already exists', r.text)

def BreakReadingLoop():
    #Get the glogal var
    global keepReading
    #Change the global var to idicate false which will start the write process
    keepReading = False

def main():
    #register the global var
    global keepReading
    try:
        #Register the button event
        button.when_activated = BreakReadingLoop
        #Get the main loop
        loop = asyncio.get_event_loop()
        #Main looping mechanim
        while True:
            #Check to see if the program should now write to the server or keep reading
            if keepReading == False:
                #Start the write async task
                Write_Task = loop.create_task(Write())
                #Run the write task and wait for it to complete
                loop.run_until_complete(Write_Task)
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