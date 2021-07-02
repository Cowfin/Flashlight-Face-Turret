import cv2

#Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#To capture video from webcam. 
#cap = cv2.VideoCapture(0)
#To use a video file as input 
cap = cv2.VideoCapture('video.mp4')

def Convert_Coordinates(x,y,width,height):
    motor_x = (180.0/(width/(x+0.001)))
    motor_y = (180.0/(height/(y+0.001)))
    return motor_x, motor_y

while True:
    x_pos = 0.0
    y_pos = 0.0
    _, frame = cap.read()
    height, width, _ = frame.shape

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    #Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        x_pos = (x + (w/2))
        y_pos = (y + (h/2))
        break

    #print('X:' + str(x_pos) + '  Y:' + str(y_pos))
    #Draw a dot where the center of the face is
    cv2.circle(frame,(int(x_pos),int(y_pos)),2,(0,255,0),-1)

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