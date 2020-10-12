#!/usr/bin/env python
# coding: utf-8

# In[1]:


# importing libraries
import sqlite3
import paho.mqtt.client as mqtt
import time as t
import minimalmodbus
import serial
from datetime import datetime, date, timedelta
import json
import traceback
import sys

client = mqtt.Client() # here we are getting the instance of the Client class

exitFlag = True # this is taken for the authentication purpose

client.username_pw_set(username="Anand",password="12345678") # username and password set by me for connection




#---------------------------------------------------------------------------------------------------------------
# Modbus Communication Parameters

# instrument = minimalmodbus.Instrument('COM5', 2)  # port name, slave address (in decimal)
# instrument.serial.baudrate = 9600                   # Baud
# instrument.serial.bytesize = 8
# instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
# instrument.serial.stopbits = 1
# instrument.serial.timeout = 0.05                   # seconds


# ========================Call Backs==========================================================================
def on_publish(client,userdata,mid):        # call back for the published data
    print("Payload Published: "+str(mid))   # printing the message id of the published message

def on_connect(pvtClient,userdata,flags,rc):   # call back for the connection acknowledgement
    global exitFlag # here I am setting the exitFlag based on connection status, we will use this flag later on
    if(rc == 0):  # on successful connection
        print("publisher Connected")  # printing the data
        print("Connected to client! Return Code:"+str(rc)) # printing the data on the screen
        exitFlag = False

    elif(rc ==5): # in case of authentication error
        print("Authentication Error! Return Code: "+str(rc))  # printing the data on the screen
        client.disconnect()
        exitFlag = True

# here we are using this call back for the logs generation, these logs are helpful to us while debugging
def on_log(client, userdata, level, buf):   # call backs for the logs,
    print("Logs: "+str(buf))                # printing the logs on the screen, this will show the logs
                                            #about the flags that will used by the publisher and subscriber

def on_disconnect(pvtClient, userdata, rc): # this call back will run, when a disconnect() is received
    print("disconnecting reason  " +str(rc))
    client.disconnect()

# ============================================================================================================
# Associating the functions with the call backs===========================================
client.on_publish       = on_publish
client.on_connect       = on_connect
client.on_log           = on_log
client.on_disconnect    = on_disconnect
# ============================================================================================================
# Establishing Connection ========

host       = "localhost"
port       = 1883
keepAlive  = 45

client.connect(host,port,keepAlive)
# =========================================

# starting the loop
# we are using this loop and sleep in-between client.connect(...) and client.publish(...)
# so we can observe the call backs
client.loop_start();        # starting a loop in order to observe the call backs
t.sleep(2)               # giving a sleep time for the connection to setup

# once connected, publish the message
# ============Publishing the message ======
topic_name = "anand/smartsolarbox/data"
QOS        = 2                  # here we can use different Quality of service, based on our requirement
retain     = True

# if the connection is successful then this while loop will run
while(exitFlag == False):   # here we are using the flags which we have set earlier,
    t.sleep(10)          # giving some time for the call backs to process
    
    #------------------------------------------------------------------------------------------------------------------------------

    # Variabes to be read

    # Solar_Array_Current= instrument.read_register(57,3,signed = True) 
    # Solar_Array_Voltage= instrument.read_register(57,3,signed = True)
    # Solar_Array_Power= instrument.read_register(57,3,signed = True)
    # Battery_Current= instrument.read_register(57,3,signed = True)
    # Battery_Voltage= instrument.read_register(57,3,signed = True)
    # Battery_SOC= instrument.read_register(57,3,signed = True)
    # Load_Current= instrument.read_register(57,3,signed = True)
    # Load_Voltage= instrument.read_register(57,3,signed = True)
    # Load_Power= instrument.read_register(57,3,signed = True)
    # Box_Temperature= instrument.read_register(57,3,signed = True)
    # timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    #-------------------------------------------------------------------------------------------------------


    #Dummy Values---------------------------------------------------------------------------------------
    Solar_Array_Current= 2
    Solar_Array_Voltage= 51
    Solar_Array_Power= 102
    Battery_Current= 5
    Battery_Voltage= 48
    Battery_SOC= 90
    Load_Current= 3
    Load_Voltage= 230
    Load_Power= 690
    Box_Temperature= 35
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    data = {"Solar_Array_Current=":Solar_Array_Current, "Solar_Array_Voltage=":Solar_Array_Voltage,
    "Solar_Array_Power=":Solar_Array_Power,"Battery_Current=":Battery_Current,"Battery_Voltage=":Battery_Voltage
   ,"Battery_SOC=":Battery_SOC,"Load_Current=":Load_Current,"Load_Voltage=":Load_Voltage,
   "Load_Power=":Load_Power,"Box_Temperature=":Box_Temperature,"timestamp=":timestamp}

    MQTT_MSG = json.dumps(data)

    payload = MQTT_MSG 
    client.publish(topic_name,payload,QOS,retain)  # publishing the message (payload)
    if(payload == "exit(0)"):   # in case user has entered "exit(0)" then exit and disconnect
        client.disconnect()



#For a given MQTT setup we can set this value of either 0, 1, 2, wherein
#different QOS have different properties

#Also, in our case, we can use the functionality of retaining the last known message
#in case the given client (subscriber) is not present, or unable to receive the message
#(payload), Hence, setting the value of retain parameter as True or 1 will make sure that
#in case of undelivered message, the given message is retained
# =========================================
# If you use the loop_start() or loop_forever functions then the loop runs in a separate thread,
# and it is the loop that processes the incoming and outgoing messages.

client.loop_stop()  # stopping the time loop

# make sure to use client.loop_stop() function too, if we have used client.loop_start() function


# In[ ]:




