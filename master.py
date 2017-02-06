from simple_contour import area_detector
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from motorcontrol import *
from LineSensor import LineSensor

def direction_adjustment(left, right, turningmotor, turned_left, turned_right):
    # check line sensor data and adjust accordingly
    if left.check() == True and right.check() == False:
        turningmotor.move(1)
        time.sleep(.05)
        turningmotor.stop()
        return True, False
    elif left.check() == False and right.check() == True:
        turningmotor.move(0)
        time.sleep(.05)
        turningmotor.stop()
        return False, True
    else:
        if turned_left:
            turningmotor.move(0)
            time.sleep(.05)
            turningmotor.stop()
        elif turned_right:
            turningmotor.move(1)
            time.sleep(.05)
            turningmotor.stop()
        return False, False
    

def travel(destination, drive_forward, drive_backward, turn_forward, turn_backward):
    # allow the camera to warmup
    time.sleep(0.1)

    turningmotor = Motor(turn_forward, turn_backward, 22)
    drivemotor = Motor(drive_forward, drive_backward, 23)

    left = LineSensor(11)
    right = LineSensor(13)
    turned_left = False
    turned_right = False
    drivemotor.move(1)
                                                                                            
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # grab the raw NumPy array representing the image
        image = frame.array
        
        #convert the image to Hue Saturation Value format
        hsv = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only the color of destination
        mask = cv2.inRange(hsv, destination[0], destination[1])
        
        presence=area_detector(mask)

        if presence:
            drivemotor.stop()
            print "I have arrived"
            break

        #check the frame to make sure you haven't reached the end of the hallway
        mask_stop = cv2.inRange(hsv, rooms["stop"][0], rooms["stop"][1])
        presence_stop=area_detector(mask_stop)
        if presence_stop:
            drivemtoor.stop()
            GPIO.cleanup()
            GPIO.setmode(GPIO.BOARD)
            travel(destination, drive_backward, drive_forward, turn_backward, turn_forward)
            break
        
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        turned_left, turned_right = direction_adjustment(left, right, turningmotor, turned_left, turned_right)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

GPIO.setmode(GPIO.BOARD)

rooms = {}
rooms['start'] = [np.array([129, 0, 138]), np.array([179, 255, 255])] #purple
rooms['A'] = [np.array([129, 0, 138]), np.array([179, 255, 255])] #yellow
rooms['B'] = [np.array([129, 0, 138]), np.array([179, 255, 255])] #green         
rooms['C'] = [np.array([129, 0, 138]), np.array([179, 255, 255])] #blue
rooms['stop'] = [np.array([129, 0, 138]), np.array([179, 255, 255])] #red 

drive_forward, drive_backward, turn_forward, turn_backward = 19, 21, 36, 38

command = raw_input("Which room would you like me to come to? A, B or C? ")
destination = rooms[command]
travel(destination, drive_forward, drive_backward, turn_forward, turn_backward)

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

return_command = raw_input("Type yes to confirm that you have taken your snack: ")
if return_command == "yes":
    destination = rooms["start"]
travel(destination, drive_backward, drive_forward, turn_backward, turn_forward) 

            
