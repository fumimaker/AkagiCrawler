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
connect = "/dev/cu.usbserial-230"

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
#stageSelect = [800, 450]
stageSelect = [800, 470]
#syutsugeki = [1176, 584]
syutsugeki = [1176, 604]
#fleetSelect = [1315, 680]
fleetSelect = [1315, 700]
#hensei = [1467, 714]
hensei = [1467, 734]
#kaihi = [1385, 536]
kaihi = [1385, 556]
touchany = [500, 500]
#confirm = [1323, 738]
confirm = [1323, 758]
#info = [839, 590]

info = [839, 610]

imagecnt = 0
# pixelRatio = 22.4
pixelRatio = 11.3
displayScale = 0.5
state = 0
runCounter = 0

files = os.listdir("./cropedShot/")
print(files)
filename = []
for f in files:
    tmp = f.strip(".jpg")
    tmp = tmp.strip("croped")
    filename.append(int(tmp))
print(filename)
filename.sort(reverse=True)
print(filename)
yolo = YOLO()

def debugMode():
    x, y , name , len = detectEnemyPos(0)
    print(x, y)
    #_list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
    _list = [(x)*displayScale, (y)*displayScale]
    print("{} detected. Touch X:{:.2f} Y:{:.2f}".format(
        name, _list[0], _list[1]))
    touch(_list)
    '''
    x, y = detectEnemy()
    _list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
    print(_list)
    touch(_list)
    move(0, 0)
    
    locale = get_locate_from_filename("azurenImg/machibuse.png")
    if locale == None:
        touch(confirm)
    else:
        touch(kaihi)
    '''
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
        # グレイスケールで検索(95%一致で判定)
        locate = pyautogui.locateCenterOnScreen(
            filename, grayscale=True, confidence=0.9)
        # フルカラーで検索(遅い)
        # locate = pg.locateCenterOnScreen(filename)
        times += 1
        if not locate == None:
            flag = False
        if times > 3:
            locate = None
            flag = False
    print("Detect image. {}".format(locate))
    return locate


def enemy():
    print("Yolo: 検出開始")
    x, y, name = detectEnemy()
    _list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
    #_list = [(x)*displayScale, (y)*displayScale]
    print("{} detected. Touch X:{:.2f} Y:{:.2f}".format(
        name, _list[0], _list[1]))
    touch(_list)
    return x, y, name


def detectEnemyPos(rank):
    print("ScreenShot.")
    sc = pyautogui.screenshot()
    sc = sc.convert("RGB")
    sc.save("shot.jpg")
    img = cv2.imread("shot.jpg")
    img2 = img[45: 1595, 0: 3360]
    global imagecnt

    
    _filenameString = "cropedShot/croped"+str(imagecnt+filename[0]+1)+".jpg"
    imagecnt+=1
    cv2.imwrite(_filenameString, img2)
    print("detecting enemy.")
    objects_info_list = get_objects_information(yolo, _filenameString)

    img = Image.open(_filenameString)
    _gx = []
    counter = 0
    for object_info in objects_info_list:
        class_name = object_info['predicted_name']
        x = object_info['x']
        y = object_info['y']
        width = object_info['width']
        height = object_info['height']
        print("{} x:{} y:{} height:{} width:{}".format(
            class_name, x, y, height, width))
        counter += 1
    
    length = len(objects_info_list)
    for i in range(length):
        for j in reversed(range(i+1, length)):
            dicMinusOne = objects_info_list[j-1]
            dic = objects_info_list[j]
            if dicMinusOne["x"] < dic["x"]:
                objects_info_list[j-1], objects_info_list[j] = objects_info_list[j], objects_info_list[j-1]
    try:
        dic = objects_info_list[rank]
    except:
        dic = objects_info_list[0]
    print(objects_info_list)
    x = dic["x"]+(dic["width"]/2)
    y = dic["y"]+(dic["height"]/2)
    name = dic["predicted_name"]
    #return x-50, y+40, name, len(objects_info_list)
    return x, y+120, name, len(objects_info_list)


