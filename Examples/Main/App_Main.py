#!/usr/bin/env python
import asyncio
import sys
from time import sleep
from gpiozero import Button
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests

GPIO.setwarnings(False)
keepReading = True
lastID =""
foundID = ""
button = Button(26)
reader = SimpleMFRC522()

endpoint_Auth = 'http://c27010c32dbc.ngrok.io/auth'
endpoint_Register = 'http://c27010c32dbc.ngrok.io/register'

#The below is information on event loops for asyncio
#Stack overflow 53998267 - how to reset an asyncio eventloop by a worker

async def Read():
    """
    Function: Read from the database every 1 second
    if a card has not been scanned then there will be no call to the database
    """
    global lastID
    global foundID
    loop = asyncio.get_event_loop()
    while True:
        print('Reading')
        #Read the RFID card
        id, text = reader.read()

        #Check if found anything
        if not id:
            #empty
            pass
        else:
            #not empty
            #create the payload for the server
            lastID = id
            foundID = id
            payload = {'cardID': id}
            print(payload)
            #Send the payload to the server for verification
            r = requests.post(endpoint_Auth, data=payload)
            #print a response code - 202 Accepted
            print(r.text)
            #Sleep so this is not immediately called again
            sleep(1)

        #Read from the data base here
        await asyncio.sleep(1)
        if keepReading == False: # this section might cause error
            loop.stop()
            await asyncio.sleep(2)

async def Write(workerID):
    print(workerID, 'Writing')
    global keepReading
    text = "WallWalkers - unit 10, 6 Jones Rd, Capalaba, 4157"
    reader.write(text)
    id, text = reader.read()
    cleanText = text.lstrip().rstrip()
    payload = {'cardID': id}
    print(payload)
    r = requests.post(endpoint_Register, data=payload)
    keepReading = True
    print(r.text)

    print(workerID, 'Written')
    

def BreakReadingLoop():
    global keepReading
    keepReading = False   
    # Write_Task = asyncio.create_task(Write(1))
    # await Write_Task


def main():
    try:
        global keepReading
        button.when_activated = BreakReadingLoop
        loop = asyncio.get_event_loop()
        loop.create_task(Read())
        workerID = 0
        while True:
            # if keepReading == False:
            workers = []
            workerID += 1
            workers.append(loop.create_task(Write(workerID)))
            loop.run_forever()
            for t in workers:
                t.cancel()
    except KeyboardInterrupt:
        sys.ext(1)


if __name__=="__main__":
    main()



#Below is a working code loop which can be used as backup if you fuck
# up the above code somehow
# !/usr/bin/env python
# import asyncio
# import sys
# from time import sleep
# from gpiozero import Button

# keepReading = True
# lastID =""
# foundID = ""
# button = Button(26)

# #Stack overflow 53998267 - how to reset an asyncio eventloop by a worker

# async def Read():
#     """
#     Function: Read from the database every 1 second
#     if a card has not been scanned then there will be no call to the database
#     """
#     loop = asyncio.get_event_loop()
#     while True:
#         print('Reading', keepReading)
#         #Read from the data base here
#         await asyncio.sleep(1)
#         if keepReading == False: # this section might cause error
#             loop.stop()
#             await asyncio.sleep(2)

# async def Write(workerID):
#     print(workerID, 'Writter')
#     await asyncio.sleep(1)
#     global keepReading
#     keepReading = True
    

# def BreakReadingLoop():
#     global keepReading
#     keepReading = False
#     # print(keepReading)
    

# def main():
#     try:
#         button.when_activated = BreakReadingLoop
#         loop = asyncio.get_event_loop()
#         loop.create_task(Read())
#         workerID = 0
#         sleep(1)
#         while True:
#             workers = []
#             workerID += 1
#             workers.append(loop.create_task(Write(workerID)))
#             loop.run_forever()
#             for t in workers:
#                 t.cancel()
#     except KeyboardInterrupt:
#         sys.ext(1)


# if __name__=="__main__":
#     main()
