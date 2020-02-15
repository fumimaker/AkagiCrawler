import cv2
import numpy as np

# 学習器(cascade.xml)の指定
Cascade = cv2.CascadeClassifier('./cv/cascade/data/stage10.xml')
# 予測対象の画像の指定
img = cv2.imread('test.jpg', cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
point = Cascade.detectMultiScale(gray, 1.1, 3)

if len(point) > 0:
    for rect in point:
        cv2.rectangle(img, tuple(rect[0:2]), tuple(
            rect[0:2]+rect[2:4]), (0, 0, 255), thickness=2)
else:
    print("not detected.")

cv2.imwrite('detected.jpg', img)
