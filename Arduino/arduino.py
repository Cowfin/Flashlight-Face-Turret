import serial
import time


arduino = serial.Serial('COM5', 9600)

def send(x,y):
    arduino.write(bytes(num,'utf-8'))
    time.sleep(0.05)

while True:
    