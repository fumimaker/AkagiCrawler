import time
import pyautogui as pg
import sys


def get_locate_from_filename(filename):
    locate = None
    while locate == None:
        time.sleep(0.1)
        # グレイスケールで検索(95%一致で判定)
        locate = pg.locateCenterOnScreen(
            filename, grayscale=True, confidence=0.950)
        # フルカラーで検索(遅い)
        # locate = pg.locateCenterOnScreen(filename)
    return locate
    

if __name__ == "__main__":
    pos_x, pos_y = get_locate_from_filename('origin.png')
    print(pos_x, pos_y)
