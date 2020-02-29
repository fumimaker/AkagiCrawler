import time
import pyautogui
import sys
import math
import cv2
from PIL import Image
from yolo import YOLO
import os
from objects import get_objects_information


if __name__ == '__main__':
    yolo = YOLO()
    for i in range(3):
        sc = pyautogui.screenshot()
        sc = sc.convert("RGB")
        sc.save("shot.jpg")
        img = cv2.imread("shot.jpg")
        img2 = img[45: 1595, 0: 3360]
        cv2.imwrite("croped.jpg", img2)
        image_path = "croped.jpg"
        objects_info_list = get_objects_information(yolo, image_path)
        
        count = 0
        img = Image.open(image_path)
        for object_info in objects_info_list:
            class_name = object_info['predicted_name']
            x = object_info['x']
            y = object_info['y']
            width = object_info['width']
            height = object_info['height']
            print("{} x:{} y:{} height:{} width:{}".format(class_name, x, y, height, width))
            
            cropped_img = img.crop((x, y, x + width, y + height))
            cropped_img.save("./pic/{}{}.jpg".format(class_name, count))
            count = count + 1
    yolo.close_session()
