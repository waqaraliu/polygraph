import subprocess
from httpsession import main
from configparser import ConfigParser
import socket
import os
import re
import time
from zeroconf import ServiceInfo, Zeroconf
import logging

deviceId = None
bonjourHost=None
port=None
framerate=None
resolution=None
deviceIp=None
zeroconf = None
info = None

def startTestServer1():
    print('starting rt server')
    
def startTestServer2():
    print('starting narrow BW server')
    executeProcess()
    
def getBonjourIp():
    global deviceIp
    try:
        #host_name = socket.gethostname()
        #host_ip = socket.gethostbyname(host_name)
        #print("Hostname :  ",host_name)
        ip = re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), os.popen('ip addr show eth0').read()).groups()[0]
        deviceIp = ip
        print('IP is :' + ip)
    except:
        print("Unable to get Hostname and IP")

def createBonjourService():
    global info
    host_ip = socket.gethostbyname( socket.gethostname())
    desc = {'version':"0.1",'name':'BonjourService'}
    info = ServiceInfo(
           "_" + "bonjourservice" + "._tcp.local.",
           "Server._" + "bonjourservice" + "._tcp.local.",
           addresses=[socket.inet_aton("169.254.0.5")],
           port=8089,
           properties=desc,
           server="BonjourService.local.",
       )
    
def stop_zeroconf():
      """Stop Zeroconf."""
      logging.info("Stopping Zeroconf...")
      zeroconf.unregister_service(info)
      zeroconf.close()
      
def register_zeroconf():
    logging.info("   Registering service...")
    zeroconf.register_service(info)
    logging.info("   Registration done.")
    
def parseConfigFile():
    global deviceId, bonjourHost, port, framerate, resolution
    config = ConfigParser()
    config.read('config.ini')
    deviceId = config.get('device', 'deviceId')
    bonjourHost = config.get('device', 'bonjour')
    port = config.get('device', 'port')
    framerate = config.get('device', 'framerate')
    resolution = config.get('device', 'resolution')
    print('device :' + deviceId + ' ,bonjourHost:' + bonjourHost + ' ,port:' + port + ' ,frameRate:' + framerate + ' ,Resolution:' + resolution)
    
def executeProcess():
    try:
        
        p = subprocess.call("/home/pi/polygraf/app/app --log-level=0 --host=" + deviceIp + " --port=" + port + " -f " + framerate + " -l -r " + resolution + " -m mjpeg", shell=True)
        print('Executing Process')
        #p.wait()
    except KeyboardInterrupt:
        print('closing app')
    except BrokenPipeError:
        print('closing app')
        
    
def startHttpApp():
    p = subprocess.call("ping -c1 `ip -4 route show default | awk '/default/ {print $3}'`", shell=True)
    
def app():
    global zeroconf
    print('starting main app')
    #get app config first
    parseConfigFile()
    zeroconf = Zeroconf()
    #here check Ethernet
    while True:
        #if ethernet connected then proceed to HDMI capture device
        #check if capture device is connected
        out = subprocess.call("ping -c1 `ip -4 route show default | awk '/default/ {print $3}'`", shell=True)
        print(out)
        if out == 0:
            print('Ethernet Connected')
            getBonjourIp()
            createBonjourService()
            register_zeroconf()
            print('Exiting')
            #exit()
            return
        else:
            print('Please check Ethernet Connection')
            time.sleep(5)
        print('looping')
    #main()
if __name__ == '__main__':
    app()




