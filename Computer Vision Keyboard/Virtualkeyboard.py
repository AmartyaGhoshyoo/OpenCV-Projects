import cv2
from  time  import sleep
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller,Key
import cvzone
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,820)
detector=HandDetector(detectionCon=0.8)
class Button:
    def __init__(self,pos,text,size=(85,85)):
        self.pos=pos
        self.text=text
        self.size=size
        
def drawall(img,buttonlist):
    temp=0
    for button in buttonlist:
        x,y=button.pos
        w,h=button.size
        if button.text in {'Sp','Clr','LrC','UpC','Ent'}:
            cvzone.cornerRect(img, (x+temp,y, 150, 85), l=15, t=10, colorR=(100, 40, 60), colorC=(100,100,0))
            cv2.rectangle(img,(x+temp,y),(x+150+temp,y+85),(100,40,60),cv2.FILLED)
            cv2.putText(img,button.text,(x+15+temp,y+65),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,255,255),3,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
            temp+=100
        else:
            cvzone.cornerRect(img, (x, y, w, h), l=15, t=10, colorR=(100, 40, 60), colorC=(100,100,0))
            cv2.rectangle(img,button.pos,(x+w,y+h),(100,40,60),cv2.FILLED)
            """
            Always remeber here in openCV projects and yolo origin always at the top left corner in the frame
            Understanding the Coordinates:
            (100,100) → Top-left corner of the rectangle (x=100, y=100).
            (200,200) → Bottom-right corner of the rectangle (x=200, y=200).
            """ 
            cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,255,255),3,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
            """
            cv2.putText(img, "Q", (150,150), cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 3, cv2.FILLED)
            (125,170): This is the bottom-left corner of the text, not the center.
            cv2.FONT_HERSHEY_COMPLEX, 2: The font size is 2, affecting text placement.
            The rectangle is from (100,100) to (200,200), meaning its center is (150,150), but the text is not centered automatically.
            
            To get the text size
            (text_width, text_height), bqaseline = cv2.getTextSize(text, font, font_scale, thickness)
            # Compute the center position
            x = 100 + (100 - text_width) // 2
            y = 100 + (100 + text_height) // 2  # Adjusting for baseline
            
            
            """

x,y=85,85
buttonlist=[]
words="Q W E R T Y U I O P-A S D F G H J K L :-Z X C V B N M , . ?-Sp Clr LrC UpC Ent".split('-')
words=[part.split() for part in words]
#METHOD-1
for j in range(len(words)):
    for i,key in enumerate(words[j],1):
        buttonlist.append(Button((100*i,100*(j+1)),key))

# METHOD-2
# for j in range(len(words)):
#     for i,w in enumerate(words[j],1):
#         globals()[f"createButton{i+(j*10)}"]=Button((x,y),w)
#         x=x+100
#     x=85
#     y=y+100

