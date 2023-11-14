#import in necessary thing - openCV for camera, sleep and RPi.GPIO for controlling the motors
#numpy for QoL
import cv2
from time import sleep
import RPi.GPIO as GPIO
import numpy as np

#gives the bounds that indicate the color of rust
lower_red = np.array([0, 50, 50])
upper_red = np.array([100, 255, 255])

#begin vide capture, will be used to take one image
cam = cv2.VideoCapture(0)

def getInitialRust():
   
    print("GETTING INITIAL VALUE")
    #begin vide capture, will be used to take one image
   
    #before getting an image, the camera must be prepped, because it adjusts lighting
    #to do this, we must let it take some frames for some time. It uses this time to
    #adjust the lighting and things.
    loopNum = 0
    frame = None
   
    #this section scans 50 frames, which is enough time to let the camera adjust its settings
    #then it takes the 50th frame, and stores it in the "frame" variable
    while loopNum < 50:
        _, frame = cam.read()
        loopNum += 1
       
        if cv2.waitKey(1) == ord("w"):
            break
       
       
   
    #if camera is unable to take picture, through error
    if not cam.isOpened():
        print("ERROR: CAMERA NOT WORKING")
        exit()
   
    #creates a mask using the specified rust colors. does this by
    #scanning each pixel of the image to determine whether the rgb
    #values lie between them. Then it takes the size of the original
    #frame and stores it
    mask = cv2.inRange(frame, lower_red, upper_red)
    width, length, channels = frame.shape
   
    #counts the number of pixels that falls between the range of rust
    #colors and uses the size of the frame to calculate percentage of
    #the image that is rust colored
    numHighlighted = cv2.countNonZero(mask) / (width * length)
   
   
    #clean up
    #returns the number of highlighted pixels
    return numHighlighted


#variable for determining the amount of rust on screen at the start
startRust = getInitialRust()


def main():
    print("STARTING RUST AMOUNT: ", startRust)
   
    while not checkFrame(startRust, 50):
        sleep(10)
       
    cam.release()
    cv2.destroyAllWindows()
       
    moveMotor(1, 3, 100)
   
    sleep(15)
   
    moveMotor(2, 5, 80)
   
def moveMotor(motorNum, sleepTime, motorPower):
   
    #set motor variable
    motorPin = None
   
    #if motor number is one, use gate motor. if two, use basketMotor
    if motorNum == 1:
        motorPin = 32
    else:
        motorPin = 33
   
    #GPIO (General purpose input output) set up on RPi
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(motorPin, GPIO.OUT)
   
    #set motorPin variable to a frequency of 1000, and set duty cycle to
    #given amount in parameters
    motorPin = GPIO.PWM(motorPin, 1000)
    motorPin.start(motorPower)
   
    #let the motor run for provided amount of time in paramters
    sleep(sleepTime)
   
    #clean up
    motorPin.stop()
    GPIO.cleanup()
   
   
   
def checkFrame(basis, percentageWanted):
   
    print("CHECKING FRAME")
   
   
    #before getting an image, the camera must be prepped, because it adjusts lighting
    #to do this, we must let it take some frames for some time. It uses this time to
    #adjust the lighting and things.
    loopNum = 0
    frame = None
   
    #this section scans 50 frames, which is enough time to let the camera adjust its settings
    #then it takes the 50th frame, and stores it in the "frame" variable
    while loopNum < 50:
        _, frame = cam.read()
        loopNum += 1
        print(loopNum)
       
        if cv2.waitKey(1) == ord("w"):
            break
       
       
    #if camera is unable to take picture, through error
    if not cam.isOpened():
        print("ERROR: CAMERA NOT WORKING")
        exit()
   
    #creates a mask using the specified rust colors. does this by
    #scanning each pixel of the image to determine whether the rgb
    #values lie between them. Then it takes the size of the original
    #frame and stores it
    mask = cv2.inRange(frame, lower_red, upper_red)
    width, length, channels = frame.shape
   
    #counts the number of pixels that falls between the range of rust
    #colors and uses the size of the frame to calculate percentage of
    #the image that is rust colored
    numHighlighted = cv2.countNonZero(mask) / (width * length)
    print(numHighlighted)
    #clean up
   
   
    #check to see whether the new scanned amount is less than the initial
    #scanned amount. Does this by getting the percentage of size difference
    #between the current scanned amount and the initial scanned amount
    #then it checks to see if this percentage falls in between the given range
    #if it does, return true, else, return false
    if ((numHighlighted / basis) * 100 < percentageWanted):
        return True
   
    return False


main()
