import comm.lora_client
import time


if __name__ == '__main__':
    ser = comm.lora_client.connect()
    i = 0

    
    while(True):
        
        if ser is None:
            ser = comm.lora_client.connect()
        
        i = i + 1
        data = "test %d\n" % i
        comm.lora_client.send(ser, data)

        time.sleep(5)

    # comm.lora_client.close()