import cv2


#Capture video from webcam. 
cap = cv2.VideoCapture(2)

#Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

minX = 1
maxX = 180
minY = 1
maxY = 180
x_Range = maxX-minX
y_Range = maxY-minY

x_Pos = 0.0
y_Pos = 0.0

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
        y_Pos = (y + h/2) 
        break

    motor_x = x_Pos/width * x_Range + minX
    motor_y = y_Pos/width * y_Range + minY



    #Display image
    cv2.imshow('frame', frame)
