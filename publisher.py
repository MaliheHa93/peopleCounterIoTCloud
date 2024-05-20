import paho.mqtt.client as mqtt
import time 
from datetime import datetime
import os
import urllib.parse 
import json
import random
import csv
import numpy as np
from glob import glob
from csv import DictReader
from json import dumps
from itertools import groupby
import requests
import threading 
import queue 
import schedule
import api.flask_api as api
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))

def on_message(client, obj, msg):
    json_str = json.dumps(topic, separators=(',', ':'))
    print(json_str)
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
       
def on_publish(client, obj, mid):
    
    print("mid: " + str(mid))

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish


url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urllib.parse.urlparse(url_str)
topic = url.path[1:] or 'test'

# Connect
mqttc.username_pw_set(url.username, url.password)
mqttc.connect(url.hostname, url.port)


# Publish a message
mqttc.publish(topic, "Number of people in each vehicles is: ")

#Reading the entering and exiting info of vehicles 
enter=[]
exit=[]
round=1
json_object={}
class fleet:
    def __init__(self) -> None:
        self.inputkey=""
    __allEnterance=[]
    __allExiting=[]
    
    #the function that read all the csv files from the directory
    def readingbVehicleSCV(self,f):
        buslist=[]
        trainlist=[]
        tramlist=[]
        
        for csvFileName in glob(f):
            datas = {}
            groups = []
            uniquekeys = []
            
            with open(csvFileName, 'r', encoding='utf8') as csvFile:
                csvReader = DictReader(csvFile, skipinitialspace=True)
                listOfRows = [rows for rows in csvReader]
                data = [dict(d) for d in csvReader]

                for row in listOfRows:
                    listOfKeys = [key for key in row]

                if "ID" in listOfKeys:
                    self.inputKey = "ID"
                else:
                    self.getKey(listOfRows)

                for rows in listOfRows:
                    datas[rows[self.inputKey]] = rows
                

                jsonName = f + csvFileName.split('.')[0]+'.json'
            with open(jsonName, 'w', encoding='utf8') as jsonFile:
                jsonFile.write(dumps(datas,indent=4))
            datas.clear()

        print(f'[SUCCESSFULLY CONVERTED ALL \'EM CSV FILES]')
    
    #read Json files
    def read_jSONFiles(self,f):
        with open(f, 'r') as busfile:
            json_object = json.load(busfile)
        with open(f, "r") as trainfile:
            jjson_object = json.load(trainfile)  
        with open(f, "r") as tramfile:
            json_object = json.load(tramfile)
        #print(json_object)


#create object form fleet object
Bus = fleet()    
Tram = fleet() 
Train = fleet() 

#1.reading Bus
Bus.readingbVehicleSCV(r"../csv files/Bus.csv")
#schedule.every(10).minutes.do()

#3.reading Train
Train.readingbVehicleSCV(r"../csv files/Train.csv")

#3.reading Tram
Tram.readingbVehicleSCV(r"../csv files/Tram.csv")

#read JSON files for sending to threads in each round
Bus.read_jSONFiles("csv files/Bus.json")
Train.read_jSONFiles("csv files/Train.json")
Tram.read_jSONFiles("csv files/Tram.json")

#First: create thread for sending multiple json payloads through http requset to API
exitFlag = 0
class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q)
      print ("Exiting " + self.name)

def process_data(threadName, q):
   while not exitFlag:
      queueLock.acquire()
      if not workQueue.empty():
         data = q.get()
         print(data)
         queueLock.release()
         sendRequest(data)
         #print ("%s processing %s" % (threadName, data))
      else:
         queueLock.release()
         time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
#nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(1000)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for word in json_object:
   workQueue.put(word)
   
queueLock.release()
#print("word is",workQueue)

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")

#
def read_nextRound():
    schedule.every(10).minutes.do()

#second: post payload in json format to url in API by requests module
def sendRequest(payload):
   response=requests.post('http://127.0.0.1:5000/count', data=payload)
   response.json()
