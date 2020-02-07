import serial
import time

ser = serial.Serial("/dev/cu.usbserial-30", 115200,
                    timeout=30, parity=serial.PARITY_NONE)
flg = 1
while flg:
    moji = ser.readline()
    if moji == b"Grbl 0.9i ['$' for help]\r\n":
        print(moji.strip().decode('utf-8'))
        flg = 0

moji1 = 'M05 S0\r\n'
moji2 = 'M03 S1000\r\n'
ser.write(b"\r\n\r\n")
time.sleep(3)

print("Start")
ser.write(b"M03 S0\r\n")
print(moji1)
flg = 1
while flg:
    tmp = ser.readline()
    if tmp == b"ok\r\n":
        print(tmp.strip().decode('utf-8'))
        tmp2 = ser.readline()
        if tmp2 == b"ok\r\n":
            print(tmp2.strip().decode('utf-8'))
            flg = 0

ser.write(b"M03 S1000\r\n")
print(moji2)
flg = 1
while flg:
    tmp = ser.readline()
    if tmp == b"ok\r\n":
        print(tmp.strip().decode('utf-8'))
        tmp2 = ser.readline()
        if tmp2 == b"ok\r\n":
            print(tmp2.strip().decode('utf-8'))
            flg = 0

ser.close()
