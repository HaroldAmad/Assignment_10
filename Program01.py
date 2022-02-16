import cv2
import numpy as np
from pyzbar.pyzbar import decode
import datetime
import pytz

def decoder(image):
    gray_img = cv2.cvtColor(image,0)
    QRcode = decode(gray_img)

    for obj in QRcode:
        points = obj.polygon
        (x,y,w,h) = obj.rect
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        QRcodeInfo = obj.data.decode("utf-8")
        string = "Data" + str(QRcodeInfo)
        
        currentTime = datetime.datetime.now(pytz.timezone('Asia/Manila'))
        
        with open ('ContactTracing.txt', 'w') as f:
            f.write(str(QRcodeInfo))
            
        with open ('ContactTracing.txt', 'a') as f:
            f.write(str(currentTime))
        
        cv2.putText(frame, string, (x,y), cv2.FONT_ITALIC,0.8,(0,255,0), 2)
        print("Data: "+QRcodeInfo+"")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(10)
    if code == ord('q'):
        break