# import RPi.GPIO as GPIO
import time
import sys, tty, termios, os
import RPi.GPIO as io

import pygame
from pygame.locals import *



io.setmode(io.BCM)

# Constant values
# PWM_MAX                 = 100

# Disable warning from GPIO
io.setwarnings(False)

# Here we configure the GPIO settings for the left and right motors spinning direction. 
# It defines the four GPIO pins used as input on the L298 H-Bridge to set the motor mode (forward, reverse and stopp).

#Steering Motor
leftmotor_in1_pin = 27
leftmotor_in2_pin = 22
io.setup(leftmotor_in1_pin, io.OUT)
io.setup(leftmotor_in2_pin, io.OUT)

#Foward/Backward Motor
rightmotor_in1_pin = 24
rightmotor_in2_pin = 25
io.setup(rightmotor_in1_pin, io.OUT)
io.setup(rightmotor_in2_pin, io.OUT)

io.output(leftmotor_in1_pin, False)
io.output(leftmotor_in2_pin, False)
io.output(rightmotor_in1_pin, False)
io.output(rightmotor_in2_pin, False)

# Here we configure the GPIO settings for the left and right motors spinning speed. 
# It defines the two GPIO pins used as input on the L298 H-Bridge to set the motor speed with a PWM signal.

# leftmotorpwm_pin = 4
# rightmotorpwm_pin = 17

# io.setup(leftmotorpwm_pin, io.OUT)
# io.setup(rightmotorpwm_pin, io.OUT)

# leftmotorpwm = io.PWM(leftmotorpwm_pin,100)
# rightmotorpwm = io.PWM(rightmotorpwm_pin,100)

# leftmotorpwm.start(0)
# leftmotorpwm.ChangeDutyCycle(0)

# rightmotorpwm.start(0)
# rightmotorpwm.ChangeDutyCycle(0)


def setMotorMode(motor, mode):

# setMotorMode()

# Sets the mode for the L298 H-Bridge which motor is in which mode.

# This is a short explanation for a better understanding:
# motor     -> which motor is selected left motor or right motor
# mode      -> mode explains what action should be performed by the H-Bridge

# setMotorMode(leftmotor, reverse)  -> The left motor is called by a function and set into reverse mode
# setMotorMode(rightmotor, stopp)   -> The right motor is called by a function and set into stopp mode

    if motor == "steermotor":
        if mode == "left":
            io.output(leftmotor_in1_pin, True)
            io.output(leftmotor_in2_pin, False)
        elif  mode == "right":
            io.output(leftmotor_in1_pin, False)
            io.output(leftmotor_in2_pin, True)
        else:
            io.output(leftmotor_in1_pin, False)
            io.output(leftmotor_in2_pin, False)
            
    elif motor == "powermotor":
        if mode == "reverse":
            io.output(rightmotor_in1_pin, True)
            io.output(rightmotor_in2_pin, False)     
        elif  mode == "forward":
            io.output(rightmotor_in1_pin, False)
            io.output(rightmotor_in2_pin, True)        
        else:
            io.output(rightmotor_in1_pin, False)
            io.output(rightmotor_in2_pin, False)
    else:
        io.output(leftmotor_in1_pin, False)
        io.output(leftmotor_in2_pin, False)
        io.output(rightmotor_in1_pin, False)
        io.output(rightmotor_in2_pin, False)



def setMotorSteer(power):

# SetMotorLeft(power)

# Sets the drive level for the left motor, from +1 (max) to -1 (min).

# This is a short explanation for a better understanding:
# SetMotorLeft(0)     -> left motor is stopped
# SetMotorLeft(0.75)  -> left motor moving forward at 75% power
# SetMotorLeft(-0.5)  -> left motor moving reverse at 50% power
# SetMotorLeft(1)     -> left motor moving forward at 100% power
    if power < 0:
        # Reverse mode for the left motor
        setMotorMode("steermotor", "left")
        # pwm = -int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    elif power > 0:
        # Forward mode for the left motor
        setMotorMode("steermotor", "right")
        # pwm = int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    else:
        # Stopp mode for the left motor
        setMotorMode("steermotor", "stop")
        # pwm = 0
#   print "SetMotorLeft", pwm
    # leftmotorpwm.ChangeDutyCycle(pwm)

