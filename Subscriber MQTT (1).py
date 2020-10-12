#!/usr/bin/env python
# coding: utf-8

# In[3]:


# importing Libraries 
import paho.mqtt.client as mqtt
import time
import json
from datetime import datetime, date
import traceback
import sys
import sqlite3

#---------------------------------------------------------------------------------------------------------------------------

client      =   mqtt.Client()
topicName   =   "anand/smartsolarbox/data"
QOS_val        =   2

client.username_pw_set(username="anand",password="12345678")

#SQLite table Creation---------------------------------------------------------------

try:
    sqliteConnection = sqlite3.connect('Smart_Solar_Box.db')
    sqlite_create_table_query = '''CREATE TABLE BoxStatus_HistoryTbl (
                                RowID INTEGER PRIMARY KEY,
                                JSONData TEXT NOT NULL,
                                Timestamp datetime);'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")

#--------------- Defining call backs---------------------------------------------------------------
def on_connect(pvtClient,userdata,flags,rc):
    if(rc == 0):
        print("Connected to client! Return Code:"+str(rc)) # printing the data on the screen
        result = client.subscribe(topicName, QOS_val)  # getting the Tuple from the call back

    elif(rc ==5):
        print("Authentication Error! Return Code: "+str(rc))  # printing the data on the screen
        client.disconnect()


def on_message(pvtClient, userdata, msg):
    # here we are extracting details from the msg parameter,
    print("\n============================================")
    print("Payload       : " +str(msg.payload.decode()))
    print("Qos of message: "+str(msg.qos))
    print("Message Topic : "+str(msg.topic))
    print("Message retain: "+ str(msg.retain))
    print("============================================\n")
        #Connecting to sqlite
    conn = sqlite3.connect('Smart_Solar_Box.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    now = datetime.now()
#     print(tim)
    print(type(now))

    # Preparing SQL queries to INSERT a record into the database.
    sql_insert = ('''INSERT INTO BoxStatus_HistoryTbl(
       JSONData, Timestamp)
        VALUES (?,?) ''');
    data = (str(msg.payload.decode()),now,)
    cursor.execute(sql_insert,data,)


    conn.commit()
    print("Records inserted........")

    # Closing the connection
    conn.close()

    if(msg.payload.decode() == "exit(0)" ):
        client.disconnect()

# currently not using this callback
def will_set(pvtClient, payload="disconnected!!!", qos=2, retain=False):
    print("status: "+payload)

def on_log(topic, userdata, level, buf):
    print("Logs: "+str(buf))
# -------------------------------------------------------------------------------------------------------------

# ======== Associating the methods with the given callbacks of the MQTT ======
client.on_connect   =   on_connect
client.on_message   =   on_message
client.on_log       =   on_log
#client.will_set     =   will_set
# ============================================================================

host        = "localhost"
port        = 1883
keepAlive   = 60

client.connect(host,port,keepAlive) # establishing the connection

time.sleep(2)               # giving a sleep time for the connection to setup
 
client.loop_forever()


# In[ ]:





# In[ ]:




