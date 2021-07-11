import cv2
import time
import numpy as np
import pigpio

def nothing(x):
    pass

def Convert_Angle(angle):
    freq = ((angle/180) * 2000) + 500
    return freq

def window_maker(name, w,h):
    cv2.namedWindow("Calibrate")
    cv2.createTrackbar("MotorX",name,0,w,nothing)
    cv2.createTrackbar("MotorY",name,0,h,nothing)

pio = pigpio.pi()

servoX = 17
servoY = 27

pio.set_PWM_frequency(servoX,50)
pio.set_PWM_frequency(servoY,50)

cap = cv2.VideoCapture(0)

x_Pos = 0.0
y_Pos = 0.0
window = "Calibrate"

window_maker(window,180,180)


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    height, width, _ = frame.shape

    motor_Value = np.array([cv2.getTrackbarPos("MotorX",window),cv2.getTrackbarPos("MotorY",window)])

    pio.set_servo_pulsewidth(servoX, Convert_Angle(motor_Value[0]))
    pio.set_servo_pulsewidth(servoY, Convert_Angle(motor_Value[1]))

    cv2.imshow(window, frame)
    
    k = cv2.waitKey(30)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows

