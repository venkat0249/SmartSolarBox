from config import *
import paho.mqtt.client as mqtt
import minimalmodbus
import serial
from datetime import datetime, date, time, timedelta
import json
import time

# instrument = minimalmodbus.Instrument('COM5', 2)  # port name, slave address (in decimal)
# instrument.serial.baudrate = 9600                   # Baud
# instrument.serial.bytesize = 8
# instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
# instrument.serial.stopbits = 1
# instrument.serial.timeout = 0.05                   # seconds


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

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")

Connected = False   #global variable for the state of the connection

# Define on_publish event function
def on_publish(client, userdata, mid):
    print ("Message Published...")

#def on_connect(client, userdata, flags, rc):
#    client.subscribe(MQTT_BOX_STATUS_TOPIC)
#    client.publish(MQTT_BOX_STATUS_TOPIC, MQTT_MSG)

#def on_message(client, userdata, msg):
#    print(msg.topic)
#    print(MQTT_MSG)
#    client.disconnect() # Got message then disconnect

# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
#mqttc.on_message = on_message

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

mqttc.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)

try:
    while True:
 
        mqttc.publish(MQTT_BOX_STATUS_TOPIC, MQTT_MSG)
        time.sleep(10)
 
except KeyboardInterrupt:

    mqttc.disconnect()
    mqttc.loop_stop()
#mqttc.sleep(2)   
# Loop forever
#mqttc.loop_forever()
