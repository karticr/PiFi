#!/usr/bin/env python3
from flask import Flask, render_template, flash, request, url_for, redirect, Response, jsonify          
from time import sleep     
from threading import Thread
import subprocess
import os
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

os.chdir(get_script_path())

import dataManagement as dm
from commandExec import commandExec

app = Flask(__name__)


def getWifiList():
    data = "sudo iw dev wlan0 scan | grep SSID | awk '{print $2}'"
    ret = commandExec(data)
    ret = ret.split("\n")
    ret = [x for x in ret if x]
    return ret

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return redirect("http://192.168.4.1/login" )


@app.route('/login', methods=["GET", "POST"])
def index():
    access_point="yolo"
    wifi_list = getWifiList()
    return render_template('index.html', wifi_list = wifi_list, access_point=access_point)



@app.route('/setwifi', methods=["GET", "POST"])
def setWifi():
    try:
        if request.method == "POST":
            attempted_ssid = request.form['ssid']
            attempted_psk  = request.form['psk']
            print(attempted_ssid)
            print(attempted_psk)
            Thread(target=dm.switchToWifi, args=(attempted_ssid, attempted_psk, )).start()
            return render_template('restart.html', message = "Restart in progress, wait. rrawr", alert_msg = "Restart Complete")
    except Exception as e:
        print(str(e))
        return render_template('404.html'), "Error"


@app.route('/changeap', methods=["GET", "POST"])
def changeSettings():
    try:
        if request.method == "POST":
            attempted_ssid         = request.form['ssid_ap']
            attempted_psk          = request.form['psk_ap']
            attempted_new_psk      = request.form['psk_new_ap']
            attempted_confirm_psk  = request.form['psk_confirm_ap']
            print(attempted_ssid)
            print(attempted_psk)
            print(attempted_new_psk)
            print(attempted_confirm_psk)
            return render_template('restart.html', message = "Changing Settings", alert_msg = "Settings Updated")
    except Exception as e:
        print(str(e))
        return render_template('404.html'), "Error"
        
    return "yolo"

@app.route('/ierror')
def iError():
    return render_template('connectionError.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 80, threaded=True, debug=True)                                          # Starting the Flask App and giving it permission to be accessable by all the ip addresses.
