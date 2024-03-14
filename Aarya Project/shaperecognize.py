# pip install opencv-contrib-python    ----> for using extra opencv modeules
# pip install cvlib  ----> This is used for the object detection
# pip install gtts playsound   ---> gtts(Google to text speech ),this is used for when the system saw the object it make sound to that object
# python -m pip install --upgrade pip setuptools wheel  (To update the wheel)

import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox  # drwa_bbox ---> so that the box appears to the object
from gtts import gTTS
from playsound import playsound


video = cv.VideoCapture(0)

while True:
    ret,frame = video.read()
    bbox,label,conf = cv.detect_common_objects(frame)
    output_img = draw_bbox(frame,bbox,label,conf)
    
    
    cv2.imshow("Object Detecting",output_img)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    