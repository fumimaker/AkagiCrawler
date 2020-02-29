import pyautogui
import random

num = 10
x = [random.randint(0, 100) for _ in range(num)]
print(x)

arr = x

""" バブルソート """
length = len(x)

for i in range(length):
    for j in reversed(range(i+1, length)):
        if arr[j-1] < arr[j]:
            arr[j-1], arr[j] = arr[j], arr[j-1]
print(x)


while True:
    '''
        filename = "azurenImg/info.png"
        locate = pyautogui.locateCenterOnScreen(
            filename, grayscale=True, confidence=0.9)
        print(locate)
        '''
    print(pyautogui.position())
