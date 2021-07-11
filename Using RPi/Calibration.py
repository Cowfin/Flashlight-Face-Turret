import cv2
import RPi.GPIO as GPIO
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

def window_maker(name, w,h):
    cv2.namedWindow("Calibrate")
    cv2.createTrackbar("MotorX",name,0,w,nothing)
    cv2.createTrackbar("MotorY",name,0,h,nothing)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servoX = GPIO.PWM(11,50)
servoY = GPIO.PWM(13,50)

servoX.start(0)
servoY.start(0)

cap = cv2.VideoCapture(2)

x_Pos = 0.0
y_Pos = 0.0
window = "Calibrate"

window_maker(window,180,180)

while True:
    _, frame = cap.read()
    height, width, _ = frame.shape

    motor_Value = np.array([cv2.getTrackbarPos("MotorX",window),cv2.getTrackbarPos("MotorY",window)])

    servoX.ChangeDutyCycle(Convert_Angle(motor_Value[0]))
    servoY.ChangeDutyCycle(Convert_Angle(motor_Value[1]))

    cv2.imshow(window, frame)
    
    k = cv2.waitKey(30)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows