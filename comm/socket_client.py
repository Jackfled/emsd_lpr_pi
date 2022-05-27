import socket
import time

def connect(HOST, PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    reconnect = 0
    while(True):
        try:
            client.connect((HOST,PORT))
        except OSError:
            reconnect = reconnect+1
            print('Timeout, reconnecting...({})'.format(reconnect))
            time.sleep(5)
        else:
            break

    return client


def send(client, msg):
    client.sendall(msg.encode('utf-8'))
    data = client.recv(1024)
    print(repr(data))
    client.close()
