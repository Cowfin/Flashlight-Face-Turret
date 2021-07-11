import cv2
import RPi.GPIO as GPIO
import time

def Convert_Angle(angle):
    dutycycle = 2+(angle/18)
    return dutycycle

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servoX = GPIO.PWM(11,50)
servoY = GPIO.PWM(13,50)

#Capture video from webcam. 
cap = cv2.VideoCapture(0)

#Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

minX = 0
maxX = 45
minY = 120
maxY = 155
x_Range = maxX-minX
y_Range = maxY-minY

servoX.start(Convert_Angle(minX))
servoY.start(Convert_Angle(minY))

x_Pos = 0.0
y_Pos = 0.0

time.sleep(1)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)  #mirror the image
    height, width, _ = frame.shape

    centerH = height//2
    centerW = width//2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        #Draw the rectangle around each face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #Draw a dot where the center of the face is
        cv2.circle(frame,(int(x+w/2),int(y+h/2)),2,(0,255,0),-1)
        x_Pos = (x + w/2)
        y_Pos = height - (y + h/2)
        break

    motor_x = x_Pos/width * x_Range + minX
    motor_y = y_Pos/height * y_Range + minY

    servoX.ChangeDutyCycle(Convert_Angle(motor_x))
    servoY.ChangeDutyCycle(Convert_Angle(motor_y))
    

    #Display image
    cv2.imshow('frame', frame)
    
    #Stop if escape key is pressed
    k = cv2.waitKey(30)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows
servoX.stop()
servoY.stop()
GPIO.cleanup()