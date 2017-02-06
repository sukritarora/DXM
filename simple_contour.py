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
