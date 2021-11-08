import time
import pywifi
from pywifi import const

def getInterface():
    #check if wifi is connected
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    print('interface :' + iface)

def helpMethod():
    print('helped')
