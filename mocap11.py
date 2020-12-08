"""
Author - Simon Sprouse 11/2020

-create images from webcam - done
-create window for the image - done
-track limbs
-do math
-display measurements on screen
-record angles in a log
-sound the alarm
-close the loop with a key

"""

import cv2
from colr import color
import numpy

cap = cv2.VideoCapture(0)

#Create windows
cv2.namedWindow('Trackbars')
cv2.namedWindow('Color1')
cv2.namedWindow('Color2')
cv2.namedWindow('Color3')
cv2.namedWindow('Color4')

cv2.resizeWindow('Trackbars',500,200)

cv2.createTrackbar('Range1', 'Trackbars', 30, 255, lambda x:None)
cv2.createTrackbar('Range2', 'Trackbars', 30, 255, lambda x:None)
cv2.createTrackbar('Range3', 'Trackbars', 30, 255, lambda x:None)
cv2.createTrackbar('Range4', 'Trackbars', 30, 255, lambda x:None)



def colorPrint(bgr):
    print(color("Blue = ", fore = (bgr[2], bgr[1], bgr[0]), back = 0), 
              color(bgr[0],fore = (bgr[2], bgr[1], bgr[0]), back = 0),
              color("Green = ", fore = (bgr[2], bgr[1], bgr[0]), back = 0),
              color(bgr[1], fore = (bgr[2], bgr[1], bgr[0]), back = 0),
              color("Red = ", fore = (bgr[2], bgr[1], bgr[0]), back = 0),
              color(bgr[2], fore = (bgr[2], bgr[1], bgr[0]), back = 0))
    
"""
Left click applies the range, Right click removes the range
"""

def mouseClick1(event, x, y, flags, params):
    
    global c1_lower, c1_middle, c1_upper, applyRange1
    
    if event == cv2.EVENT_LBUTTONDOWN: 
        bgr = frame[ y, x]
        colorPrint(bgr)    
        c1_middle = [bgr[0],bgr[1],bgr[2]]
        applyRange1 = True
     
    elif event == cv2.EVENT_RBUTTONDOWN:  
        c1_lower = [0,0,0]
        c1_upper = [255,255,255]
        applyRange1 = False
        
def mouseClick2(event, x, y, flags, params):
    
    global c2_lower, c2_middle, c2_upper, applyRange2
    
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr = frame[ y, x]
        colorPrint(bgr)
        c2_middle = [bgr[0],bgr[1],bgr[2]]
        applyRange2 = True

    elif event == cv2.EVENT_RBUTTONDOWN:       
        c2_lower = [0,0,0]
        c2_upper = [255,255,255]
        applyRange2 = False

def mouseClick3(event, x, y, flags, params):
    
    global c3_lower, c3_middle, c3_upper, applyRange3
    
    if event == cv2.EVENT_LBUTTONDOWN: 
        bgr = frame[ y, x]
        colorPrint(bgr)
        c3_middle = [bgr[0],bgr[1],bgr[2]]
        applyRange3 = True
        
    elif event == cv2.EVENT_RBUTTONDOWN:       
        c3_lower = [0,0,0]
        c3_upper = [255,255,255]
        applyRange3 = False
        
def mouseClick4(event, x, y, flags, params):
    
    global c4_lower, c4_middle, c4_upper, applyRange4
    
    if event == cv2.EVENT_LBUTTONDOWN:      
        bgr = frame[ y, x]
        colorPrint(bgr)
        c4_middle = [bgr[0],bgr[1],bgr[2]]
        applyRange4 = True
        
    elif event == cv2.EVENT_RBUTTONDOWN:   
        c4_lower = [0,0,0]
        c4_upper = [255,255,255]
        applyRange4 = False

"""
This function caps the upper and lower limits in case the range is too high.
If the range puts the upper limit above 255, it's reset to 255
If the range puts the lower limit below 0, it's reset to 0
"""

def colorCap(lower,middle,upper,margin):
    
    
    #loop repeats for each bgr value
    for i in range(0,3):
    
        #if the range exceeds 255 it gets capped
        if middle[i] + margin > 255:
            upper[i] = 255
            
        elif middle[i] + margin <= 255:
            upper[i] = (middle[i] + margin)
         
        #if the range drops below 0 it gets bottomed
        if middle[i] - margin < 0:
            lower[i] = 0 
            
        elif middle[i] - margin >= 0:
            lower[i] = (middle[i] - margin)
       
    return lower, upper



#Call the mouse function
cv2.setMouseCallback('Color1', mouseClick1, param = None)
cv2.setMouseCallback('Color2', mouseClick2, param = None)
cv2.setMouseCallback('Color3', mouseClick3, param = None)
cv2.setMouseCallback('Color4', mouseClick4, param = None)


#Random stuff to make the loop work
c1_lower = [0,0,0]
c1_upper = [255,255,255]
c2_lower = [0,0,0]
c2_upper = [255,255,255]
c3_lower = [0,0,0]
c3_upper = [255,255,255]
c4_lower = [0,0,0]
c4_upper = [255,255,255]
applyRange1 = False
applyRange2 = False
applyRange3 = False
applyRange4 = False
keypressed = 1


