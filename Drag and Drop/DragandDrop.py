import cv2
import cvzone
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
from Cvzone.HandTrackingModule import HandDetector
detector=HandDetector(detectionCon=0.8)
cx,cy,w,h=100,100,200,200 # x,y,width,height of the rectangle
class DragRect:
    def __init__(self,posCenter,size=(150,150)):
        self.posCenter=posCenter
        self.size=size
        self.color=(100,50,0)
    def update(self,cursor):
        global temp
        cx,cy=self.posCenter
        w,h=self.size
        

        if cx-w//2<cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:
            self.color=(0,255,0)
            if l<40:
             
                temp=0
                self.color=(100,50,0)
                pass # if the distance between the index finger and the thumb is less than 40 then we do nothing
            else:
                self.posCenter=cursor[0],cursor[1]
                cx,cy=cursor[0],cursor[1] # if the cursor is inside the rectangle then we set the center of the rectangle to the cursor position
                # Actually what happens here within one second the 30 frames are captured supposed , so if we move our index finger slowly in every capture it remains within the rectangle
                # but if we move too quickly then the finger doesn't captured within the rectangle that's why if we move too quickly that ractangle doesn't move with index finger 
                # wotherwise for every miliseconds capture it moves with the index finger because it is in rectangle captured frame
                

        else:
            temp=0
            self.color=(100,50,0)


temp=0
rectList=[]
for i in range(5):          
    rectList.append(DragRect((i*200+100,150)))
while True:
    success,img=cap.read() # captures frames from the video streaming
    img=cv2.flip(img,1) # One is horizontal flip of the image
    allhands,img=detector.findHands(img) # findhands is a function which returns the list of all hands and the image with the hand drawn on it 

    if allhands:
        l,_,_= detector.findDistance((allhands[0]["lmList"][8][0],allhands[0]["lmList"][8][1]),(allhands[0]["lmList"][12][0],allhands[0]["lmList"][12][1]),img)
        cursor= allhands[0]["lmList"][8]
        for rect in rectList:
            if temp!=0:
                temp.update(cursor)
                break
            else:
                rect.update(cursor)
                if rect.color==(0,255,0):
                    temp=rect
                    break
    # Draw Solid 
    
    # for rect in rectList:
    #     cx,cy=rect.posCenter
    #     w,h=rect.size
    #     color=rect.color
    #     cv2.rectangle(img,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),color,cv2.FILLED)  
    #     cvzone.cornerRect(img,(cx-w//2,cy-h//2,w,h),colorC=(255,255,255),t=10,rt=0)
    
    # Draw Transparent
    Nimg=np.zeros_like(img,np.uint8)
    for rect in rectList:
        cx,cy=rect.posCenter
        w,h=rect.size
        color=rect.color
        cv2.rectangle(Nimg,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),color,cv2.FILLED)  
        cvzone.cornerRect(Nimg,(cx-w//2,cy-h//2,w,h),colorC=(255,255,255),t=10,rt=0)
    out=img.copy()
    alpha=0.3 # transparency 
    mask=Nimg.astype(bool)
    out[mask]=cv2.addWeighted(img,alpha,Nimg,1-alpha,0)[mask]
    
    cv2.imshow("Image",out)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
    