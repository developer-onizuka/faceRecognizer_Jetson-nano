#!/usr/bin/python3
import face_recognition
import cv2
from adafruit_servokit import ServoKit
myKit=ServoKit(channels=16)
#import time
print(cv2.__version__)

donFace=face_recognition.load_image_file('~/Desktop/pyPro/faceRecognizer/demoImages/known/Donald Trump.jpg')
donEncode=face_recognition.face_encodings(donFace)[0]
#print(donEncode)
nancyFace=face_recognition.load_image_file('~/Desktop/pyPro/faceRecognizer/demoImages/known/Nancy Pelosi.jpg')
nancyEncode=face_recognition.face_encodings(nancyFace)[0]
#print(nancyEncode)

Encodings=[donEncode,nancyEncode]
Names=['The Donald','Nancy Pelosi']

font=cv2.FONT_HERSHEY_SIMPLEX
dispW=640
dispH=480
pan=145
tilt=100
cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

CenterW1=int(dispW/2)-int(dispW*.01)
CenterW2=int(dispW/2)+int(dispW*.01)
CenterH1=int(dispH/2)-int(dispH*.01)
CenterH2=int(dispH/2)+int(dispH*.01)

myKit.servo[0].angle=pan
myKit.servo[1].angle=tilt

red=0
green=255
blue=0
while True:
    _,frame=cam.read()
    frameSmall=cv2.resize(frame,(0,0),fx=.5,fy=.5)
    frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
    facePositions=face_recognition.face_locations(frameRGB,model='cnn')
    allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
    for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
        name='Unknown Person'
        matches=face_recognition.compare_faces(Encodings,face_encoding)
        if True in matches:
            first_match_index=matches.index(True)
            name=Names[first_match_index]
        top=int(top*2)
        right=int(right*2)
        bottom=int(bottom*2)
        left=int(left*2)
        if matches[0]:
            red=255
        cv2.rectangle(frame,(left,top),(right,bottom),(blue,green,red),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,255,255),1)
        blue=0
        green=0
        red=0
        faceW=int((left+right)/2)
        faceH=int((top+bottom)/2)
        if faceW > CenterW2:
            pan=pan-int((faceW-CenterW2)/29)
        if faceW < CenterW1:
            pan=pan+int((CenterW1-faceW)/29)
        if faceH > CenterH2:
            tilt=tilt-int((faceH-CenterH2)/29)
        if faceH < CenterH1:
            tilt=tilt+int((CenterH1-faceH)/29)
        if pan>180:
            pan=180
            #print('Pan Out Of Range')
        elif pan<0:
            pan=0
            #print('Pan Out Of Range')
        if tilt>180:
            tilt=180
            #print('Pan Out Of Range')
        elif tilt<0:
            tilt=0
            #print('Pan Out Of Range')
        myKit.servo[0].angle=pan
        myKit.servo[1].angle=tilt
    cv2.imshow('nanoCam',frame)
    #cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break 
cam.release()
cv2.destroyAllWindows()
