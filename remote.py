#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  remote.py - Control a 3-button remote to raise and lower a projector screen
#
#  Kyle Gabriel (2015)
#
# Start with: remote.py -up
#             remote.py -s

import getopt
import sys
import time
import RPi.GPIO as GPIO

# GPIO pins connected to the remote buttons
upPin = 8
downPin = 4
stopPin = 3

def usage():
    print "remote.py: Control a 3-button remote to raise and lower a" \
          "projector screen\n"
    print "Usage: remote.py OPTION\n"
    print "Options:"
    print "    -i, --initialize"
    print "           Initialize the GPIO pins (set all low)"
    print "    -d, --down"
    print "           Lower the screen"
    print "    -s, --stop"
    print "           Halt movement of the screen"
    print "    -u, --up"
    print "           Raise the screen"
    print "    -h, --help"
    print "           Show this help and exit"

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(upPin, GPIO.OUT)
    GPIO.output(upPin, 0)
    GPIO.setup(downPin, GPIO.OUT)
    GPIO.output(downPin, 0)
    GPIO.setup(stopPin, GPIO.OUT)
    GPIO.output(stopPin, 0)

if len(sys.argv) == 1: # No arguments given
    usage()
    sys.exit(1)

try:
    opts, args = getopt.getopt(sys.argv[1:], 'idsuh',
        ["initialize", "down", "stop", "up", "help"])
except getopt.GetoptError as err:
    print(err) # print "option -x not recognized"
    usage()
    sys.exit(2)

try:
    for opt, arg in opts:
        if opt in ("-i", "--initialize"):
            print "Initializing GPIO pins connected to the projector remote"
            init()
        elif opt in ("-u", "--up"):
            init()
            print "Raising projector screen"
            GPIO.output(upPin, 1)
            time.sleep(1)
            GPIO.output(upPin, 0)
            time.sleep(36.5) # delay (seconds) for screen to fully raise
            GPIO.output(stopPin, 1)
            time.sleep(1)
            GPIO.output(stopPin, 0)
        elif opt in ("-d", "--down"):
            init()
            print "Lowering projector screen"
            GPIO.output(downPin, 1)
            time.sleep(1)
            GPIO.output(downPin, 0)
            time.sleep(39) # permit catching ctrl+c to stop screen descent
            GPIO.output(stopPin, 1)
            time.sleep(1)
            GPIO.output(stopPin, 0)
        elif opt in ("-s", "--stop"):
            init()
            print "Stopping projector screen movement"
            GPIO.output(stopPin, 1)
            time.sleep(1)
            GPIO.output(stopPin, 0)
        elif opt in ("-h", "--help"):
            usage()
except KeyboardInterrupt:  
    GPIO.output(stopPin, 1)
    time.sleep(1)
    GPIO.output(stopPin, 0)
    print "Keyboard interrupted operation!"
except:
    GPIO.output(stopPin, 1)
    time.sleep(1)
    GPIO.output(stopPin, 0)
    print "Other error!"