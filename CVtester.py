from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from motorcontrol import *

pi = 3.14159265
def area_detector(image):
    contours, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 1000
    for contour in contours:
        contour_area = cv2.contourArea(contour)
        if contour_area > min_contour_area and is_circle(contour, contour_area):
            return True
    return False

def is_circle(contour, contour_area):
    if (get_circle_area(contour) / contour_area - 1) < .5:
        return True
    return False

def get_circle_area(contour):
    (x, y), radius = cv2.minEnclosingCircle(contour)
    circle_area = pi * radius ** 2
    return circle_area

 # initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, np.array([129, 0, 138]), np.array([179, 255, 255]))
    
    presence=area_detector(mask)

    cv2.imshow("Frame", image)
    cv2.imshow("Mask", mask)
    
    print presence
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
