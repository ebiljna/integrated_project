import time 
from pymata4 import pymata4

board = pymata4.Pymata4() #circuit.Arduino()

tl1Red=1
tl1Yellow=2
tl1Green=3
tl2Red=4
tl2Yellow=5
tl2Green=6
tl3Red=7
tl3Green=8
tl4Red=9
tl4Yellow=10
tl4Green=11
tl5Red=12
tl5Yellow=13
tl5Green=14
tl6Red=15
tl6Yellow=16
tl6Green=17
wl1=18
pl1Red=19
pl1Green=20
pl2Red=21
pl2Green=22
pa1=23
ss3Timer=24


#Ultrasonic sensors
trig = 10
echo1 = 9
echo2 = 8
echo3 = 7
echo4 = 6
echo5 = 5
pbInput = 4
osInput = 3
#US1
board.set_pin_mode_sonar(trig, echo1)
#US2
board.set_pin_mode_sonar(trig, echo2)
#US3
board.set_pin_mode_sonar(trig, echo3)
#US4
board.set_pin_mode_sonar(trig, echo4)
#US5
board.set_pin_mode_sonar(trig, echo5)

#PB and OS input
board.set_pin_mode_digital_input(pbInput)
board.set_pin_mode_digital_input(osInput)

#shift register
ser=13 
rclk=12
srclk=11
#latchPin
board.set_pin_mode_digital_output(rclk)
#dataPin
board.set_pin_mode_digital_output(ser)
#clockPin
board.set_pin_mode_digital_output(srclk)

startTime = time.time()
    
integration = True

pollingRate = 0.05
sensorMountHeight = 4.5
overheightLimit = 4.0

#no. of shift registers
chain_number = 4

state = {
    #ultrasonic sensors
    "us1": {"detected": False, "timeOfLast": None, "triggered": False},
    "us2": {"detected": False, "timeOfLast": None, "triggered": False},
    "us3": {"detected": False, "timeOfLast": None, "triggered": False},
    "us4": {"detected": False, "timeOfLast": None, "triggered": False},
    "us5": {"detected": False, "timeOfLast": None, "triggered": False},

    #traffic lights
    "tl1": {"colour": "green"},
    "tl2": {"colour": "green"},
    "tl3": {"colour": "green"},
    "tl4": {"colour": "green"},
    "tl5": {"colour": "green"},
    "tl6": {"colour": "green"},
    "tl7": {"colour": "green"},

    
    #buzzer
    "pa1": {"sound": False},
    

}

