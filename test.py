from citc.communicators.serialcommunicator import SerialCommunicator
import paho.mqtt.client as mqtt
import sys
import traceback
import logging
import threading
import pprint
import json
import time
import os

try:
    import queue
except ImportError:
    import Queue as queue

def determine(x):
    return {

        '0x10': "BrownI",
        '0x30': "Brown0",
        '0x70': "White0",
        '0x50': "WhiteI",
        '0x37': "B0W0",
        '0x15': "BIWI",
        '0x17': "BIW0",
        '0x35': "B0WI",
        '0x0': "Neutral"
    }[x]

def msgPorte(x):
    return {
        '0x9': "close",
        '0x8': "open"
    }[x]

def msgPrise(x):

    return 


def on_connect(client, obj, flags, rc):
    print("enocean-server is connected to the mqtt with result code "+str(rc))

def on_disconnect(client, flags, rc):
    print("enocean-server is disconnected to the mqtt with result code "+str(rc))

def on_message(client, userdata, msg): #incoming MQTT
    print("No callback for message: ")

def send(topic, msg):
    mqttclient.publish(str(topic),str(msg))

def convertHex(tabDec):
    result = []
    for i in tabDec:
        result.append(hex(i))

    return result

def convertTemp(x):
   return 40-(x/(255/40)) 
    

#enocean = SerialCommunicator(port="/dev/tty.usbserial-FTWTOH0A")
enocean = SerialCommunicator(port="/dev/ttyUSB0")

print(enocean)

ip='smartlivinglab.fr'
port=1883
timeout=60
#Begin listen Encoean Telegrams
enocean.daemon = True
enocean.start()

#MQTT
mqttclient = mqtt.Client(client_id="client-"+str(os.getpid()), clean_session=True)
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.on_disconnect = on_disconnect    
mqttclient.connect(ip, port, timeout)
mqttclient.loop_start()
#mqtt.subscribe(topic="#")

test =""
while enocean.is_alive():

    try:
        
        p = enocean.receive.get(block=True, timeout=1)
        print(p)
        print("Les donnees sont ")

        print(p.data)
        tabConv = []
        for i in p.data:
            tabConv.append(hex(i))


        print("Envoie du MQTT")
        
        #Si c'est l'interrupteur
        if p.sender == 2690016:
            print("Communication de l'interrupteur")
            
            if tabConv[6] == "0x20":
                print("Interrupteur relache")
            
            if tabConv[6] == "0x30":
                print("Interrupteur appuye. Bouton est : " + determine(tabConv[1]))

            send(p.sender,determine(tabConv[1]))
           
        
        if p.sender == 25203027:
            print("Communication du detecteur de porte")
            send(p.sender, msgPorte(tabConv[1]) )

        if p.sender == 26374959:
            send(p.sender, p.data[6])

        if p.sender == 25307177:
            send(p.sender, convertTemp(p.data[3]))


        print("Previous : ") 
        print(str(convertHex(test)))
        print("now : ")
        print(str(p.data))
        test = p.data

    except queue.Empty:
        continue
    except KeyboardInterrupt:
        break
    except Exception:
        traceback.print_exc(file=sys.stdout)
        continue    
enocean.stop()

    

