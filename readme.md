# AkagiClawler
![trim_7B661DAF-7301-4F50-BCA1-EE6E1A696B7B 5](https://user-images.githubusercontent.com/25518367/87650220-44b0ae80-c78c-11ea-9a94-9aefd21a9dab.gif)
アズレンのアカギを絶対に出したいために始まったプロジェクト．完全にオレオレ仕様なので流用できないと思うけど一応公開しておく．もし使ってみたいという声があれば整備するかもしれない．
果てしなく限界な動作なので動いている様子をみてください．


# How does it work?
iPhoneの画面をpyautoguiでキャプチャしてKerasYOLOV3で学習したモデルよりシーン判別，自分がゲームないのどこのステートメントにいるかを識別します．シーン判別をすると次にタッチする場所をXYプロッタによりタッチします．認識したキャラクターの座標よりGcodeを自動生成し送信，XYプロッタを動作させます．  
![IMG_3323](https://user-images.githubusercontent.com/25518367/87649552-68bfc000-c78b-11ea-924f-db4e204ff1b4.JPG)

**AIが代わりにゲームを進めてくれます（？）**

# Requirement

MBP2018Late 15inch MacOSX Mojave
- absl-py==0.7.1
- astor==0.8.0
- bleach==1.5.0
- cycler==0.10.0
- gast==0.2.2
- grpcio==1.21.1
- h5py==2.9.0
- html5lib==0.9999999
- Keras==2.1.5
- kiwisolver==1.1.0
- Markdown==3.1.1
- matplotlib==3.0.3
- numpy==1.16.4
- Pillow==6.0.0
- protobuf==3.8.0
- pyparsing==2.4.0
- python-dateutil==2.8.0
- PyYAML==5.1.1
- scipy==1.3.0
- six==1.12.0
- tensorboard==1.6.0
- tensorflow==1.6.0
- termcolor==1.1.0
- Werkzeug==0.15.4
- pyautogui

  たしかこんなものだった気がする

# Usage

果てしなく限界な動作なので動いている様子をみてください．

https://twitter.com/fumi_maker/status/1233750592582897665

# How to use

1. 敵キャラがいる海域の画面をたくさんキャプチャ
2. VOTTでアノテーション
   1. 当方はPascalVOCで吐き出してYoloの形式に変換しました．
3. Keras-yolo3でトレーニング
   1. 当方はGPGPUサーバーで学習させました．
   2. 2時間くらいで終わりました
   3. 適当なテスト用の海域用意して認識させてみましょう
   4. 多少のズレの傾向を把握しておきましょう
4. XYプロッタを用意する
5. XYプロッタをつないで，/dev/xxxxを変えてGcodeが動くことを確認する
6. QuickTimeでiPhoneをミラーリングしましょう．
   1. マルチモニターの場合はPyautoguiでスクショを撮っている関係でメイン画面をMacにしてください．
   2. QuickTimeを最大化ではない一番大きい状態にして両端がぴったり画面に着くようにする．
   3. 上辺はメニューバーにぴったり着くようにする．
7. 原点を合わせて./keras-yolo/AkagiClawler.pyを実行する
8. 色々例外処理しながら動いているので判定が遅いですが暖かい目で見守ってあげましょう．

