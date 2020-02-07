import serial
import time

ser = serial.Serial("/dev/cu.usbserial-30", 115200,
                   timeout = 30, parity=serial.PARITY_NONE)


def checkOK():
    flg = 1
    while flg:
        tmp = ser.readline()
        if tmp == b"ok\r\n":
            print(tmp.strip().decode('utf-8'))
            tmp2 = ser.readline()
            if tmp2 == b"ok\r\n":
                flg = 0


def servoUp():
    data = b"M03 S0\r\n"
    print("data")
    ser.write(data)
    checkOK()


def servoDown():
    data = b"M03 S1000\r\n"
    print("data")
    ser.write(data)
    checkOK()


def main():
    flg = 1
    while flg:
        moji = ser.readline()
        if moji == b"Grbl 0.9i ['$' for help]\r\n":
            print(moji.strip().decode('utf-8'))
            flg = 0
    time.sleep(1)
    print("Start")
    servoUp()
    time.sleep(1)
    servoDown()
    time.sleep(1)
    ser.close()


if __name__ == '__main__':
    main()
