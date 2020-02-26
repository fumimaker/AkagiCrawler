import pyautogui

while True:
        filename = "azurenImg/syutugeki.png"
        locate = pyautogui.locateCenterOnScreen(
            filename, grayscale=True, confidence=0.9)
        print(locate)
        print(pyautogui.position())
