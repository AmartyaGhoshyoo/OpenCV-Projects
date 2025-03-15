import time
import math
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# import os 
# os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import cv2 
import HandTrackingModule as htm
detector=htm.HandDetector(detconf=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetVolumeRange()

cap=cv2.VideoCapture(0) #Access a video stream
cW,cH=640,480
cap.set(3,cW)
cap.set(4,cH)
ct,pt=0,0
while True:
    success,img=cap.read() # It is the actual one which capture a frame form the video stream
    img=detector.findhand(img)
    lists=detector.findposition(img)
    if len(lists)!=0:
        x1,y1=lists[4][1],lists[4][2]
        x2,y2=lists[8][1],lists[8][2]
        x3,y3=lists[12][1],lists[12][2]
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)
        xm,ym=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(xm,ym),15,(255,255,0),cv2.FILLED)
        
        line_len=math.hypot(x2-x1,y2-y1)
        line_len_new=math.hypot(x3-x2,y3-y2)
        cv2.rectangle(img,(50,150),(85,400),(0,0,255),3)
        print(line_len_new)
        if line_len<50:
            cv2.circle(img,(xm,ym),15,(0,0,0),cv2.FILLED)
        vol_bar=np.interp(line_len,[50,300],[400,150])     
        cv2.rectangle(img,(50,int(vol_bar)),(85,400),(0,0,255),cv2.FILLED)
        if line_len_new>50:
            
            vol=np.interp(line_len,[50,300],[-65.25,0.0]) 
   
            #interp generally refers to interpolation
            #-65.25(min),0.0(max) is the range from volume.GetVolumeRange()
            #our goal were to put the line_len in that range
           
            """   
            1. numpy.interp() - 1D Linear Interpolation
            Used to interpolate values in a dataset.

            python
            Copy
            Edit
            import numpy as np

            x = [1, 2, 3]        # Known x-values
            y = [10, 20, 30]     # Corresponding y-values
            x_new = 2.5          # New x-value to interpolate

            y_new = np.interp(x_new, x, y)
            print(y_new)  # Output: 25.0 (Interpolates between 20 and 30)
            Explanation:
            It estimates y_new at x_new=2.5 by linearly interpolating between (2,20) and (3,30).
            """
            volume.SetMasterVolumeLevel(vol, None) # this function will change the volume with our hand gesture by calling the Audio API
            print(line_len,vol)
    ct=time.time()
    fps=1/(ct-pt)
    pt=ct
    cv2.putText(img,f'FPS:{int(fps)}',(40,60),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()