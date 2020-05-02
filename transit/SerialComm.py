import serial
import time

ser = serial.Serial('/dev/ttyACM3', 9600)
while 1:
    ser.write(b'3')
    print('311')
    ser.write(b'5')
    print('511')
    time.sleep(1)
    if(ser.in_waiting >0):
        line = ser.readline()
        print(line)
    
        