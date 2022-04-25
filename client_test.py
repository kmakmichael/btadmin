from btcomms import BTComms
import sys
import time

time.sleep(0.5)
if sys.argv[1] != 'D':
    com = BTComms(sys.argv[1])
    com.send(sys.argv[2])
time.sleep(1.5)
