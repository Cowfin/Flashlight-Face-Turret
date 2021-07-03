import cv2
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servoX = GPIO.PWM(11,50)
servoY = GPIO.PWM(13,50)

#Converts degrees to DutyCycle value
def Convert_Angle(angle):
    dutycycle = 2+(angle/18)
    return dutycycle

#Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Capture video from webcam. 
cap = cv2.VideoCapture(0)

dX = 90
dY = 90
x_Pos = 0.0
y_Pos = 0.0

servoX.start(dX)
servoY.start(dY)

time.sleep(1)

small_Inc = 2
large_Inc = 10

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
        #Draw the rectangle around the main face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        x_Pos = (x + w//2)
        y_Pos = (y + h//2)
        #Draw a dot where the center of the face is
        cv2.circle(frame,(int(x_Pos),int(y_Pos)),2,(0,255,0),-1)
        break

    if ((x_Pos < (centerW)) & (dX > 0) & (dX < 180)):
        if (abs((x_Pos - centerW)) > 100):
            dX -= large_Inc
        else:
            dX -= small_Inc
    elif((x_Pos > (centerW)) & (dX > 0) & (dX < 180)):
        if (abs((x_Pos - centerW)) > 100):
            dX += large_Inc
        else:
            dX += small_Inc

    if ((y_Pos < (centerH)) & (dY > 0) & (dY < 90)):
        if (abs((y_Pos - centerH)) > 100):
            dY += large_Inc
        else:
            dY += small_Inc
    elif((y_Pos > (centerH)) & (dY > 0) & (dY < 90)):
        if (abs((y_Pos - centerH)) > 100):
            dY -= large_Inc
        else:
            dY -= small_Inc

    if (dX <= 0):
        dX = 1
    elif (dX >= 180):
        dX = 179
        
    if (dY <= 45):
        dY = 1
    elif (dY >= 135):
        dY = 89

    servoX.ChangeDutyCycle(Convert_Angle(dX))
    servoY.ChangeDutyCycle(Convert_Angle(dY))

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