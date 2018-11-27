#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 22:20:50 2018

@author: James Bounds
"""

import os
import cv2
import time

dataDir = 'c:/path/to/folder/'

os.chdir(dataDir)

def getLastFile(fL):
    valMax = -1
    nameOut = None
    for fName in fL:
        try:
            fileInt = int(fName.replace('.png',''))
            if(fileInt > valMax):
                valMax = fileInt
                nameOut = fName
        except:
            continue
    return str(valMax - 1) + '.png'

def watermarkDate(image):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,475)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    
    cv2.putText(img,time.strftime('%H : %M : %S'), bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType )

fileList = os.listdir('.')
N = len(fileList)
haveFrame = False

while True:
    fileList = os.listdir('.')
    Nnew = len(fileList)
    if(Nnew != N):
        fName = getLastFile(fileList)
        img = cv2.imread(fName,1)
        watermarkDate(img)
        cv2.imshow('Last Detected Motion', img)
        cv2.waitKey(1)
        print(fName)
        haveFrame = True
    else:
        if(haveFrame):
            cv2.imshow('Last Detected Motion',img)
        time.sleep(.1)
    N = Nnew
cv2.destroyAllWindows()
