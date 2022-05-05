from serial import Serial

ser = Serial('/dev/ttyACM0', baudrate=115200)
while True:
    i = (input() + '\r\n').encode('ascii')
    print(f'writing {i}')
    ser.write(i)
