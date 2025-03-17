import cv2
import time
cap=cv2.VideoCapture(0)
from cvzone import HandDetector
detector = HandDetector(detconf=0.8)
cap.set(3,1280) # It is used to set the width of the frame
cap.set(4,720) # It is used to set the height of the frame
while True:
    success,img=cap.read()
    img=detector.findhand(img)
    lists=detector.findposition(img)
    
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
cap.release() # It is used to release the camera and close the window which was opened by the camera 
cv2.destroyAllWindows() # It is used to close all the windows which were opened by the camera
