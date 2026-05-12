# Subsystem 1 Code
# Created By: Shreeneel Tarale
# Created Date: 14/04/2026
# Version: v0.1

import time
from pymata4 import pymata4
import utils
import config
import output
from config import (trig,
    tl1Red,
    tl1Yellow,
    tl1Green,
    tl2Red,
    tl2Yellow,
    tl2Green)


global sequenceTl1Trigger, sequenceTl2Trigger, sequencePa1Trigger

sequenceTl1Trigger = False
sequenceTl2Trigger = False  
sequencePa1Trigger = False

redTimerTl1 = yellowTimerTl1 = redTimerTl2 = yellowTimerTl2 = 0.0


def set_tl(tlNumber, redPin, yellowPin, greenPin, colour="reset"):
    
    #set the state of this light to the colour
    config.state[f"tl{tlNumber}"]["colour"] = colour
    global redTimerTl1, yellowTimerTl1, redTimerTl2, yellowTimerTl2



    if colour == "red":

        if tlNumber == 1:
            redTimerTl1 = time.time()
        elif tlNumber == 2:
            redTimerTl2 = time.time()

        output.write(redPin, 1)
        output.write(yellowPin, 0)
        output.write(greenPin, 0)
        
    elif colour == "yellow":

        if tlNumber == 1:
            yellowTimerTl1 = time.time()
        elif tlNumber == 2:
            yellowTimerTl2 = time.time()

        output.write(redPin, 0)
        output.write(yellowPin, 1)
        output.write(greenPin, 0)

    elif colour == "green":

        output.write(redPin, 0)
        output.write(yellowPin, 0)
        output.write(greenPin, 1)

    elif colour == "reset":

        output.write(redPin, 0)
        output.write(yellowPin, 0)
        output.write(greenPin, 0)


def sequence_tl1(start):

    global sequenceTl1Trigger
    now = start

    if config.state["tl1"]["colour"] == "green":
        set_tl(1, tl1Red, tl1Yellow, tl1Green, "yellow")

    elif config.state["tl1"]["colour"] == "yellow" and (now-yellowTimerTl1 >= 1):
        set_tl(1, tl1Red, tl1Yellow, tl1Green, "red")
    
    elif config.state["tl1"]["colour"] == "red" and (now-redTimerTl1 >= 30):
        set_tl(1, tl1Red, tl1Yellow, tl1Green, "green")
        sequenceTl1Trigger = False


def sequence_tl2(start):

    global sequenceTl2Trigger
    now = start
    
    if config.state["tl2"]["colour"] == "green":
        set_tl(2, tl2Red, tl2Yellow, tl2Green, "yellow")

    elif config.state["tl2"]["colour"] == "yellow" and (now-yellowTimerTl2 >= 1):
        set_tl(2, tl2Red, tl2Yellow, tl2Green, "red")
    
    elif config.state["tl2"]["colour"] == "red" and (now-redTimerTl2 >= 3):
        set_tl(2, tl2Red, tl2Yellow, tl2Green, "green")
        sequenceTl2Trigger = False

def sequence_pa1(start):
    global sequencePa1Trigger

    if not config.state["pa1"]["sound"]:
        config.state["pa1"]["sound"] = True
    elif config.state["pa1"]["sound"] and not ((config.state["tl1"]["colour"] == "red") or (config.state["tl2"]["colour"] == "red")):
        config.state["pa1"]["sound"] = False

        sequencePa1Trigger = False



def update():
    global sequenceTl1Trigger, sequenceTl2Trigger, sequencePa1Trigger

    if config.state["ss4"]["active"]:
        return

    us1Result = utils.poll_us(trig, 1)
    us2Result = utils.poll_us(trig, 2)

    if us1Result[0] and not config.state["us1"]["triggered"]:

        print(f"[ALERT] Overheight Vehicle Detected (US1), Height: {us1Result[1]:.2f}m, Time: {us1Result[2]}")

        config.state["us1"]["triggered"] = True 

        sequenceTl1Trigger = True
    
    if us2Result[0]:
        if config.state["us1"]["timeOfLast"] != None:
            if 16 <= (time.time() - config.state["us1"]["timeOfLast"]) <= 22.5:
                sequenceTl2Trigger = True
                sequencePa1Trigger = True
        else:
            sequencePa1Trigger = True
            sequenceTl2Trigger = True
            sequenceTl1Trigger = True

def apply_outputs():

    now = time.time()

    if sequenceTl1Trigger:
        sequence_tl1(now)

    if sequenceTl2Trigger:
        sequence_tl2(now)

    if sequencePa1Trigger:
        sequence_pa1(now)



