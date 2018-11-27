# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 05:11:04 2018

@author: James Bounds
"""

import cv2
import numpy as np
#import matplotlib.pyplot as plt
import sys
import time

#Good for detecting slower motion
rigorous = True

#Comparison to previous frame
THREASH1 = 0.003
#Comparison to last saved frame
THREASH2 = 0.0075
#Noise rejection
TOLERANCE = 85

#Interval (seconds) to record background images
BG_INTERVAL = 5

showFrames = False

outputFolder = 'c:/path/to/folder/'
outputIndex = 0
bgIndex = 0

for i in range(1,len(sys.argv)):
    if(sys.argv[i]=='--show-frames'):
        print("Camera Window enabled")
        showFrames = True

if(showFrames):
    cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
print("Camera Device Successfully opened")

vc.set(28,125)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
if(showFrames):
    cv2.imshow("preview",frame)
    
print("Successful grab from camera")
stillFrame = frame
timeStart = time.time()
time_lastAcq = timeStart

#--------Begin Main loop-------------
while rval:
    rval, newFrame = vc.read()
    if(showFrames):
        key = cv2.waitKey(1)
#    if key == 27: # exit on ESC
#        break
    #--------Motion detection----------
    frameDiff_sqr = (frame - newFrame)**2
    frameDiff_sqr[frameDiff_sqr < TOLERANCE] = 0
    stillDiff_sqr = (stillFrame-newFrame)**2
    stillDiff_sqr[stillDiff_sqr < TOLERANCE] = 0
    if(outputIndex < 100 or not rigorous and np.mean(frameDiff_sqr)/np.mean(newFrame) > THREASH1
        or rigorous and np.mean(stillDiff_sqr)/np.mean(newFrame) > THREASH2):
        if(showFrames):    
            cv2.imshow("preview", newFrame)
        cv2.imwrite(outputFolder + str(outputIndex) + '.png', newFrame)
        outputIndex += 1
        print("Captured %d frames" % outputIndex)
        stillFrame=frame
        time_lastAcq = time.time()
    elif(int(time.time()-time_lastAcq) > BG_INTERVAL ):
        cv2.imwrite(outputFolder + "bgFrame_" + str(bgIndex) + ".png",newFrame)
        bgIndex += 1
        print("Background Frame %d at %.1f seconds" % (bgIndex,time.time()-timeStart))
        time_lastAcq = time.time()
    frame = newFrame
        
vc.release()
cv2.destroyWindow("preview")
