# receive data from remote device

import paho.mqtt.client as mqtt
from pymongo import MongoClient
import time

flag=0
label=0
db_client=MongoClient('172.31.16.222',27017)
db=db_client['gec'] # select the db
c=db['dht'] # collection name

client=mqtt.Client()
client.connect('172.31.16.222',1883)
print('Broker Connected')

client.subscribe('iot/gec')

def notification(client,userdata,msg):
 global flag,label
 t=(msg.payload).decode('utf-8')
 t=t.split(',')
 hum=t[1]
 temp=t[2]
 if(float(hum)>80 and float(hum)<=90):
  label=0
 elif(float(hum)>90 and float(hum)<=93):
  label=1
 elif(float(hum)>93 and float(hum)<=96):
  label=2
 elif(float(hum)>96 and float(hum)<=100):
  label=3
 k={}
 k['humidity']=float(hum)
 k['temp']=float(temp)
 k['label']=label
 print (k)
 c.insert_one(k)
 print ('Data Inserted')
 if(float(hum)>90 and flag==0):
  print ('Send Notification to User')
  flag=1
 elif(float(hum)<90):
  flag=0

client.on_message=notification
client.loop_forever()
