import serial
import time
import pyautogui
import sys
import math
import cv2
from PIL import Image
from yolo import YOLO
import os
from objects import get_objects_information

feedingSpeed = 3000
connect = "/dev/cu.usbserial-30"

debug = False
#debug = True
ser = None
'''
origin = [252, 167]
stageSelect = [1763, 918]
syutsugeki = [2348, 1170]
fleetSelect = [2624, 1357]
'''

origin = [125, 83]
stageSelect = [800, 450]
syutsugeki = [1176, 584]
fleetSelect = [1315, 680]
hensei = [1467, 714]
kaihi = [1385, 536]
touchany = [500, 500]
confirm = [1323, 738]

# pixelRatio = 22.4
pixelRatio = 11.3
displayScale = 0.58333

yolo = YOLO()

def debugMode():
    '''
    x, y = detectEnemy()
    _list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
    print(_list)
    touch(_list)
    move(0, 0)
    '''
    locale = get_locate_from_filename("azurenImg/machibuse.png")
    if locale == None:
        touch(hensei)
    else:
        touch(kaihi)
    move(0, 0)

def scalingAndOffset(cord):
    _x, _y = cord
    _list = [(_x-origin[0])*displayScale, (_y-origin[1])*displayScale]
    return _list

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
    print("Servo UP")
    print(data.strip().decode('utf-8'))
    ser.write(data)
    checkOK()


def servoDown():
    data = b"M03 S1000\r\n"
    print("Servo Down")
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
    _x = coord[0]
    _y = coord[1]
    print("touch X:{:.2f} Y:{:.2f}".format(_x, _y))
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
    flag = True
    while flag:
        time.sleep(1)
        # グレイスケールで検索(95%一致で判定)
        locate = pyautogui.locateCenterOnScreen(
            filename, grayscale=True, confidence=0.9, region=(0, 25, 2880, 1371))
        # フルカラーで検索(遅い)
        # locate = pg.locateCenterOnScreen(filename)
        times += 1
        if not locate == None:
            flag = False
        if times > 5:
            locate = None
            flag = False
    print("Detect image. {}".format(locate))
    return locate


def detectEnemy():
    
    sc = pyautogui.screenshot()
    sc = sc.convert("RGB")
    sc.save("shot.jpg")
    img = cv2.imread("shot.jpg")
    img2 = img[45: 1595, 0: 3360]
    cv2.imwrite("croped.jpg", img2)
    image_path = "croped.jpg"
    objects_info_list = get_objects_information(yolo, image_path)
    
    img = Image.open(image_path)
    _gx = []
    _gy = []
    counter = 0
    for object_info in objects_info_list:
        class_name = object_info['predicted_name']
        x = object_info['x']
        y = object_info['y']
        width = object_info['width']
        height = object_info['height']
        _gx.append(x+width/2)
        _gy.append(y+height/2)
        print("{} x:{} y:{} height:{} width:{} center:{},{}".format(
            class_name, x, y, height, width, _gx[counter], _gy[counter]))
        counter += 1
    max = 0
    index = 0
    counter = 0
    for i in _gx:
        if i > max:
            max = i
            index = counter
        counter += 1
    dic = objects_info_list[index]
    x = dic["x"]+(dic["width"]/2)
    y = dic["y"]+(dic["height"]/2)
    name = dic["predicted_name"]
    return x-20, y, name


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
    print("ステージセレクト")
    touch(stageSelect)
    print("出撃確認")
    touch(syutsugeki)
    print("艦隊選択")
    touch(fleetSelect)
    move(0, 0)

    completed = False
    while not completed:
        time.sleep(5)
        print("Yolo: 検出開始")
        x, y, name = detectEnemy()
        _list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
        print("{} detected. Touch X:{:.2f} Y:{:.2f}".format(name, _list[0], _list[1]))
        touch(_list)
        locale = get_locate_from_filename("azurenImg/machibuse.png")  # 敵艦みゆ
        if locale == None:
            print("敵艦遭遇なし")
            print("出撃")
            touch(hensei)
        else:
            print("敵艦見ゆ")
            print("回避")
            touch(kaihi)

        locale = get_locate_from_filename("azurenImg/contact.png")
        if locale == None:  # 敵をタッチできていない リトライ
            print("タッチ失敗，リトライ")
            x, y, name = detectEnemy()
            _list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
            print("Enemy detected. Touch X:{:.2f} Y:{:.2f}".format(
                _list[0], _list[1]))
            touch(_list)
        else:  # 戦闘開始確認
            print("戦闘開始確認ヨシ")
            move(0, 0)

        while get_locate_from_filename("azurenImg/victory.png") == None:
            print("waiting for victory...")
            time.sleep(1)
        print("戦闘終了確認")
        touch(touchany)  # 完全勝利確認
        time.sleep(1)
        print("アイテム入手確認")
        touch(touchany)  # アイテム入手確認
        time.sleep(2)
        print("End")
        touch(confirm)
        move(0, 0)
        if name == "boss":
            completed = True
            print("ボス撃破，終了")
        else:
            print("{} 撃破".format(name))
            print("敵検索継続")
    yolo.close_session()
    ser.close()


if __name__ == '__main__':
    if not debug:
        ser = serial.Serial(connect, 115200,
                            timeout=30, parity=serial.PARITY_NONE)
        main()
    else:
        ser = serial.Serial(connect, 115200,
                            timeout=30, parity=serial.PARITY_NONE)
        debugMode()
