import cv2

def Convert_Coordinates(x,y,width,height):
    motor_x = (180.0/(width/(x+0.001)))
    motor_y = (180.0/(height/(y+0.001)))
    return motor_x, motor_y

#Converts degrees to DutyCycle value
def Convert_Angle(angle):
    dutycycle = 2+(angle/18)
    return dutycycle

#Finds center of face from center of screen
def Find_Distance(cX,cY,x,y):
    rX = -(cX-x)
    rY = -(cY-y)

#Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#Capture video from webcam. 
cap = cv2.VideoCapture(2)

min_X_Angle = 50
max_X_Angle = 110
min_Y_Angle = 50
max_Y_Angle = 100
x_Angle = max_X_Angle - min_X_Angle
y_Angle = max_Y_Angle - min_Y_Angle

center_X = x_Angle/2
center_Y = y_Angle/2


while True:
    x_pos = 0.0
    y_pos = 0.0
    _, frame = cap.read()
    frame = cv2.flip(frame,1)  #mirror the image
    height, width, _ = frame.shape

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    
    for (x, y, w, h) in faces:
        #Draw the rectangle around each face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        #Draw a dot where the center of the face is
        cv2.circle(frame,(int(x+w/2),int(y+h/2)),2,(0,255,0),-1)
        x_Pos = (x + w/2)
        y_Pos = (y + h/2) 
        break

    #print('X:' + str(x_pos) + '  Y:' + str(y_pos))
    

    #print('motorX:' + str(motor_x) + '  motorY:' + str(motor_y))
    motor_x,motor_y = Convert_Coordinates(x_pos,y_pos,width,height)

    
    #Display image
    cv2.imshow('frame', frame)

    #Stop if escape key is pressed
    k = cv2.waitKey(30)
    if k==27:
        break

cap.release()
cv2.destroyAllWindows