import time

from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # with draw
    data = []

    # # 设置fps
    # cTime = time.time()
    # fps = 1 / (cTime - pTime)  # 计算fps
    # pTime = cTime  # 更新下一帧图像处理的起始时间
    # # 把fps值显示在图像上,img画板;fps变成字符串;显示的位置;设置字体;字体大小;字体颜色;线条粗细
    # cv2.putText(img, f'FPS: {str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (153, 51, 255), 3)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), serverAddressPort)

    cv2.imshow("Image", img)
    cv2.waitKey(1)