def detectEnemy():
    sc = pyautogui.screenshot()
    sc = sc.convert("RGB")
    sc.save("shot.jpg")
    img = cv2.imread("shot.jpg")
    img2 = img[45: 1595, 0: 3360]
    _filenameString = "cropedShot/croped"+str(imageCounter)+".jpg"
    cv2.imwrite(_filenameString, img2)
    objects_info_list = get_objects_information(yolo, _filenameString)
    
    img = Image.open(_filenameString)
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
    while 1:
        time.sleep(3)
        print("ステージセレクト")
        touch(stageSelect)
        print("出撃確認")
        touch(syutsugeki)
        print("艦隊選択")
        touch(fleetSelect)
        move(0, 0)
        completed = False
        while not completed:
            failCounter = 0
            time.sleep(5)
            state = 0
            changeFlag = False
            infoFlg = False
            contactFlg = False
            enemyFlg = True
            while state != 5:
                time.sleep(1)
                if enemyFlg:
                    x, y, name, length = detectEnemyPos(failCounter)
                    print(x, y)
                    #_list = [(x-origin[0])*displayScale, (y-origin[1])*displayScale]
                    _list = [(x)*displayScale, (y)*displayScale]
                    print("{} detected. Touch X:{:.2f} Y:{:.2f}".format(
                        name, _list[0], _list[1]))
                    touch(_list)
                    time.sleep(5)

                print("状況確認")
                if get_locate_from_filename("azurenImg/syutugeki.png") != None: 
                    # 出撃確認になっていたら
                    print("出撃確認になっていた")
                    state = 4
                    infoFlg = False
                    touch(hensei)
                    contactFlg = True
                    time.sleep(5)
                elif get_locate_from_filename("azurenImg/machibuse.png") != None:
                    # 待ち伏せ艦隊検知になっていたら
                    print("待ち伏せ艦隊検知になっていた")
                    state = 7
                    touch(kaihi)
                    changeFlag = False
                    enemyFlg = True
                    infoFlg = False
                    move(0, 0)
                    time.sleep(5)
                else:
                    # 敵飛行機検知になったら
                    print("敵飛行機検知になった，もしくはタップ失敗")
                    servoDown()
                    servoUp()
                    if get_locate_from_filename("azurenImg/syutugeki.png") != None:
                        # 出撃確認になっていたら
                        print("出撃確認になっていた")
                        state = 4
                        infoFlg = False
                        touch(hensei)
                        contactFlg = True
                        time.sleep(5)
                    else:
                        move(0, 0)
                        failCounter += 1
                        # touch(hensei)
                        infoFlg = True
                        #enemyFlg = True
                        contactFlg = True

                if infoFlg:
                    if get_locate_from_filename("azurenImg/info.png") != None:
                            print("INFO detect")
                            touch(info)

                if contactFlg:
                    if get_locate_from_filename("azurenImg/contact.png") != None:
                        # 戦闘開始していたら
                        print("戦闘開始していた")
                        state = 5
                        failCounter = 0
            move(0, 0)


            while get_locate_from_filename("azurenImg/victory.png") == None:
                print("waiting for victory...")
                time.sleep(1)
            print("戦闘終了確認")
            touch(confirm)  # 完全勝利確認
            time.sleep(1)
            print("アイテム入手確認")
            touch(confirm)  # アイテム入手確認
            time.sleep(2)
            print("End")
            touch(confirm)
            move(0, 0)
            global runCounter
            if name == "boss":
                completed = True
                print("ボス撃破，終了")
                print("周回カウンタ　{}週目".format(runCounter))
                runCounter += 1
            else:
                print("{} 撃破".format(name))
                print("敵検索継続")
                print("周回カウンタ　{}週目".format(runCounter))

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
