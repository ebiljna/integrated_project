#SubSytem 4 H19
#Version: 3
#Last Edited: 12/05

from pymata4 import pymata4
import time
import utils
import config
import output
from config import (trig,
    tl1Red,
    tl1Yellow,
    tl1Green,
    tl3Red,
    tl3Green,
    pa1,
    wl1)

tolerance = 0.10
                

global sequenceTl3Trigger

ss4Trigger = False

def set_tl(tlNumber, redPin, greenPin, yellowPin=None, colour="reset"):
    
    #set the state of this light to the colour
    utils.state[f"tl{tlNumber}"]["colour"] = colour


    if colour == "red":
        output.write(redPin, 1)
        output.write(greenPin, 0)
        if yellowPin is not None:
            output.write(yellowPin, 0)
        
        

    elif colour == "yellow":
        if yellowPin is None:
            print(f"Warning: TL{tlNumber} has no yellow light")
            return
        output.write(redPin, 0)
        output.write(greenPin, 0)
        output.write(yellowPin, 1)
        
    elif colour == "green":
        output.write(greenPin, 1)
        output.write(redPin, 0)
        if yellowPin is not None:
            output.write(yellowPin, 0)
            

    elif colour == "reset":
        output.write(greenPin, 0)
        output.write(redPin, 0)
        if yellowPin is not None:
            output.write(yellowPin, 0)
            
def set_wl(wlNumber, pin1, pin2, mode="reset"):
    
    #set the state of this light to the colour
    config.state[f"wl{wlNumber}"]["mode"] = mode

    if mode == "on":
        output.write(pin1, 1)
        output.write(pin2, 1)

    elif mode == "off":
        output.write(pin1, 0)
        output.write(pin2, 0)
        
    elif mode == "reset":
        output.write(pin1, 0)
        output.write(pin2, 0)
        


def update():

    us1 = utils.poll_us(trig, 1)
    us2 = utils.poll_us(trig, 2)
    us3 = utils.poll_us(trig, 3)
    us4 = utils.poll_us(trig, 4)
    us5 = utils.poll_us(trig, 5)

    overheightDetected = (
        abs(us3[1] - us4[1]) <= tolerance
        and us3[0]
    )

    # Activate override mode
    if overheightDetected:
        config.state["ss4"]["active"] = True

    # Detect vehicle exiting
    if config.state["ss4"]["active"] and us5[0]:
        config.state["ss4"]["vehicleExited"] = True

    # Check whether ANY sensors still detect object
    sensorsStillDetecting = (
        us1[0]
        or us2[0]
        or us3[0]
        or us4[0]
        or us5[0]
    )

    # Reset only after exit AND all clear
    if (
        config.state["ss4"]["vehicleExited"]
        and not sensorsStillDetecting
    ):

        config.state["ss4"]["active"] = False
        config.state["ss4"]["vehicleExited"] = False


def apply_outputs():

    if config.state["ss4"]["active"]:

        # Stop traffic
        set_tl(3, tl3Red, tl3Green, None, "red")

        set_tl(1, tl1Red, tl1Green, tl1Yellow, "red")

        # Enable warning lights
        set_wl(1, wl1, wl1, "on")

        # Enable alarm
        output.write(pa1, 1)

    else:

        # Resume traffic
        set_tl(3, tl3Red, tl3Green, None, "green")

        set_tl(1, tl1Red, tl1Green, tl1Yellow, "green")

        # Disable warning lights
        set_wl(1, wl1, wl1, "off")

        # Disable alarm
        output.write(pa1, 0)

