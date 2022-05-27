import socket
from datetime import datetime

# HOST = '192.168.1.218'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000        

max_size = 1000

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

print('Server started at {}'.format(dt_string))
print('Server address: {}:{}'.format(HOST,PORT))
print('Waiting for a client now !')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

server.listen(5)

while True:
    conn, addr = server.accept()
    data = conn.recv(max_size)

    # print('Connected by {}'.format(addr))
    print()
    print(data)

    conn.sendall(b'Received')
    conn.close()

server.close()
