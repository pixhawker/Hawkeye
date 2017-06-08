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
import re
import urlparse



###################################################

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
    help="path to the JSON configuration file")
args = vars(ap.parse_args())
warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))

###################################################




### Setup #####################################################################


camera = PiCamera()
camera.resolution = tuple(conf["resolution"])
camera.framerate = conf["fps"]
rawCapture = PiRGBArray(camera, size=tuple(conf["resolution"]))
face_cascade = cv2.CascadeClassifier( '/home/pi/opencv-3.1.0/data/lbpcascades/lbpcascade_frontalface.xml' )
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
t_start = time.time()
fps = 0
fatal=0
number=0
### Helper Functions ##########################################################


def get_faces( img ):

    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    faces = face_cascade.detectMultiScale( gray )
    
    return faces, img

def draw_frame( img, faces ):
   # global camera 
   # global camera.resolution
   # global camera.framerate
    global xdeg
    global ydeg
    global fps
    global time_t

    # Draw a rectangle around every face
    for ( x, y, w, h ) in faces:

        cv2.rectangle( img, ( x, y ),( x + w, y + h ), ( 0, 0, 255 ), 2 )
        cv2.putText(img, "Face No." + str( len( faces ) ), ( x, y ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 )

    # Calculate and show the FPS
    fps = fps + 1
    sfps = fps / (time.time() - t_start)
    cv2.putText(img, "FPS : " + str( int( sfps ) ), ( 10, 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.5, ( 0, 0, 255 ), 2 ) 

    cv2.imshow( "Frame", img )
    cv2.waitKey( 1 )
  

### Main ######################################################################

if __name__ == '__main__':

    pool = mp.Pool( processes=4 )
    fcount = 0
    
    camera.capture( rawCapture, format="bgr" )  

    r1 = pool.apply_async( get_faces, [ rawCapture.array ] )    
    r2 = pool.apply_async( get_faces, [ rawCapture.array ] )    
    r3 = pool.apply_async( get_faces, [ rawCapture.array ] )    
    r4 = pool.apply_async( get_faces, [ rawCapture.array ] )    

    f1, i1 = r1.get()
    f2, i2 = r2.get()
    f3, i3 = r3.get()
    f4, i4 = r4.get()
  #  if str(len(f1))!=0:
  #          print "Found " + str( len( f1 ) ) + " face(s)"
    
    rawCapture.truncate( 0 )    

    for f in camera.capture_continuous( rawCapture, format="bgr", use_video_port=True ):
        frame = f.array
        timestamp = datetime.datetime.now()
        text = "Unoccupied"
 
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
        if  fcounter==3:
            fcounter=0
            cv2.accumulateWeighted(gray, avg, 0.5)
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
            thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
                cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            (_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
 
            for c in cnts:
        # if the contour is too small, ignore it
                if cv2.contourArea(c) < conf["min_area"]:
                    continue
  
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
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
                   # if conf["use_dropbox"]:
                    # write the image to temporary file
                   # t = TempImage()
                   # cv2.imwrite(t.path, frame)
 
                    #print "[UPLOAD] {}".format(ts)
                   # path = "{base_path}/{timestamp}.jpg".format(
                    #    base_path=conf["dropbox_base_path"], timestamp=ts)
                   # client.put_file(path, open(t.path, "rb"))
                   # t.cleanup()
                        camera.capture('/home/pi/Pictures/shareall/motion.jpg')

                        lastUploaded = timestamp
                        motionCounter = 0
 
            else:
                motionCounter = 0 
        fcounter += 1
  #      print fcounter   
    #######################################
       # image = imutils.resize(image, width=500)
       # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
       # gray = cv2.GaussianBlur(gray1, (21, 21), 0)
       # if avg is None:
       #     print "[INFO] starting background model..."
       #     avg = gray.copy().astype("float")
       #     rawCapture.truncate(0)
       #     continue

        if   fcount == 1:
            r1 = pool.apply_async( get_faces, [ frame ] )
           # print r1
            f2, i2 = r2.get()
            draw_frame( i2, f2 )
            if str(len(f2))!=0:
                print "Found " + str( len( f2 ) ) + " face(s)"
            str_face=str(len(f2))
            int_face=int(str_face)
            print (int_face,type(face_set))
            if int_face!=0:
       #          fatal=1
                 camera.capture('/home/pi/Pictures/shareall/face.jpg')
              #   number=number+1
              #   if number>10:
              #      number=0
    # Draw a rectangle around every face

        
    # Calculate and show the FPS
                 print "Searching......"
                 time.sleep(2)
                # geshi=search
                 (a,b)=search()
               #  geshi=search()
                 print (a,b)
               #  geshi_str= geshi.__str__()
               #  print geshi_str,type(geshi_str)
               #  if len(geshi_str)<=10:
                    
            #     if type(geshi)!=tuple:
                #    print "Wrong"
                    
              #   else:
              #      print "Right"
                    
                 c=float(a)
                 d=b
                 print d,type(d)
                 if c>80:
                         id="8a503c25065b44f8532a0e893e9b1c03"
                         id1="319dd19c19bae5abe5d4dd4d85f57f1d"
                         id2="b50f514a3a58d800cdf16c4875799282"
                         if d==id:
                             name="shuai qing"
                             print "I know him(her):  ",name
                         if d==id1:
                             name="shuai lin"
                             print "I know him(her):  ",name
                         if d==id2:
                             name="shuai bo"
                             print "I know him(her):  ",name


                 else:
                     print "He(She) is a stranger"
                    # send()
        elif fcount ==3:
            r2= pool.apply_async( get_faces, [ frame ] )
            f3, i3 = r3.get()
            draw_frame( i3, f3 )
            if fatal==1:
               time.sleep(1)

        elif fcount ==5:
            r3 = pool.apply_async( get_faces, [ frame ] )
            f4, i4 = r4.get()
            draw_frame( i4, f4 )
            if fatal==1:
               time.sleep(1)

        elif fcount ==7:
            r4 = pool.apply_async( get_faces, [ frame ] )
            f1, i1 = r1.get()
            draw_frame( i1, f1 )
            if fatal==1:
                time.sleep(1)
           # if fcount in range(1,5):
            #   
            #    if conf["show_video"]:
            #         cv2.imshow("Security Feed", img)
            #         amp=0xFF
            #         key = cv2.waitKey(1) &amp

                   # if key == ord("q"):
                 #       break

            fcount = 0

        fcount += 1
     #   if conf["show_video"]:
     #       cv2.imshow("Security Feed", frame)
     #       amp=0xFF
     #       key = cv2.waitKey(1) &amp#

     #       if key == ord("q"):
     #           break
        rawCapture.truncate( 0 )
