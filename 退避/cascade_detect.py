import cv2

image = "./test2.PNG"
# カスケードファイルを読み込む
face_cascade = cv2.CascadeClassifier(
    "./stage4.xml")
# 画像を読み込む
loaded_img = cv2.imread(f"{image}")
# （高さ・幅・色数)
# 読み込んだ画像を、グレースケール画像として読み込む
gray = cv2.cvtColor(loaded_img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray)
if len(faces) == 0:
    print('画像が認識されません')
else:
    for (x, y, w, h) in faces:
            # この中で、顔の部分に色をつけている処理をしている
        penned_img = cv2.rectangle(
            loaded_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = penned_img[y:y+h, x:x+w]
    # 画像を表示させる
    cv2.imshow('img', penned_img)
    # キーボードの入力を待つ
    cv2.waitKey(0)
    # 画像windowを閉じる
    cv2.destroyAllWindows()
