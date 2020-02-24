import time
import pyautogui
import sys
import math
import cv2
from PIL import Image
from keras_yolo3.yolo import YOLO


if __name__ == '__main__':
    sc = pyautogui.screenshot("shot.png")
    img = cv2.imread("shot.png")
    img2 = img[45: 1595, 0: 3360]
    cv2.imwrite("croped.png", img2)

    yolo = YOLO()
    image_path = "./croped.png"
    objects_info_list = get_objects_information(yolo, image_path)
    yolo.close_session()

    img = Image.open(image_path)
    count = 0
    for object_info in objects_info_list:
        class_name = object_info['predicted_name']
        x = object_info['x']
        y = object_info['y']
        width = object_info['width']
        height = object_info['height']
        cropped_img = img.crop((x, y, x + width, y + height))
