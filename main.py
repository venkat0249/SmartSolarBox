from config import *
from flask import Flask, render_template #used for the server and delivering html pages
from flask_socketio import SocketIO, emit #used for asynchronous event-based communication between server and client
from flask_mqtt import Mqtt
from threading import Thread, Event
from random import random
from time import sleep


"""
This file creates an mqtt client and updates an html webpage when mqtt client receives info
"""

app = Flask(__name__) #create the server application
app.config['SECRET_KEY'] = 'ecowet' #not sure what this is for yet
app.config['TEMPLATES_AUTO_RELOAD'] = False
app.config['MQTT_BROKER_URL'] = MQTT_HOST  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = MQTT_PORT  # default port for non-tls connection
app.config['MQTT_USERNAME'] = MQTT_USERNAME  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = MQTT_PASSWORD # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = MQTT_TLS_ENABLED  # set TLS to disabled for testing purposes
socketio = SocketIO(app) #create the socket IO instance for comms
mqtt = Mqtt(app) #create the mqtt instance for mqtt comms
hostname = FLASK_HOST #hostname where flask will run
port = FLASK_PORT #flask port
mqtt_topic = MQTT_BOX_STATUS_TOPIC

thread = Thread()
thread_stop_event = Event()

@app.route("/") #base route (or path/url)
def index():
    return render_template('index.html') #display the main html file


@socketio.on('subscribe') #defined in the javascript
def handle_subscribe(topic):
    print("MQTT subscribing to " + topic)
    mqtt.subscribe(topic) #just subscribe to the topic

@socketio.on('connect') # whenever a client connects to url 'hostname:port/test'
def test_connect():
    print('Client connected')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(mqtt_topic)
    print("MQTT subscribing to haha " + mqtt_topic)

#define what will happen when mqtt broker gets a message from its subscription
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print(message.payload.decode())
    socketio.emit('mqtt_message',data=data) #emit the data to be caught by the javascript client-side app 
    #socketio.emit('test_number',{'number': '10hi'},namespace='/')

if __name__ == "__main__":
    app.run(host=hostname, port=port) 