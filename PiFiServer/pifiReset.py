import RPi.GPIO as GPIO
import time
from threading import Thread

import os
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

os.chdir(get_script_path())

check_cmd = "sudo systemctl status pifiWeb.service | grep Active | awk '{print $2}'"


from commandExec import commandExec
from dataManagement import switchToAp

rest_button = 40
led_pin     = 38

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(rest_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led_pin, GPIO.OUT)


def ledBlink():
    while True:
        data = commandExec(check_cmd).rstrip().lstrip()
        if(data == "active"):
            GPIO.setup(led_pin,GPIO.OUT)
            GPIO.output(led_pin,GPIO.HIGH)
            time.sleep(.5)
            GPIO.output(led_pin,GPIO.LOW)
            time.sleep(.5)
        else:
            time.sleep(1)

i = False


Thread(target=ledBlink).start() 

while True:
    input = GPIO.input(rest_button)
    print(input)
    if(not input):
        print("Starting server")
        Thread(target=commandExec, args= ("sudo systemctl start pifiWeb.service",)).start()   
        time.sleep(1)
        print("Starting Ap")
        switchToAp()
        i = True
    time.sleep(3)