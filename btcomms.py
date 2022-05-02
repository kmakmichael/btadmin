import socket
import sys
import os

base_addr = os.environ['BT_ADMIN_ADDR']

class BTComms:

    def __init__(self, n, tgt=base_addr):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.name = n
        self.target = tgt
        self.bind()
        try:
            self.sock.connect(self.target)
        except:
            print(f'error connecting to {self.target}')
            sys.exit(1)

    def confirm(self):
        self.send('R')
        while True:
            data = self.sock.recv(3)
            if data and data == b'ACK':
                return

    # send a string
    def send(self, msg):
        try:
            self.sock.sendall(f'{self.name}:{msg}'.encode())
        except:
            print('could not send data')


    def bind(self):
        self.addr = f'{base_addr}{self.name}'
        try:
            os.unlink(self.addr)
        except:
            if os.path.exists(self.addr):
                raise
        self.sock.bind(self.addr)
    
    
    def __del__(self):
        self.sock.close()
