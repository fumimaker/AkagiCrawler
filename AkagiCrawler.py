import serial
import time
import pyautogui
import sys
import math

ser = serial.Serial("/dev/cu.usbserial-30", 115200,
                    timeout=30, parity=serial.PARITY_NONE)

feedingSpeed = 2500


origin = [252, 167]
stageSelect = [1763, 918]
syutsugeki = [2348, 1170]
fleetSelect = [2624, 1357]

pixelRatio = 22.4


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


def touch(coord):
    _x = (coord[0] - origin[0]) / pixelRatio
    _y = (coord[1] - origin[1]) / pixelRatio

    n = 3  # 切り捨て桁数
    _x = math.floor(_x * 10 ** n) / (10 ** n)
    _y = -1 * math.floor(_y * 10 ** n) / (10 ** n)
    move(_x, _y)
    servoDown()
    servoUp()


def get_locate_from_filename(filename):
    locate = None
    times = 0
    while locate == None:
        time.sleep(0.1)
        # グレイスケールで検索(95%一致で判定)
        locate = pyautogui.locateCenterOnScreen(
            filename, grayscale=True, confidence=0.2)
        # フルカラーで検索(遅い)
        # locate = pg.locateCenterOnScreen(filename)
        times += 1
        if times > 5:
            locate = 1

    return locate


def main():
    flg = 1
    while flg:
        moji = ser.readline()
        if moji == b"Grbl 0.9i ['$' for help]\r\n":
            print(moji.strip().decode('utf-8'))
            flg = 0
    print("Akagi Crawler Start")
    servoUp()
    setZeroPosition()
    touch(stageSelect)
    touch(syutsugeki)
    touch(fleetSelect)
    try:
        pos_x, pos_y = get_locate_from_filename('triangle1.png')
        touch(pos_x, pos_y)
    except:
        try:
            pos_x, pos_y = get_locate_from_filename('triangle2.png')
            touch(pos_x, pos_y)
        except:
            try:
                pos_x, pos_y = get_locate_from_filename('triangle3.png')
                touch(pos_x, pos_y)
            except:
                try:
                    pos_x, pos_y = get_locate_from_filename('triangle4.png')
                    touch(pos_x, pos_y)
                except:
                    try:
                        pos_x, pos_y = get_locate_from_filename('triangle5.png')
                        touch(pos_x, pos_y)
                    except:
                        move(0, 0)
                        pass
    move(0, 0)
    ser.close()


if __name__ == '__main__':
    main()
