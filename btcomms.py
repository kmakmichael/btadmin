import socket
import sys
import os

server_addr = os.environ['BT_ADMIN_ADDR']

class BTComms:

    def __init__(self, pre, tgt=os.environ['BT_ADMIN_ADDR']):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.prefix = pre
        self.target = tgt
        try:
            self.sock.connect(self.target)
        except:
            print(f'error connecting to {self.target}')
            sys.exit(1)

    def confirm():
        send('R')


    # send a string
    def send(self, msg):
        try:
            self.sock.sendall(f'{self.prefix}:{msg}'.encode())
        except:
            print('could not send data')

    def __del__(self):
        self.sock.close()
