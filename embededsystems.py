# Paschalis Ilias
# CircuitPython
# Line follower

import board
import digitalio
import simpleio
import time
import pwmio
from adafruit_motor import servo, motor

# initialize DC motors
freq = 10000

mL1 = pwmio.PWMOut(board.GP8, frequency = freq)
mL2 = pwmio.PWMOut(board.GP9, frequency = freq)
motorL = motor.DCMotor(mL1, mL2)

mR1 = pwmio.PWMOut(board.GP10, frequency = freq)
mR2 = pwmio.PWMOut(board.GP11, frequency = freq)
motorR = motor.DCMotor(mR1, mR2)

# Alazei thn taxitita twn kinitirwn
# Dehete input apo 0 eos 1, px 0.5 . 
def moveM(LThro, RThro):
    motorL.throttle = LThro
    motorR.throttle = -RThro

def mForward():
    moveM(0.5, 0.5)

def mBreak():
    moveM(0, 0)
    
def turnRight():
    moveM(0, 0.25)
    
def turnLeft():
    moveM(0.25, 0)

while True:
    mForward()
    time.sleep(1)
    mBreak()
    time.sleep(0)