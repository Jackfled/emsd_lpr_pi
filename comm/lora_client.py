import serial
import time
# import logging
from models.logger import Logger

log = Logger('log/lorawan.log', level='debug').logger

# logging.basicConfig(filename="log.txt", level=logging.DEBUG)
def connect():
    # return None
    try:
        #ser = serial.Serial('/dev/ttyAMA2',115200,timeout=0.5) 
        log.debug("opening /dev/ttyACM0")
        ser = serial.Serial('/dev/ttyACM0',115200,timeout=1.0) # USB-Serial Connection (By Akyas)
    #    ser.write("Serial Success\n".encode())
        
        return ser

    except BaseException as err:
        log.error(err)

    try:
        log.debug("opening /dev/ttyACM1")
        #ser = serial.Serial('/dev/ttyAMA2',115200,timeout=0.5) 
        ser = serial.Serial('/dev/ttyACM1',115200,timeout=1.0) # USB-Serial Connection (By Akyas)
    #    ser.write("Serial Success\n".encode())
        return ser

    except BaseException as err:
        log.error(err)

    log.debug("open serial port fail.")
    return None


def send(ser, msg):

    if ser is None:
        log.debug("not connect yet....")

        # ser = connect()
        return 

    try:
        msg1 = msg.encode()
        log.debug(f"sending ... {msg1}")

        ser.write(msg1)
        while ser.in_waiting > 0:
            line = ser.readline().decode().rstrip()
            #print(line)
            log.debug("reply: " + line)

    except BaseException as err:
        log.error(err)