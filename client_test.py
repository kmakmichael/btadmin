from btcomms import BTComms
import sys
import time

if sys.argv[1] != 'D':
    com = BTComms(sys.argv[1])
    com.send(sys.argv[2])