#loop to mask the paint chips
while keypressed != 27:
    
    
    #varibales for trackbar position
    range1 = cv2.getTrackbarPos('Range1','Trackbars')
    range2 = cv2.getTrackbarPos('Range2','Trackbars')
    range3 = cv2.getTrackbarPos('Range3','Trackbars')
    range4 = cv2.getTrackbarPos('Range4','Trackbars')
    
    
    #if leftmouse is clicked the range is applied
    if applyRange1 == True:
       
       c1_range = colorCap(c1_lower,c1_middle,c1_upper,range1)
       c1_lower = c1_range[0]
       c1_upper = c1_range[1]
    
    if applyRange2 == True:
        
       c2_range = colorCap(c2_lower,c2_middle,c2_upper,range2)
       c2_lower = c2_range[0]
       c2_upper = c2_range[1]
   
    if applyRange3 == True:
        
       c3_range = colorCap(c3_lower,c3_middle,c3_upper,range3)
       c3_lower = c3_range[0]
       c3_upper = c3_range[1]
   
    if applyRange4 == True:
        
       c4_range = colorCap(c4_lower,c4_middle,c4_upper,range4)
       c4_lower = c4_range[0]
       c4_upper = c4_range[1]
    
   
    
    #Reformat lists as numpy arrays
    c1_lower = numpy.array(c1_lower, dtype = "uint8")
    c1_upper = numpy.array(c1_upper, dtype = "uint8")
    c2_lower = numpy.array(c2_lower, dtype = "uint8")
    c2_upper = numpy.array(c2_upper, dtype = "uint8")
    c3_lower = numpy.array(c3_lower, dtype = "uint8")
    c3_upper = numpy.array(c3_upper, dtype = "uint8")
    c4_lower = numpy.array(c4_lower, dtype = "uint8")
    c4_upper = numpy.array(c4_upper, dtype = "uint8")
    
    
    #creates image variable
    ret, frame = cap.read() 
    
    
    #creates masks
    c1_mask = cv2.inRange(frame, c1_lower, c1_upper)    
    c2_mask = cv2.inRange(frame, c2_lower, c2_upper)
    c3_mask = cv2.inRange(frame, c3_lower, c3_upper)
    c4_mask = cv2.inRange(frame, c4_lower, c4_upper)
    
    
    #applies the masks to frame 
    c1_filtered = cv2.bitwise_and(frame, frame, mask = c1_mask)
    c2_filtered = cv2.bitwise_and(frame, frame, mask = c2_mask)
    c3_filtered = cv2.bitwise_and(frame, frame, mask = c3_mask)
    c4_filtered = cv2.bitwise_and(frame, frame, mask = c4_mask)
    
    
    #display images
    cv2.imshow('Color1', c1_filtered)
    cv2.imshow('Color2', c2_filtered)
    cv2.imshow('Color3', c3_filtered)
    cv2.imshow('Color4', c4_filtered)
    
    keypressed = cv2.waitKey(30)



cap.release()
cv2.destroyWindow('Color1')
cv2.destroyWindow('Color2')
cv2.destroyWindow('Color3')
cv2.destroyWindow('Color4')
cv2.destroyWindow('Trackbars')

"""
░░░░░░░░░░░░░░░░▄▄▄███████▄▄░░░░░░░░░░░░
░░░░░░░░░░░░░░▄███████████████▄░░░░░░░░░
░░░░░░░░░░░░░█▀▀▀▄░░░░█████▀▀███▄░░░░░░░
░░░░░░░░░░░░█░░▄░░█▄▄█░░░░▀▄▄█████░░░░░░
░░░░░░░░░▄▀▀▀▄▄▀▀▀▀▀▀▄░░▀░░█▀▀▀░▀██░░░░░
░░░░░░░▄▀░░░░░█░░░░░░▀▄▄▄▄█░░░░░░░▀▄░░░░
░░░░░░▄▀░░░░░▄█▀▄▄▄▄░░░░░▄░░░░░░░░░█░░░░
░░░░░░█░░░░░▄█▀▄▄▄▄▄▄▄▄▄▀▀░░░░░░░░░▀▄░░░
░░░░░█░░░░░░▀█▄░░░░░░░░░░░░░░░░░░░░░█░░░
░░░░░█░░░░░░░░▀▄░░░░░░░░░░░░░░░░░░░░█░░░
░░░░░█░░░░░░░░▄█░░░░░░░░░░░░░░░░░░░░█░░░
░░░░░█░░░░░░▄▀░░░░░░░░▀▄░░░░░░░░░░░░█░░░
░░░░░█░░░░░░▀▄░░░▄░░░░░█░░░░░░░░░░░░█░░░
░░░░░█░░░░░░░░▀▀▀▀▀█▄▄▀░░░░░░░░░░░░░█░░░
░░░░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▄██░░
░░░░░█▄░░░░░░░░░░░░░░░░░░░░░░░░░░▄▀▀▄▀▄▄
░░░░▄█▀▄░░░░░░░░░░░░░░░░░░░░░░▄▄▀░░▄▀░░░
░▄░▀░░█░▀▄▄░░░░░░░░░░░░░░░▄▄▄▀░░░▄▀░░░░░
▀░░░░░░▀▄░░▀▄░░░░░░░░▄▄▄▀▀░░░░▄▀▀░░░░░░░

"""
