#include <Servo.h>

int servoPinX = 9;
int servoPinY = 10;

Servo servoX;
Servo servoY;

void setup(){
    servoX.attach(servoPinX);
    servoY.attach(servoPinY);
    Serial.begin(9600);
}

void loop(){
    servoX.write(0);
    servoY.write(0);
    delay(1000);
    servoX.write(90);
    servoY.write(90);
    delay(1000);
    servoX.write(180);
    servoY.write(180);
    delay(1000);
}
