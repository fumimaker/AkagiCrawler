import time
import pyautogui as pg
import sys
import math

def get_locate_from_filename(filename):
    locate = None
    times = 0
    while locate == None:
        time.sleep(0.1)
        # グレイスケールで検索(95%一致で判定)
        locate = pg.locateCenterOnScreen(filename, grayscale=True, confidence=0.9)
        # フルカラーで検索(遅い)
        # locate = pg.locateCenterOnScreen(filename)
        times += 0.1
        if times > 1:
            locate = 1
            break
    return locate
    

if __name__ == "__main__":
    pos = get_locate_from_filename('enemy3.png')
    print(pos)
    while 1:
        time.sleep(0.5)
        print(pg.position())
