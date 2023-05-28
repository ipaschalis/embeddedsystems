# Line follower
# 	Version 1.0.4 Mar 28 2023
# For Maker Pi RP2040 running CircuitPython

# MIT license

# Copyright (c) 2023:
# 	Paschalis Ilias
#		ipaschalis2002@gmail.com
# 	Ralousis Anastasios
# 	Giarmantzis Ephstratios


import board
import digitalio
import time
import pwmio
from adafruit_motor import motor

# initialize DC motors
freq = 10000

mL1 = pwmio.PWMOut(board.GP8, frequency=freq)
mL2 = pwmio.PWMOut(board.GP9, frequency=freq)
motorL = motor.DCMotor(mL1, mL2)

mR1 = pwmio.PWMOut(board.GP10, frequency=freq)
mR2 = pwmio.PWMOut(board.GP11, frequency=freq)
motorR = motor.DCMotor(mR1, mR2)

# initialize IR sensors
right_ir = digitalio.DigitalInOut(board.GP4)
left_ir = digitalio.DigitalInOut(board.GP6)


# Αλλάζει την ταχύτητα των κινητήρων
# Δέχεται από -1 έως 1, πχ 0.5
def move_m(left_throttle, right_throttle):
    motorL.throttle = -left_throttle
    motorR.throttle = right_throttle


def move_forward():
    move_m(0.30, 0.30)


def move_back():
    move_m(-0.25, -0.25)


def move_stop():
    move_m(0, 0)


def turn_right():
    move_back()
    time.sleep(0.25)
    move_m(0, 0.30)
    time.sleep(0.5)
    move_stop()
    time.sleep(0.1)


def turn_left():
    move_back()
    time.sleep(0.25)
    move_m(0.30, 0)
    time.sleep(0.5)
    move_stop()
    time.sleep(0.1)


if __name__ == "__main__":
    move_stop()

    while True:
        # Παύση για πιο ομαλή λειτουργιά
        time.sleep(0.005)

        # Διάβασμα αισθητήρων 
        r_ir = right_ir.value
        l_ir = left_ir.value

        if not r_ir and not l_ir:  # αν δεν βλέπει την γραμμή ξεκινάει
            move_forward()
        elif r_ir and l_ir:  # αν βλέπει την γραμμή και από τους δυο αισθητήρες κάνει πίσω και σταματάει
            move_stop()
        elif not r_ir and l_ir:  # αν βλέπει την γραμμή από έναν αισθητήρα γυρνάει
            turn_right()
        elif r_ir and not l_ir:
            turn_left()
        else:
            move_stop()
