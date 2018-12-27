from passlib.hash import sha256_crypt
import os
import sqlite3 as lite
import subprocess
from time import sleep

import confVariables as cf
from commandExec import commandExec

pwd = os.getcwd()


def saveToFile(file, data):
    with open (file, 'w') as w:
        w.write(data)

def checkPassword(input_pwd):
    with open(pwd+'/.pwd_hash.txt', 'r') as r:
        data = r.read()
        res = sha256_crypt.verify(input_pwd, data)
        return res
        
def savePassword(password):
    hashed_pwd = sha256_crypt.encrypt(password)
    saveToFile(pwd+'/.pwd_hash.txt', hashed_pwd)

def editWifi(ssid, psk):
    data = cf.wifi_config.format(ssid, psk)
    saveToFile(cf.wifi_config_dir, data)
   
def editAP(ssid, psk):
    data = cf.hostapd_conf.format(ssid, psk)
    saveToFile(cf.hostapd_conf_dir, data)
    sleep(1)
    resetAP()

def resetDhcpcd():
    sleep(1)
    commandExec(cf.damean_reload)
    sleep(1)
    commandExec(cf.dhcpcd_restart)
    sleep(1)

def resetAP():
    commandExec(cf.stop_ap_services)
    sleep(.5)
    commandExec(cf.start_ap_serivces)
    sleep(.5)


def switchToWifi(ssid, psk):
    editWifi(ssid, psk)
    dhcpd_data_wifi = cf.wifi_dhcpd_config.format(' ')
    saveToFile(cf.wifi_dhcpd_dir, dhcpd_data_wifi)
    resetDhcpcd()
    hostapd_wifi = cf.hostapd_config.format(' ')
    saveToFile(cf.hostapd_dir, hostapd_wifi )
    commandExec('sudo reboot')

def switchToAp():
    data = cf.wifi_dhcpd_config.format(cf.wifi_dhcpd_data)
    saveToFile(cf.wifi_dhcpd_dir, data)
    resetDhcpcd()
    data = cf.hostapd_config.format(cf.hostapd_config_data)
    saveToFile(cf.hostapd_dir, data )
    resetAP()


