import cv2
import numpy as np
import matplotlib.pyplot as plt

# 画像の読込み
img_path = '../datasets/peach/0.jpg'
img = cv2.imread(img_path)

# 取得する色の範囲を指定する
lower_yellow = np.array([20, 50, 50])
upper_yellow = np.array([100, 255, 255])
 
# 指定した色に基づいたマスク画像の生成
img_mask = cv2.inRange(img, lower_yellow, upper_yellow)

cap = cv2.VideoCapture(0)
 
while(1):
 
    # フレームを取得
    ret, frame = cap.read()
 
    # フレームをHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    # 取得する色の範囲を指定する
    lower_yellow = np.array([20, 50, 50])
    upper_yellow = np.array([100, 255, 255])
 
    # 指定した色に基づいたマスク画像の生成
    img_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
 
    # フレーム画像とマスク画像の共通の領域を抽出する。
    img_color = cv2.bitwise_and(frame, frame, mask=img_mask)
 
    cv2.imshow("SHOW COLOR IMAGE", img_color)
 
    # qを押したら終了
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
