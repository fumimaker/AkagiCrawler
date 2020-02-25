import os
from PIL import Image
import cv2

def get_objects_information(yolo, image_path):
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError
        image = Image.open(image_path)
        print("file opened.")
        img, dictionary = yolo.detect_image(image)
        # img.show()
        return dictionary
    except FileNotFoundError:
        print("The Image file isn't found. Check the image file path.")
    except IOError:
        print('Image open Error. Try again.')