findText=""
keyboard=Controller()
Uppercase=True
while True:
    success,img=cap.read()
    allhands,img=detector.findHands(img)
    # METHOD-2
    # for j in range(len(words)):
    #     for i,w in enumerate(words[j],1):
    #         globals()[f"createButton{i+(j*10)}"].draw(img)
    #Method-1 
    drawall(img,buttonlist)
    l,f,c=img.shape
       
    if allhands:
        temp=0
        index={
            'Sp':0,
            'Clr':1,
            'LrC':2,
            'UpC':3,
            'Ent':4
        }
        if Uppercase:
            for button in buttonlist:
                x,y=button.pos
                w,h=button.size
                
                if button.text in {'Sp','Clr','LrC','UpC','Ent'}:
                    if (x+100*index[button.text])<(allhands[0]["lmList"][8][0]) < (x+150+100*index[button.text]) and y<(allhands[0]["lmList"][8][1])< (y+h):
                        cv2.rectangle(img,(x+(100*index[button.text])-5,y-5),(x+150+5+(100*index[button.text]),y+h+5),(200,100,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+15+(100*index[button.text]),y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                        index4=(allhands[0]["lmList"][4][0],allhands[0]["lmList"][4][1])
                        index12=(allhands[0]["lmList"][12][0],allhands[0]["lmList"][12][1])
                        l,_,_=detector.findDistance(index4,index12,img)
                        if l<30:
                            if button.text=='Sp':
                                keyboard.press(Key.space)
                                # keyboard.release(Key.space)
                            if button.text=='Clr':
                                keyboard.press(Key.backspace)
                            if button.text=='Ent':
                                keyboard.press(Key.enter)
                                # keyboard.release(key.backspace)
                            if button.text=='LrC':
                                Uppercase=False
                                                        
                            # keyboard.press(button.text)
                            cv2.rectangle(img,(x+(100*index[button.text])-5,y-5),(x+150+5+(100*index[button.text]),y+h+5),(255,255,0),cv2.FILLED)
                            cv2.putText(img,button.text,(x+15+(100*index[button.text]),y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                            if button.text=='Sp':
                                findText+=" "
                            elif button.text=='Clr' and findText:
                                findText=findText.split()
                                findText[-1]=findText[-1][:-1]
                                findText = " ".join(findText)  # Removes the last word   
                            elif button.text in {'LrC','UpC','Clr','Ent'}:
                                pass
                            else:
                                findText+=button.text
                            sleep(0.25)
                        
                else:
                    if x <(allhands[0]["lmList"][8][0]) < (x+w) and y<(allhands[0]["lmList"][8][1])<y+h:
                        cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),(200,100,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                        index4=(allhands[0]["lmList"][4][0],allhands[0]["lmList"][4][1])
                        index12=(allhands[0]["lmList"][12][0],allhands[0]["lmList"][12][1])
                        l,_,_=detector.findDistance(index4,index12,img)
                        if l<30:
                            keyboard.press(button.text)
                                
                            cv2.rectangle(img,button.pos,(x+w,y+h),(255,255,0),cv2.FILLED)
                            cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.

                            findText+=button.text
                            sleep(0.25)
        else:
            for button in buttonlist:
                x,y=button.pos
                w,h=button.size
                
                if button.text in {'Sp','Clr','LrC','UpC','Ent'}:
                    if (x+100*index[button.text])<(allhands[0]["lmList"][8][0]) < (x+150+100*index[button.text]) and y<(allhands[0]["lmList"][8][1])< (y+h):
                        cv2.rectangle(img,(x+(100*index[button.text])-5,y-5),(x+150+5+(100*index[button.text]),y+h+5),(200,100,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+15+(100*index[button.text]),y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                        index4=(allhands[0]["lmList"][4][0],allhands[0]["lmList"][4][1])
                        index12=(allhands[0]["lmList"][12][0],allhands[0]["lmList"][12][1])
                        l,_,_=detector.findDistance(index4,index12,img)
                        if l<30:
                            if button.text=='Sp':
                                keyboard.press(Key.space)
                                # keyboard.release(Key.space)
                            if button.text=='Clr':
                                keyboard.press(Key.backspace)
                                # keyboard.release(key.backspace)
                            if button.text=='Ent':
                                keyboard.press(Key.enter)    
                            if button.text=='UpC':
                                Uppercase=True
                                                        
                            # keyboard.press(button.text)
                            cv2.rectangle(img,(x+(100*index[button.text])-5,y-5),(x+150+5+(100*index[button.text]),y+h+5),(255,255,0),cv2.FILLED)
                            cv2.putText(img,button.text,(x+15+(100*index[button.text]),y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                            if button.text=='Sp':
                                findText+=" "
                            elif button.text=='Clr' and findText:
                                findText=findText.split()
                                findText[-1]=findText[-1][:-1]
                                findText = " ".join(findText)  # Removes the last word   
                            elif button.text in {'LrC','UpC','Clr','Ent'}:
                                pass
                            else:
                                findText+=button.text
                            sleep(0.25)
                        
                else:
                    if x <(allhands[0]["lmList"][8][0]) < (x+w) and y<(allhands[0]["lmList"][8][1])<y+h:
                        cv2.rectangle(img,(x-5,y-5),(x+w+5,y+h+5),(200,100,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                        index4=(allhands[0]["lmList"][4][0],allhands[0]["lmList"][4][1])
                        index12=(allhands[0]["lmList"][12][0],allhands[0]["lmList"][12][1])
                        l,_,_=detector.findDistance(index4,index12,img)
                        if l<30:
                            keyboard.press((button.text).lower())
                                
                            cv2.rectangle(img,button.pos,(x+w,y+h),(255,255,0),cv2.FILLED)
                            cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
                            findText+=(button.text).lower()
                            sleep(0.25)
    cv2.rectangle(img,(100,520),(1200,595),(100,100,0),cv2.FILLED)
    cv2.putText(img,findText,(100,575),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,255,255),3,cv2.FILLED)  # tcv2.putText() places the text based on the bottom-left corner of the text instead of the center.
    
    cv2.imshow("Image",img) # the window opens it's not the macbook's camera window ,this is created by cv2
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows() # cv2.imshow opens image window ,needed to be destroyedq