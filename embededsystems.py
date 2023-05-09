# Line follower
# 	Version 1.0.2 Mar 5 2023
# For Maker Pi RP2040 running CircuitPython

# MIT license

# Copyright (c) 2023:
# 	Paschalis Ilias
#		ipaschalis2002@gmail.com
# 	Ralousis Anastasios
# 	Giarmantzis Ephstratios


import board
import digitalio
import simpleio
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

# initialize onboard gpio leds
LED_PINS = [board.GP0, 
            board.GP1,
            board.GP2,
            board.GP3,
            board.GP5,
            board.GP7,
            board.GP16,
            board.GP17,
            board.GP26,
            board.GP27,
            board.GP28]

LEDS = []

for pin in LED_PINS:
    # Set pins as digital output
    digout = digitalio.DigitalInOut(pin)
    digout.direction = digitalio.Direction.OUTPUT
    LEDS.append(digout)


# LED εφε
def ledscan(led_status, counter):
    if counter == 2:
        LEDS.reverse()
    for i in range(len(LEDS)):
        LEDS[i].value = led_status
        time.sleep(0.01)
    counter += 1
    if counter == 4:
        counter = 0
        LEDS.reverse()
    return not led_status, counter

# Αλλάζει την ταχύτητα των κινητήρων
# Δέχεται από -1 έως 1, πχ 0.5
def moveM(LThro, RThro):
    motorL.throttle = -LThro
    motorR.throttle = RThro

def mForward():
    moveM(0.30, 0.30)
    
def mBack():
    moveM(-0.25, -0.25)
      
def mBreak():
    moveM(0, 0)
    
def turnRight():
    mBack()
    time.sleep(0.15)
    moveM(0, 0.20)
    time.sleep(0.2)
    mBreak()
    time.sleep(0.2)
    
def turnLeft():
    mBack()
    time.sleep(0.15)
    moveM(0.20, 0)
    time.sleep(0.2)
    mBreak()
    time.sleep(0.2)

led_status = False
counter = 0

if __name__ == "__main__":
    mBreak()
    time.sleep(1)

    while True:
        # Εφε
        led_status, counter = ledscan(led_status, counter)
        
        # Παύση για πιο ομαλή λειτουργιά
        # time.sleep(0.1) Η παύση γίνεται πλέον από τα leds
        
        # Διάβασμα αισθητήρων 
        r_ir = right_ir.value
        l_ir = left_ir.value
        
        if not r_ir and not l_ir: # αν δεν βλέπει την γραμμή ξεκινάει
            mForward()
            time.sleep(0.1)
            mBreak()
            
        elif r_ir and l_ir: # αν βλέπει την γραμμή και από τους δυο αισθητήρες κάνει πίσω και σταματάει   
            mBack()
            time.sleep(0.2)
            mBreak()
            time.sleep(0.5)
        elif not r_ir and l_ir: # αν βλέπει την γραμμή από έναν αισθητήρα γυρνάει  
            turnRight()
        elif r_ir and not l_ir:
            turnLeft()
        else:
            mBreak()
