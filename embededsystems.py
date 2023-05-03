# Line follower
# 	Version 1.0.0
# For Maker Pi RP2040 running CircuitPython

# MIT license

# Programmers:
# 	Paschalis Ilias
#		ipaschalis2002@gmail.com
# 	Ralousis Anastasios
# 	Giarmantzis Ephstratios


import board
import digitalio
import simpleio
import neopixel
import time
import pwmio
from adafruit_motor import motor

# initialize DC motors
freq = 10000

mL1 = pwmio.PWMOut(board.GP8, frequency = freq)
mL2 = pwmio.PWMOut(board.GP9, frequency = freq)
motorL = motor.DCMotor(mL1, mL2)

mR1 = pwmio.PWMOut(board.GP10, frequency = freq)
mR2 = pwmio.PWMOut(board.GP11, frequency = freq)
motorR = motor.DCMotor(mR1, mR2)

# initialize IR sensors
right_ir = digitalio.DigitalInOut(board.GP4)
left_ir = digitalio.DigitalInOut(board.GP6)

# Αλλάζει την ταχύτητα των κινητήρων
# Δέχεται από -1 έως 1, πχ 0.5
def moveM(LThro, RThro):
    motorL.throttle = -LThro
    motorR.throttle = RThro

def mForward():
    moveM(0.30, 0.30)
    
def mBack():
    moveM(-0.30, -0.30)
    
def mBreak():
    moveM(0, 0)
    
def turnRight():
    moveM(0, 0.25)
    
def turnLeft():
    moveM(0.25, 0)
    
if __name__ == "__main__":
    mBreak()
    time.sleep(1)

    while True:
        time.sleep(0.1)
        r_ir = right_ir.value
        l_ir = left_ir.value
        
        if not r_ir and not l_ir: # αν δεν βλέπει την γραμμή ξεκινάει
            mForward()
        elif r_ir and l_ir: # αν βλέπει την γραμμή και από τους δυο αισθητήρες κάνει πίσω και σταματάει   
            mBack()
            time.sleep(0.2)
            mBreak()
            time.sleep(1)
        elif not r_ir and l_ir: # αν βλέπει την γραμμή από έναν αισθητήρα γυρνάει  
            turnRight()
        elif r_ir and not l_ir:
            turnLeft()
        else:
            mBreak()
