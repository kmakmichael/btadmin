import socket
import sys
import os
import btparse as par
from enum import IntEnum
from threading import Thread, Event, Barrier, Lock

server_addr = os.environ['BT_ADMIN_ADDR']
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

# data from the input modules
input_data = {
        "N": False,
        "V": False,
        "R": False,
        }
input_modules = len(input_data)
output_modules = 2

# threading stuff
data_changed = Event()
data_lock = Lock()
inputs_ready = Barrier(input_modules+1)
outputs_ready = Barrier(output_modules+1)



def client_thread(connection, indata):
    while True:
        data = connection.recv(3)
        if data:
            (src,msg) = par.msg(data)
            if msg == b'R':
                break
    try:
        print(f'[admin] confirmation from {names[src]} recieved', flush=True)
    except KeyError:
        print('uh-oh')
        return
    inputs_ready.wait()
    connection.send(b'ACK')
    nd = False
    try:
        while True:
            data = connection.recv(3)
            if data:
                (src,msg) = par.msg(data)
                # print(f'[admin] recieved {data.decode("utf-8")} -> {src}:{msg}', flush=True)
                if src == "N":
                    nd = par.navi(msg)
                if src == "V" or src == "R":
                    nd = par.binary(msg)
                with data_lock:
                    if indata[src] != nd:
                        indata[src] = nd
                        data_changed.set()
    except KeyError:
        # this should trigger somethng more catastrophic, probably
        print('ok but how')
        return


def server_socket():
    # get and check filepath
    server_addr = os.environ['BT_ADMIN_ADDR']
    try:
        os.unlink(server_addr)
    except:
        if os.path.exists(server_addr):
            raise
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(server_addr)
    return sock


def set_outputs(s):
    if s == 0:
        print('[admin] === STOP ===')
    else:
        print('[admin] ===  GO  ===')
    # print(f'state has become {s}, setting outputs to ...')
    pass


if __name__ == '__main__':
    # get a socket
    print(f'[admin] starting socket at {server_addr}')
    sock = server_socket()
    sock.listen(5)

    # connect to modules
    print('[admin] socket ready')
    threads = []
    # TODO: find some way for this to not be limited to 3. if we get a bad connection we're boned
    for i in range(0,input_modules):
        c, caddr = sock.accept()
        print(f'[admin] received connection from {caddr}')
        th = Thread(target=client_thread, args=[c, input_data])
        th.start()
        threads.append(th)
    # wait for them to be ready
    inputs_ready.wait()
    print('[admin] all input modules ready')

    # connect to output modules


    # start state machine
    print('[admin] starting FSM')
    prev_state = current_state
    while True:
        data_changed.wait()
        data_changed.clear()
        # state machine here
        with data_lock:
            # print(f'input_data is {input_data}')
            if all(input_data.values()):
                current_state = State.GO
            else:
                current_state = State.STOP
            if prev_state != current_state:
                # print(f'[admin] state changed {prev_state} -> {current_state}')
                prev_state = current_state
                set_outputs(current_state)
