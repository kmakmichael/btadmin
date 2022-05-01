from btcomms import BTComms
import sys
import time

com = BTComms(sys.argv[1])
while True:
    com.send(input())