def setMotorPower(power):

# SetMotorRight(power)

# Sets the drive level for the right motor, from +1 (max) to -1 (min).

# This is a short explanation for a better understanding:
# SetMotorRight(0)     -> right motor is stopped
# SetMotorRight(0.75)  -> right motor moving forward at 75% power
# SetMotorRight(-0.5)  -> right motor moving reverse at 50% power
# SetMotorRight(1)     -> right motor moving forward at 100% power

    if power < 0:
        # Reverse mode for the right motor
        setMotorMode("powermotor", "reverse")
        # pwm = -int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    elif power > 0:
        # Forward mode for the right motor
        setMotorMode("powermotor", "forward")
        # pwm = int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    else:
        # Stopp mode for the right motor
        setMotorMode("powermotor", "stop")
        # pwm = 0
#   print "SetMotorRight", pwm
    # rightmotorpwm.ChangeDutyCycle(pwm)


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
def printscreen():
    # Print the motor speed just for interest
    os.system('clear')
    print("w/s: direction")
    print("a/d: steering")
    print("q: stops the motors")
    print("x: exit")
    print("========== Speed Control ==========")
    print "power motor:  ", powermotor
    print "steer motor: ", steermotor



powermotor = 0
steermotor = 0
print("w/s: direction")
print("a/d: steering")
print("q: stops the motors")
print("p: print motor speed (L/R)")
print("x: exit")

while True:
    # Keyboard character retrieval method. This method will save
    # the pressed key into the variable char
    char = getch()
    # The car will drive forward when the "w" key is pressed
    if(char == "w"):
        # synchronize after a turning the motor speed
        # if speedleft > speedright:
            # speedleft = speedright
        # if speedright > speedleft:
            # speedright = speedleft
        # accelerate the RaPi car
        powermotor = min(1, powermotor+1)
        setMotorPower(powermotor)
        setMotorSteer(steermotor)
        printscreen()

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
        # synchronize after a turning the motor speed
        # if speedleft > speedright:
            # speedleft = speedright
        # if speedright > speedleft:
            # speedright = speedleft
        # slow down the RaPi car
        powermotor = max(-1, powermotor-1)
        setMotorPower(powermotor)
        setMotorSteer(steermotor)
        printscreen()

    # Stop the motors
    if(char == "q"):
        powermotor = 0
        steermotor = 0
        setMotorPower(powermotor)
        setMotorSteer(steermotor)
        printscreen()

    # The "d" key will toggle the steering right
    if(char == "d"):        
        #if speedright > speedleft:
        steermotor = min(1, steermotor+1)
        setMotorPower(powermotor)
        setMotorSteer(steermotor)
        printscreen()
        
    # The "a" key will toggle the steering left
    if(char == "a"):
        #if speedleft > speedright:
        steermotor = max(-1, steermotor-1)
        setMotorPower(powermotor)
        setMotorSteer(steermotor)
        printscreen()
        
    # The "x" key will break the loop and exit the program
    if(char == "x"):
        powermotor = 0
        steermotor = 0
        setMotorPower(powermotor)
        setMotorSteer(steermotor)
        exit()
        print("Program Ended")
        break
    
    # The keyboard character variable char has to be set blank. We need
    # to set it blank to save the next key pressed by the user
    char = ""
# End
# GPIO.setmode(GPIO.BCM)
# # GPIO.setmode(GPIO.BOARD)
# GPIO.setup(27,GPIO.OUT)   #Left motor input A 13
# GPIO.setup(22,GPIO.OUT)   #Left motor input B 15
# GPIO.setup(24,GPIO.OUT)  #Right motor input A 18
# GPIO.setup(25,GPIO.OUT)  #Right motor input B 22
# GPIO.setwarnings(False)

# while True:
#     print "Rotating both motors in clockwise direction"
#     GPIO.output(27,1)
#     GPIO.output(22,0)
#     GPIO.output(24,1)
#     GPIO.output(25,0)
#     time.sleep(1)     #One second delay

#     print "Rotating both motors in anticlockwise direction"
#     GPIO.output(27, 0)
#     GPIO.output(22,1)
#     GPIO.output(24,0)
#     GPIO.output(25,1)
#     time.sleep(1)     
