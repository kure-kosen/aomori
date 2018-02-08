import cv2
import numpy as np
import matplotlib.pyplot as plt

# 取得する色の範囲を指定する
lower_yellow = np.array([100,100,100])
upper_yellow = np.array([150,150,150])

cap = cv2.VideoCapture(0)
 
cascade = cv2.CascadeClassifier('TrainingAssistant/results/cascades/tegaki_maru3/cascade.xml') #分類器の指定

while(1):
    # フレームを取得
    ret, frame = cap.read()
 
    # フレームをHSVに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
    circles= cascade.detectMultiScale(frame, 1.1, 3) #物体の検出

    for (x, y, w, h) in circles:
        upper_left = (x, y)
        bottom_right = (x+w, y+h)
        cv2.rectangle(frame, upper_left, bottom_right, (255, 20, 147), thickness=3) #円の描画
 
    cv2.imshow("display", frame)
 
    # qを押したら終了
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
