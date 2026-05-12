
#SubSytem 3 H19
#Version: 10
#Last Edited: 12/05

from pymata4 import pymata4
import time
import utils 
import config
import output
from config import (trig,
    tl6Red, 
    tl6Yellow,
    tl6Green,
    ss3Timer)

config.state["tl6"]["colour"] = "red"
config.state["ss3"]["flash"] = False

ss3Trigger = False

lastDetectionState = False

ss3Active = False
ss3Stage = 0
ss3StageTimer = 0


def update():

    global ss3Trigger
    global lastDetectionState

    global ss3Active
    global ss3Stage
    global ss3StageTimer

    now = time.time()

    # poll US5
    us5Result = utils.poll_us(trig, 5)

    ss3Trigger = us5Result[0]

    if ss3Trigger and not lastDetectionState:

        print("Overheight vehicle detected by US5!")

        ss3Active = True
        ss3Stage = 0
        ss3StageTimer = now

    lastDetectionState = ss3Trigger

    if ss3Active:

  
        # TL6 green for 5 seconds
        if ss3Stage == 0:

            config.state["tl6"]["colour"] = "green"

            if now - ss3StageTimer >= 5:

                # vehicle still present
                if ss3Trigger:

                    print("Overheight vehicle still detected by US5, TL6 flashing green!")

                    ss3Stage = 1
                    ss3StageTimer = now

                # vehicle cleared
                else:

                    print("Vehicle cleared from US5!")

                    ss3Stage = 2
                    ss3StageTimer = now


        # flashing green while vehicle detected
        elif ss3Stage == 1:

            config.state["tl6"]["colour"] = "reset"

            # enable 556 flasher
            config.state["ss3"]["flash"] = True

            # wait until vehicle clears
            if not ss3Trigger:

                print("Overheight vehicle no longer detected by US5!")

                config.state["ss3"]["flash"] = False

                ss3Stage = 2
                ss3StageTimer = now


        # yellow for 3 seconds
        elif ss3Stage == 2:

            config.state["tl6"]["colour"] = "yellow"

            if now - ss3StageTimer >= 3:

                ss3Stage = 3
                ss3StageTimer = now

        # back to red idle
        elif ss3Stage == 3:

            config.state["tl6"]["colour"] = "red"
            config.state["ss3"]["flash"] = False

            ss3Stage = 0
            ss3Active = False



def set_tl(tlNumber, redPin, greenPin, yellowPin=None, colour="reset"):
    
    #set the state of this light to the colour
    config.state[f"tl{tlNumber}"]["colour"] = colour


    if colour == "red":

        output.write(redPin, 1)
        if yellowPin is not None:
            output.write(yellowPin, 0)
        output.write(greenPin, 0)

    elif colour == "yellow":

        if yellowPin is None:
            print(f"Warning: TL{tlNumber} has no yellow light")
            return

        output.write(redPin, 0)
        output.write(yellowPin, 1)
        output.write(greenPin, 0)
        
    elif colour == "green":

        output.write(redPin, 0)
        if yellowPin is not None:
            output.write(yellowPin, 0)
        output.write(greenPin, 1)

    elif colour == "reset":
        output.write(redPin, 0)
        if yellowPin is not None:
            output.write(yellowPin, 0)
        output.write(greenPin, 0)


def apply_outputs():

    global ss3Active
    global ss3Stage
    global ss3StageTimer
    global lastDetectionState

    if config.state["ss4"]["active"]:

        output.write(ss3Timer, 0)

        config.state["tl6"]["colour"] = "red"
        config.state["ss3"]["flash"] = False

        ss3Active = False
        ss3Stage = 0
        ss3StageTimer = 0

        lastDetectionState = False

        return

    set_tl(6, tl6Red, tl6Green, tl6Yellow, colour=config.state["tl6"]["colour"])
    if config.state["ss3"]["flash"]:
        output.write(ss3Timer, 1)
    else:
        output.write(ss3Timer, 0)
    
    
