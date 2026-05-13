#SubSytem 2 H19
#Version: 3
#Last Edited: 12/05

import time
import utils
import config
from config import (
    board,
    pb,
    tl4Red,
    tl4Yellow,
    tl4Green,
    tl5Red,
    tl5Yellow,
    tl5Green,
    plTimer,
    pl1Red,
    pl2Red,
    pl1Green,
    pl2Green
)
import output

cooldown = 30

last_pedestrian_time = 0
last_button_state = 0

pedestrian_request = False
pedestrian_sequence_active = False

pedestrian_stage = 0
pedestrian_timer = 0

traffic_stage = 0
traffic_timer = 0


config.state["tl4"]["colour"] = "green"
config.state["tl5"]["colour"] = "red"

utils.config["pedestrian"] = "solid_red"



def set_tl(tlNumber, redPin, greenPin, yellowPin=None, colour="reset"):

    utils.config[f"tl{tlNumber}"]["colour"] = colour

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

        output.write(redPin, 0)
        output.write(greenPin, 1)

        if yellowPin is not None:
            output.write(yellowPin, 0)

    elif colour == "reset":

        output.write(redPin, 0)
        output.write(greenPin, 0)

        if yellowPin is not None:
            output.write(yellowPin, 0)



def update():

    global last_button_state
    global last_pedestrian_time

    global pedestrian_request
    global pedestrian_sequence_active
    global pedestrian_stage
    global pedestrian_timer

    global traffic_stage
    global traffic_timer

    now = time.time()

    current_button = board.digital_read(pb)[0] == 1

    if current_button and not last_button_state:

        if now - last_pedestrian_time >= cooldown:

            print("BUTTON PRESSED")

            pedestrian_request = True

        else:
            print("COOLDOWN ACTIVE")

    last_button_state = current_button

    if not pedestrian_sequence_active:

        # TL4 green, TL5 red
        if traffic_stage == 0:

            utils.config["tl4"]["colour"] = "green"
            utils.config["tl5"]["colour"] = "red"

            utils.config["pedestrian"] = "solid_red"

            if traffic_timer == 0:
                traffic_timer = now

            if now - traffic_timer >= 20:

                traffic_stage = 1
                traffic_timer = now

        # TL4 yellow
        elif traffic_stage == 1:

            utils.config["tl4"]["colour"] = "yellow"

            if now - traffic_timer >= 3:

                traffic_stage = 2
                traffic_timer = now

        # TL4 red, TL5 green
        elif traffic_stage == 2:

            utils.config["tl4"]["colour"] = "red"
            utils.config["tl5"]["colour"] = "green"

            if now - traffic_timer >= 10:

                traffic_stage = 3
                traffic_timer = now

        # TL5 yellow
        elif traffic_stage == 3:

            utils.config["tl5"]["colour"] = "yellow"

            if now - traffic_timer >= 3:

                traffic_stage = 0
                traffic_timer = now


    #pedestrian sequence

    if pedestrian_request and not pedestrian_sequence_active:

        pedestrian_request = False

        pedestrian_sequence_active = True

        pedestrian_stage = 0
        pedestrian_timer = now


    if pedestrian_sequence_active:

        # If TL4 currently green

        if utils.config["tl4"]["colour"] == "green":

            # TL4 yellow
            if pedestrian_stage == 0:

                utils.config["tl4"]["colour"] = "yellow"
                utils.config["tl5"]["colour"] = "red"

                if now - pedestrian_timer >= 3:

                    pedestrian_stage = 1
                    pedestrian_timer = now

            # TL4 red + pedestrian green
            elif pedestrian_stage == 1:

                utils.config["tl4"]["colour"] = "red"

                utils.config["pedestrian"] = "green"

                if now - pedestrian_timer >= 3:

                    pedestrian_stage = 2
                    pedestrian_timer = now

            # flashing red
            elif pedestrian_stage == 2:

                utils.config["pedestrian"] = "flashing"

                if now - pedestrian_timer >= 2:

                    utils.config["pedestrian"] = "solid_red"

                    pedestrian_sequence_active = False

                    last_pedestrian_time = now

                    traffic_stage = 2
                    traffic_timer = now

        # If TL5 currently green

        elif utils.config["tl5"]["colour"] == "green":

            # TL5 yellow
            if pedestrian_stage == 0:

                utils.config["tl5"]["colour"] = "yellow"
                utils.config["tl4"]["colour"] = "red"

                if now - pedestrian_timer >= 3:

                    pedestrian_stage = 1
                    pedestrian_timer = now

            # TL5 red + pedestrian green
            elif pedestrian_stage == 1:

                utils.config["tl5"]["colour"] = "red"

                utils.config["pedestrian"] = "green"

                if now - pedestrian_timer >= 3:

                    pedestrian_stage = 2
                    pedestrian_timer = now

            # flashing red
            elif pedestrian_stage == 2:

                utils.config["pedestrian"] = "flashing"

                if now - pedestrian_timer >= 2:

                    utils.config["pedestrian"] = "solid_red"

                    pedestrian_sequence_active = False

                    last_pedestrian_time = now

                    traffic_stage = 0
                    traffic_timer = now

def apply_outputs():

    set_tl(
        4,
        tl4Red,
        tl4Green,
        yellowPin=tl4Yellow,
        colour=utils.config["tl4"]["colour"]
    )

    set_tl(
        5,
        tl5Red,
        tl5Green,
        yellowPin=tl5Yellow,
        colour=utils.config["tl5"]["colour"]
    )


    pedestrian_state = utils.config["pedestrian"]

    if pedestrian_state == "solid_red":

        output.write(plTimer, 0)
        output.write(pl2Red, 0)
        output.write(pl1Red, 1)

    elif pedestrian_state == "green":

        output.write(pl1Green, 1)
        output.write(pl2Green, 1)
        output.write(pl2Red, 0)
        output.write(pl1Red, 0)

    elif pedestrian_state == "flashing":

        output.write(plTimer, 0)
        output.write(pl2Red, 1)
        output.write(pl1Red, 0)
