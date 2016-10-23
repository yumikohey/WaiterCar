"""
Reference:
Raspberry Pi - Distance Sensor
https://www.youtube.com/watch?v=iNXfADw0M9Y    
"""
import time
from socket import *
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
print 'PI ultrasonic sensor llient is connecting to computer server host at 10.3.33.106...'
#The raspberry pi acts like the client sending sensor data to host pc like the pi_camera_client.py
# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
# client_socket.connect(('192.168.0.100', 8000))
# client_socket.connect(('192.168.0.103', 8000))
# client_socket.connect(('10.3.33.106', 8001))  #macbook ip address
client_socket.connect(('192.168.43.103', 8001))  #macbook ip address
# Make a file-like object out of the connection
# connection = client_socket.makefile('wb')

def measure():
    """
    measure distance
    """
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = time.time()

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    # print round(distance,2)

    return round(distance,2)

# referring to the pins by GPIO numbers
GPIO.setmode(GPIO.BCM)

# define pi GPIO
TRIG = 23
ECHO = 17

# output pin: Trigger
GPIO.setup(TRIG,GPIO.OUT)
# input pin: Echo
GPIO.setup(ECHO,GPIO.IN)
# initialize trigger pin to low
GPIO.output(TRIG, False)
print 'Waiting for sensor...'
time.sleep(2)

try:
    while True:
        distance = measure()
        # time.sleep(0.1)
        # d1 = measure()
        # time.sleep(0.1)
        # d2 = measure()
        # sum_d = (distance + d1 + d2)/3.
        print "Distance : %.2f cm" % distance
        # send data to the host every 0.5 sec
        # client_socket.send(str(distance))
        client_socket.send(str(distance))
        time.sleep(0.1)
finally:
    client_socket.close()
    GPIO.cleanup()
