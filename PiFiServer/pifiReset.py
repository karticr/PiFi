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


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)



def ledBlink():
    while True:
        data = commandExec(check_cmd).rstrip().lstrip()
        if(data == "active"):
            GPIO.setup(18,GPIO.OUT)
            GPIO.output(18,GPIO.HIGH)
            time.sleep(.5)
            GPIO.output(18,GPIO.LOW)
            time.sleep(.5)


i = False


Thread(target=ledBlink).start() 

while True:
    input = GPIO.input(23)
    print(input)
    if(input):
        print("Starting server")
        Thread(target=commandExec, args= ("sudo systemctl start pifiWeb.service",)).start()   
        time.sleep(1)
        print("Starting Ap")
        switchToAp()
        i = True
    time.sleep(3)