################### import some important packages
from pyimagesearch.tempimage import TempImage
from picamera.array import PiRGBArray
from picamera import PiCamera
from functools import partial
from creat_faceID import creat_faceid
from Search import search
from send_message import send
import argparse
import warnings
import datetime
import imutils
import json
import time
import cv2
import os
import multiprocessing as mp
import urllib2
import urllib
#import time
#import json
import re
import urlparse
#import urllib.request


###################################################



################################################### 
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
    help="path to the JSON configuration file")
args = vars(ap.parse_args())
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
###################################################




######### Setup the ccamera #######################
camera = PiCamera()
camera.resolution = tuple(conf["resolution"]) 
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))
face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.1.0/data/lbpcascades/lbpcascade_frontalface.xml') 
print "[INFO] warming up..."
time.sleep(conf["camera_warmup_time"])
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
fcounter = 0
facefind = 0
face_set = 0
motion_set = 0
faceid="0"
###################################################
# from the camera to capture the original dates####
for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = f.array
    timestamp = datetime.datetime.now()
    text = "Unoccupied"
    #######################################
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if avg is None:
            print "[INFO] starting background model..."
            avg = gray.copy().astype("float")
            rawCapture.truncate(0)
            continue
 
    # accumulate the weighted average between the current frame and
    # previous frames, then compute the difference between the current
    # frame and running average


    ######################################
    # capture the face(s)
#    if fcounter == 3:
#        face_set = 0
#        fcounter = 0
#        faces = face_cascade.detectMultiScale( gray )
#        if str(len(faces))!=0:
#            print "Found " + str( len( faces ) ) + " face(s)"
#            str_face=str(len(faces))
#            int_face=int(str_face)
#            print (int_face,type(face_set))
#            if int_face!=0:
#                 camera.capture('face.jpg')
#                 print "Searching......"
#                 (a,b)=search()
#                 c=float(a)
#                 d=b
#                 print d,type(d)
#                 if c>86:
#                         id="8a503c25065b44f8532a0e893e9b1c03"
#                         id1="319dd19c19bae5abe5d4dd4d85f57f1d"
#                         id2="b50f514a3a58d800cdf16c4875799282"
#                         if d==id:
#                             name="shuai qing"
#                             print "I know him(her):  ",name
#                         if d==id1:
#                             name="shuai lin"
#                            print "I know him(her):  ",name
#                         if d==id2:
#                             name="shuai bo"
#                             print "I know him(her):  ",name
#                
#                 else:
#                     print "He(She) is a stranger"
#                     send()
#                 time.sleep(5)
#                 
#                 #
#                # print (a,b)
#                #face_set = 1
#           # else:
#               # face_set = 0
#        for ( x, y, w, h ) in faces:
#            cv2.rectangle( frame, ( x, y ), ( x + w, y + h ), ( 0,0, 255 ), 2 )
#    	    cv2.putText( frame, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )
#
#    fcounter += 1 

   
    #################################################
    # capture the motion ############################	   
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
   # print frameDelta
    
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
    cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
#    print (_,cnts,_)
#    print "\n"
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"]:
            continue
#        print cv2.boundingRect
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        text = "Occupied"
 
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)
    if text == "Occupied":
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            motionCounter += 1
 
            if motionCounter >= conf["min_motion_frames"]:

		camera.capture('image.jpg')
               # if face_set == 1:
                 #   camera.capture('face.jpg')
########################################
                   # creat_faceid()
                  #  print "Searching......"
                   # creat_faceid()
                   # time.sleep(5)
                   # faceID=faceid
                   # print faceID


########################################
                lastUploaded = timestamp
                motionCounter = 0
 
    else:
        motionCounter = 0
    if conf["show_video"]:
        cv2.imshow("Security Feed", frame)
        amp=0xFF
        key = cv2.waitKey(1) &amp
 
        if key == ord("q"):
            break
 
        rawCapture.truncate(0) 
