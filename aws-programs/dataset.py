import paho.mqtt.client as mqtt
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
client=mqtt.Client()
client.connect('172.31.16.222',1883)
print ('Broker Connected')
client.subscribe('iot/gec')

db_client=MongoClient('172.31.16.222',27017)

db=db_client['gec']

c=db['dht']

'''for i in c.find():
 print(i)'''

df=pd.DataFrame(c.find())
#print(df)

# Input Features
X=df.iloc[1:,[2,-1]].values
print(X) # temp, humidity

# Output Outcomes
Y=df.iloc[1:,-2].values
print(Y) # label

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25) # 25% - Test, 75% - Train
print(X_train.shape)
print(X_test.shape)
print(len(Y_train))
print(len(Y_test))

classifier=KNeighborsClassifier(n_neighbors=5) # creating a classifier
classifier.fit(X_train,Y_train) # Model Training

Y_pred=classifier.predict(X_test) # predicting the values of X, Model Testing
print(accuracy_score(Y_pred,Y_test))

def notification(client,userdata,msg):
 t=msg.payload.decode('utf-8')
 t=t.split(',')
 hum=float(t[1])
 temp=float(t[2])
 print('Label:' , classifier.predict([[temp,hum]]))
 print(t)

client.on_message=notification
client.loop_forever()
