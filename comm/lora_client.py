import serial
import time

import threading

# import logging
from models.logger import Logger

log = Logger('log/lorawan.log', level='debug').logger



'''
create a thread to listen serial port
'''
def set_listener(ser):
    if(ser.is_open):
        # successful = True
        th = threading.Thread(target=read_from_serial_port, args=(ser,))
        th.start()

        log.debug("start thread to listening...")



# logging.basicConfig(filename="log.txt", level=logging.DEBUG)
def connect():
    # return None
    port = ""
    try:
        port = "/dev/ttyACM0"
        log.debug("Opening " + port)
        ser = serial.Serial(port, 115200, timeout=1.0) # USB-Serial Connection (By Akyas)
    #    ser.write("Serial Success\n".encode())
        set_listener(ser)
        return ser

    except BaseException as err:
        log.error(err)

    try:
        port = "/dev/ttyACM1"
        log.debug("Opening " + port)
        ser = serial.Serial(port, 115200, timeout=1.0) # USB-Serial Connection (By Akyas)
    #    ser.write("Serial Success\n".encode())
        set_listener(ser)

        return ser

    except BaseException as err:
        log.error(err)

    log.debug("Open serial port fail.")
    return None

def close(ser):
    try:
        if ser is not None:
            ser.close()
            log.debug("Closed serial port successfully.")
            return
    except BaseException as err:
        log.error(err)

    log.debug("Closed serial port fail.")
    return
'''
read reply data from serial port
'''
def read_from_serial_port(ser):
    # global GLOBAL_DATA_LIST, GLOBAL_NOTEND
    
    while (ser is not None) and ser.is_open:
        if ser.in_waiting:
            # data = b2a_hex(ser.read(ser.in_waiting)).decode('utf-8') #16进制的字符串，例如：'4141'，'FF'
            # print("\n[received] " + data)
            # GLOBAL_DATA_LIST.append(data)
            # print("begin receive 1")
            line = ser.readline().decode().rstrip()
            #print(line)
            log.debug("Reply: %s" % line)

        time.sleep(0.01)



def send(ser, msg):

    if ser is None:
        log.debug("Not connect yet....")

        # ser = connect()
        return 

    try:
        msg1 = msg.encode()  #.replace("\n", "\\n")
        log.debug(f"Sending ... {msg1}")

        ser.write(msg1)

        log.debug("begin receive...")
        # while ser.in_waiting > 0:

        #     # print("begin receive 1")
        #     line = ser.readline().decode().rstrip()
        #     #print(line)
        #     log.debug("reply: " + line)


    except BaseException as err:
        log.error(err)

