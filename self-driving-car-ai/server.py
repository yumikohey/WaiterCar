#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import SocketServer
import RPi.GPIO as io

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

# Map of drives to pins
# lDrives = [DRIVE_1, DRIVE_2, DRIVE_3, DRIVE_4]
rightmotorpwm_pin = 4
io.setup(rightmotorpwm_pin, io.OUT)
rightmotorpwm = io.PWM(rightmotorpwm_pin,100)
rightmotorpwm.start(0)
rightmotorpwm.ChangeDutyCycle(0)

def setMotorMode(motor, mode, p):

# setMotorMode()

# Sets the mode for the L298 H-Bridge which motor is in which mode.

# This is a short explanation for a better understanding:
# motor     -> which motor is selected left motor or right motor
# mode      -> mode explains what action should be performed by the H-Bridge

# setMotorMode(leftmotor, reverse)  -> The left motor is called by a function and set into reverse mode
# setMotorMode(rightmotor, stopp)   -> The right motor is called by a function and set into stopp mode
    power = abs(p)*100
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
            rightmotorpwm.ChangeDutyCycle(power)

        elif  mode == "forward":
            io.output(rightmotor_in1_pin, False)
            io.output(rightmotor_in2_pin, True)
            rightmotorpwm.ChangeDutyCycle(power)

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
        setMotorMode("steermotor", "left", power)
        # pwm = -int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    elif power > 0:
        # Forward mode for the left motor
        setMotorMode("steermotor", "right", power)
        # pwm = int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    else:
        # Stopp mode for the left motor
        setMotorMode("steermotor", "stop", power)
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
        setMotorMode("powermotor", "reverse", power)
        # pwm = -int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    elif power > 0:
        # Forward mode for the right motor
        setMotorMode("powermotor", "forward", power)
        # pwm = int(PWM_MAX * power)
        # if pwm > PWM_MAX:
        #     pwm = PWM_MAX
    else:
        # Stopp mode for the right motor
        setMotorMode("powermotor", "stop", power)
        # pwm = 0

# Function to set all drives off
def MotorOff():
    io.output(leftmotor_in1_pin, False)
    io.output(leftmotor_in2_pin, False)
    io.output(rightmotor_in1_pin, False)
    io.output(rightmotor_in2_pin, False)

# Settings for the RemoteKeyBorg server
portListen = 9038                       # What messages to listen for (LEDB on an LCD)

# Class used to handle UDP messages
class PicoBorgHandler(SocketServer.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request          # Read who spoke to us and what they said
        request = request.lower()               # Convert command to upper case
        print 'reuqeust:', request
        # driveCommands = request.split(',')      # Separate the command into individual drives
            # Special commands
        if request == 'alloff' or request == '0':
            # Turn all drives off
            MotorOff()
            print 'All drives off'
        elif request == 'x':
            # Exit the program
            MotorOff()
            print 'All drives off'
        elif request == 'wa':
            setMotorPower(1)
            setMotorSteer(-1)
        elif request == 'wd':
            setMotorPower(1)
            setMotorSteer(1)
        elif request == 'sa':
            setMotorPower(-1)
            setMotorSteer(-1)
        elif request == 'sd': 
            setMotorPower(-1)
            setMotorSteer(1)
        elif request == 'w':
            setMotorPower(1)
            setMotorSteer(0)
        elif request == 's':
            setMotorPower(-1)
            setMotorSteer(0)
        elif request == 'a':
            setMotorPower(0)
            setMotorSteer(-1)
        elif request == 'd':  
            setMotorPower(0)
            setMotorSteer(1)
        elif request == '0':
            setMotorPower(0)
            setMotorSteer(0)
        elif request == 'w0':
            setMotorPower(1)
            setMotorSteer(0)
        elif request == 's0':
            setMotorPower(-1)
            setMotorSteer(0)


try:
    global isRunning

    # Start by turning all drives off
    MotorOff()
    raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    remoteKeyBorgServer = SocketServer.UDPServer(('', portListen), PicoBorgHandler)
    # Loop until terminated remotely
    isRunning = True
    while isRunning:

        remoteKeyBorgServer.handle_request()
    # Turn off the drives and release the GPIO pins
    print 'Finished'
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    io.cleanup()
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print 'Terminated'
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    io.cleanup()