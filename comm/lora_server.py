import serial

ser = serial.Serial('/dev/ttyAMA2',115200,timeout=0.5)

while True:
    s = ser.readline()
    if(s):
        print(s)