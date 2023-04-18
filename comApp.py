import socket
import struct
from pynput.mouse import Controller
from bluetooth import *

mouse = Controller()
server_sock = BluetoothSocket(RFCOMM)
server_sock.bind(("", PORT_ANY))
server_sock.listen(1)

print("Waiting for connection...")
client_sock, client_info = server_sock.accept()
print("Connected to", client_info)

while True:
    try:
        data = client_sock.recv(8)
        if len(data) != 8:
            break

        dx, dy = struct.unpack('2i', data)
        mouse.move(dx, dy)

    except Exception as e:
        print("Error:", e)
        break

client_sock.close()
server_sock.close()
