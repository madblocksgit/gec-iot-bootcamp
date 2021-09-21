import cv2
import numpy as np
import tensorflow.keras
from PIL import Image, ImageOps

from gtts import gTTS
import pygame
import os
import time

# Load the DL Model
model=tensorflow.keras.models.load_model('keras_model.h5')

# to play audio
def play_audio(b):
 language='en'
 m=gTTS(text=b,lang=language,slow=False)
 m.save('out.mp3')
 pygame.mixer.init()
 # Loading the song
 pygame.mixer.music.load("out.mp3")
  
 # Setting the volume
 pygame.mixer.music.set_volume(0.7)
  
 # Start playing the song
 pygame.mixer.music.play()
 time.sleep(2)
 pygame.mixer.music.stop()
 time.sleep(1)
 pygame.quit()
 os.remove('out.mp3')
 
def sign_language_detector(a):
 
 # empty data variable
 data=np.ndarray(shape=(1,224,224,3),dtype=np.float32)
 
 # open the image
 image=Image.open(a)

 # resize the image to 224 x 224
 size=(224,224)
 image=ImageOps.fit(image,size,Image.ANTIALIAS)
 
 # convert this image into numpy array
 image_array=np.asarray(image)

 # Feature Scale the Image (0-2)
 normalise_image_array=(image_array.astype(np.float32)/127.0) - 1
 
 # load this image into data
 data[0]=normalise_image_array

 # pass this data to model
 result=model.predict(data)
 result=list(result[0])
 result1=max(result)
 index_result=result.index(result1)
 if (index_result==0):
   print ('No Hand Detected')
 elif (index_result==1):
   print ('Like Detected')
   play_audio('Like Detected')
   
 elif (index_result==2):
   print ('Victory Detected')
   play_audio('Victory Detected')

cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,240)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# Acquiring the images
while True:
 res,frame=cam.read()
 if res==1:
  cv2.imwrite('test.jpg',frame)
  cv2.imshow("capturing",frame)
  sign_language_detector('test.jpg')
  key=cv2.waitKey(1)
  if key==ord('q'):
   break
 else:
  print ('No Frame')

cam.release()
cv2.destroyAllWindows()
