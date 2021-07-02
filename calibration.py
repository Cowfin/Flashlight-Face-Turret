import cv2
import RPi.GPIO as GPIO
import time

def nothing(x):
    pass

def Convert_Angle(angle):
    dutycycle = 2+(angle/18)
    return dutycycle

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servoX = GPIO.PWM(11,50)
servoY = GPIO.PWM(13,50)

servoX.start(0)
servoY.start(0)

cap = cv2.VideoCapture(0)

cv2.namedWindow("Calibrate")
cv2.createTrackbar("X","Hold",0,180,nothing)
cv2.createTrackbar("Y","Hold",0,180,nothing)

while True:
    yes = 1

cap.release()
cv2.destroyAllWindows