import time
import pyautogui
import sys
import math
import cv2

sc = pyautogui.screenshot("shot.png")
img = cv2.imread("shot.png")
#img2 = img[0: 45, 3360: 1595]
img2 = img[45: 1595, 0: 3360]
cv2.imwrite("croped.png", img2)
