import socket
import sys
import os
import re
import btparse as par
from enum import IntEnum


names = {
        "N": "navigation",
        "V": "vision",
        "R": "radar",
        "T": "throttle",
        "S": "steering"
        }
# fsm stuff
class State(IntEnum):
    STOP = 0
    GO = 1
    TURN = 2
current_state = State.STOP

class Throttle(IntEnum):
    HI = 50,
    LO = -50
    Z = 0
# is this the right way to go about it
# class Steering(IntEnum):

status = {
        "N": False,
        "V": False,
        "R": False,
        "T": False,
        "S": False
        }

def init_modules(sock):
    # confirmation of other scripts
    print('[admin] waiting for full clear')
    while not all(status.values()):
        connection, caddr = sock.accept()
        try:
            while True:
                data = connection.recv(16)
                if data:
                    (src,msg) = par.msg(data)
                    if src in names.keys() and msg == b'READY':
                        print(f'[admin] confirmation from {names[src]} recieved')
                        status[src] = True
                    elif src not in status.keys():
                        print(f'[admin] invalid source {src}')
                else:
                    break
        finally:
            connection.close()


if __name__ == '__main__':
    # get and check filepath
    server_addr = os.environ['BT_ADMIN_ADDR']
    try:
        os.unlink(server_addr)
    except:
        if os.path.exists(server_addr):
            raise

    print(f'[admin] starting socket at {server_addr}')
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(server_addr)
    sock.listen(5)

    print('[admin] socket ready')
    init_modules(sock)
    print('[admin] all clear')

    # start the state machine
    print('[admin] starting FSM')
    status["V"] = False
    status["R"] = False
    prev_state = current_state
    while True:
        if all(status.values()):
            current_state = State.GO
        else:
            current_state = State.STOP
        # print(f'[admin]     --> state is now {State(current_state)}')
        if prev_state != current_state:
            print(f'[admin] state changed {prev_state} -> {current_state}')
            prev_state = current_state

        # communicate with throttle and steering here
        # consider functions
        match current_state:
            case _: pass


        # handle any new data
        connection, caddr = sock.accept()
        try:
            while True:
                data = connection.recv(16)
                if data:
                    (src,msg) = par.msg(data)
                    #print(f'[admin] recieved {data.decode("utf-8")}')
                    match src:
                        case "N": status[src] = par.navi(msg)
                        case "V" | "R": status[src] = par.binary(msg)
                        case _: print(f'[admin] bad signal: {data.decode("utf-8")}')
                else:
                    break
        except KeyError:
            raise
            continue
        finally:
            connection.close()
