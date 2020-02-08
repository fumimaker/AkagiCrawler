import serial
import time
import pyautogui
import sys


ser = serial.Serial("/dev/cu.usbserial-30", 115200,
                    timeout=30, parity=serial.PARITY_NONE)

feedingSpeed = 3000


def checkOK():
    flg = 1
    while flg:
        tmp = ser.readline()
        if tmp == b"ok\r\n":
            print(tmp.strip().decode('utf-8'))
            tmp2 = ser.readline()
            if tmp2 == b"ok\r\n":
                flg = 0
                print()


def servoUp():
    data = b"M03 S0\r\n"
    print(data.strip().decode('utf-8'))
    ser.write(data)
    checkOK()


def servoDown():
    data = b"M03 S1000\r\n"
    print(data.strip().decode('utf-8'))
    ser.write(data)
    checkOK()


def axisX(coord):
    data = b"G01 X" + str(coord).encode('utf-8') + b" F" + \
        str(feedingSpeed).encode('utf-8') + b"\r\n"
    print(data.strip().decode('utf-8'))
    ser.write(data)
    checkOK()


def axisY(coord):
    data = b"G01 Y" + str(coord).encode('utf-8') + b" F" + \
        str(feedingSpeed).encode('utf-8') + b"\r\n"
    ser.write(data)
    checkOK()


def move(x, y):
    data = b"G01 X" + str(x).encode('utf-8') + b" Y" + str(y).encode(
        'utf-8') + b" F" + str(feedingSpeed).encode('utf-8') + b"\r\n"
    ser.write(data)
    checkOK()


def setZeroPosition():
    data = b"G92 x0 y0 z0\r\n"
    print(data.strip().decode('utf-8'))
    ser.write(data)
    checkOK()


def main():
    flg = 1
    while flg:
        moji = ser.readline()
        if moji == b"Grbl 0.9i ['$' for help]\r\n":
            print(moji.strip().decode('utf-8'))
            flg = 0
    print("Start")
    servoUp()
    servoDown()
    setZeroPosition()
    servoUp()
    move(20, 20)
    ser.close()


if __name__ == '__main__':
    main()
