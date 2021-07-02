import cv2
#import RPi.GPIO as GPIO
import time
import numpy as np

def nothing(x):
    pass

def Convert_Coordinates(x,y,width,height):
    motor_x = (180.0/(width/(x+0.001)))
    motor_y = (180.0/(height/(y+0.001)))
    return motor_x, motor_y

def Convert_Angle(angle):
    dutycycle = 2+(angle/18)
    return dutycycle

'''GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servoX = GPIO.PWM(11,50)
servoY = GPIO.PWM(13,50)

servoX.start(0)
servoY.start(0)'''

cap = cv2.VideoCapture(0)


def window_maker(w,h):
    cv2.namedWindow("Calibrate")
    cv2.createTrackbar("MotorX","Axis",0,w,nothing)
    cv2.createTrackbar("MotorY","Axis",0,h,nothing)
    cv2.createTrackbar("BLX","Axis",0,w,nothing)
    cv2.createTrackbar("BLY","Axis",0,h,nothing)
    cv2.createTrackbar("TLX","Axis",0,w,nothing)
    cv2.createTrackbar("TLY","Axis",0,h,nothing)
    cv2.createTrackbar("BRX","Axis",0,w,nothing)
    cv2.createTrackbar("BRY","Axis",0,h,nothing)
    cv2.createTrackbar("TRX","Axis",0,w,nothing)
    cv2.createTrackbar("TRY","Axis",0,h,nothing)

while True:
    _, frame = cap.read()
    height, width, _ = frame.shape

    window_maker(width,height)

    motor_Value = np.array([cv2.getTrackbarPos("MotorX","Axis"),cv2.getTrackbarPos("MotorY","Axis")])
    bottom_Left = np.array([cv2.getTrackbarPos("BLX","Axis"),cv2.getTrackbarPos("BLY","Axis")])
    top_Left = np.array([cv2.getTrackbarPos("TLX","Axis"),cv2.getTrackbarPos("TLY","Axis")])
    bottom_Right = np.array([cv2.getTrackbarPos("BRX","Axis"),cv2.getTrackbarPos("BRY","Axis")])
    top_Right = np.array([cv2.getTrackbarPos("TRX","Axis"),cv2.getTrackbarPos("TRY","Axis")])

    #servoX.ChangeDutyCycle(Convert_Angle(motor_Value[0]))
    #servoY.ChangeDutyCycle(Convert_Angle(motor_Value[1]))

    print("mX: " + motor_Value[0] + " mY:" + motor_Value[1])

    k = cv2.waitKey(30)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows