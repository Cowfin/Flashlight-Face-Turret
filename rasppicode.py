import cv2
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
servoX = GPIO.PWM(11,50)
servoY = GPIO.PWM(13,50)

servoX.start(0)
servoY.start(0)

#Load the facial detection cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Capture video from webcam. 
cap = cv2.VideoCapture(0)

#Wait 1 second
time.sleep(1)

#Converts coordinates on screen into degrees
def Convert_Coordinates(x,y,width,height):
    motor_x = (180.0/(width/(x+0.001)))
    motor_y = (180.0/(height/(y+0.001)))
    return motor_x, motor_y


#Converts degrees to DutyCycle value
def Convert_Angle(angle):
    dutycycle = 2+(angle/18)
    return dutycycle

while True:
    x_pos = 0.0
    y_pos = 0.0
    _, frame = cap.read()
    height, width, _ = frame.shape

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Draw the rectangle around one main face
    for (x, y, w, h) in faces:
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        x_pos = (x + (w/2))
        y_pos = (y + (h/2))
        break

    #print('X:' + str(x_pos) + '  Y:' + str(y_pos))
    #Draw a dot where the center of the face is
    cv2.circle(frame,(int(x_pos),int(y_pos)),2,(0,255,0),-1)

    #Convert all X & Y values into their respective values
    #print('motorX:' + str(motor_x) + '  motorY:' + str(motor_y))
    motor_x,motor_y = Convert_Coordinates(x_pos,y_pos,width,height)
    servoX.ChangeDutyCycle(Convert_Angle(motor_x))
    servoY.ChangeDutyCycle(Convert_Angle(motor_y))
    time.sleep(0.5)
    
    #Display image
    cv2.imshow('frame', frame)

    #Stop when escape key pressed
    k = cv2.waitKey(30)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows
servoX.stop()
servoY.stop()
GPIO.cleanup()