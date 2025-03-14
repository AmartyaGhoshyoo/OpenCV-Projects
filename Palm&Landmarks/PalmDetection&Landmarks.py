import cv2
import mediapipe as mp
import time
import numpy as np
import mediapipe as mp # MediaPipe is an open-source framework for building pipelines to perform computer vision inference over arbitrary sensory data such as video or audio
mphands=mp.solutions.hands# calling the solutions,inside it the hands module
hands=mphands.Hands() # Hands class Loads the pretrained model trained on huge datasets of hand images in 3D which detect hand in image or in the real time and predict 21 key landmarks points on hand
"""
It loads a pre-trained deep learning model that:
✔ Detects whether a hand exists in the frame.
✔ Uses CNN-based weights to estimate 21 landmarks.
✔ Works on single or both hands simultaneously.
✔ Can handle different orientations and lighting conditions.
The model estimates (x, y, z) coordinates for each landmark:

x, y → Represent 2D pixel locations in the image.
z → Represents the relative depth of the landmark compared to the wrist.

"""
mpDraw=mp.solutions.drawing_utils# draw the predicted landmarks and connection on the image
ct,pt=0,0 #Current time and previous time 
cap=cv2.VideoCapture(0) # It is used to create a video capture object to access a video stream.
'''
    The argument inside VideoCapture() determines the source of the video:
0 → Default webcam.
1 → Second camera (if an external camera is connected, it is usually assigned index 1).
It can also take a video file path instead of an index to read from a pre-recorded video.

'''
while True: 
    success,img=cap.read() # captures a frame from the video stream. Returns 
    #It returns two values:
    #success → A boolean (True if a frame was successfully captured, False otherwise).
    #img → The captured frame (a NumPy array representing the image). Always read in BGR format
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #Convert the color from BGR fromate to RGB because hand.process only RGB
    result=hands.process(imgRGB)# Process the image with hand detection and 21 key landmarks prediction on the hand 
    # """
    # results.multi_hand_landmarks is an attribute of the results object returned by hands.process(image). It contains the landmark coordinates for all detected hands in an image.
    # 1️⃣ What Does It Store?
    # If hands are detected, it stores a list of landmark objects, where each object represents one detected hand.
    # If no hands are detected, it returns None.
    # Each hand consists of 21 landmarks, where each landmark has (x, y, z) coordinates.


    # """
    #NOTE
    #The below code runs or process only for one photo or frame that was captured, it detects hands on that one photo and draw landmarks print co ordinates and all for that one frame only .. video is nothing but continuous photos or frames 
    if result.multi_hand_landmarks:
        for handlmks in result.multi_hand_landmarks: # here handmlks is the object in multi_hand_landmarks atribute in a list [object1,object2,...] ,handmks become that object
            #When MediaPipe detects a hand, it stores 21 landmarks in handlmks.landmark as a list of objects, where each object has x, y, and z attributes.
            for id,lm in enumerate(handlmks.landmark): #here handmlks also has attribute named landmark which also contains objects for 21 landmarks by lm the object is copied in the variable "lm"
                h,w,_=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h) #accessing the object from landmark which is now indentified by lm and we are accesing the lm.x attribute , it is actually like a class which has constructor and lm is being passed to self parameter in the __init__ which has self.x and all so like lm.x,lm.y and lm.z
                """     
                handlmks.landmark = [
                NormalizedLandmark(x=0.5, y=0.6, z=-0.03),  # Wrist (index 0) # So lm becoms objects of this class
                NormalizedLandmark(x=0.52, y=0.58, z=-0.02), # Thumb CMC (index 1)
                NormalizedLandmark(x=0.55, y=0.57, z=-0.01), # Thumb MCP (index 2)
                ...
                NormalizedLandmark(x=0.65, y=0.35, z=-0.05)  # Index Tip (index 8)

                """
                print(f"Landmarks[{id}]: {cx} and {cy}")
                if id==0:
                    cv2.circle(img,(cx,cy),20,(0,0,255),cv2.FILLED)
            mpDraw.draw_landmarks(img,handlmks,mphands.HAND_CONNECTIONS)#Since draw_landmarks() only plots these fixed coordinates, it doesn’t depend on color format.
    ct=time.time()
    fps=1/(ct-pt)
    pt=ct
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),3)
     # the whole upper code executed by drawing the landmarks, circle on the captured photo or frame then after we see this image 
     # and it processes so fast that we see like real time video for every frame or photo               
    cv2.imshow("Img",img) # Displays the captured frame in a window named "Img".
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # It waits 1 miliseconds for key press then continues automatically again to capture the next frame, 
    #if 0 was given then until and unless someone press key the next frame won't be captured it will be paused 
    #The video will pause at the current frame until the user presses any key.
    #Once a key is pressed, it will move to the next frame.
    """
    cv2.waitKey(x)	    Effect
    cv2.waitKey(0)	    Waits indefinitely until a key is pressed (pauses on a frame).
    cv2.waitKey(1)	    Plays video continuously, waiting only 1ms(mili seconds) per frame.
    cv2.waitKey(30)	    Slows down video playback to ~30 FPS.
    cv2.waitKey(100)	Slows down playback to ~10 FPS.
    Understanding cv2.waitKey() and FPS
        
        
    The frame rate depends on:

    The waitKey() delay (time per frame)
    The processing time per frame (model inference, display, etc.)
    The actual FPS of the video source (e.g., webcam, file, etc.)

    Case 1: cv2.waitKey(33) → 30 FPS
    If we assume no other delays, cv2.waitKey(33) makes each iteration of the loop take at least 33 milliseconds.
    Since 1 second = 1000 ms, the number of frames displayed per second is:
    1000/33≈30
     FPS331000≈30 FPS

    This works well when processing is very fast.

    Case 2: cv2.waitKey(1) Doesn't Guarantee 1000 FPS
    If you use cv2.waitKey(1), in theory, it waits only 1 ms, meaning at most 1000 FPS.
    However, the actual FPS depends on processing speed.
    If reading and processing a frame takes 30 ms, the real FPS will be around 33 FPS, not 1000.

    Why cv2.waitKey(1) Can Still Give ~30 FPS?
    Even though cv2.waitKey(1) waits for only 1 ms, processing the frame (reading, detection, displaying) takes time.
    If total loop time = 33 ms (frame read + detection + display), then FPS ≈ 30.
    If processing is much faster (e.g., 5 ms per frame), FPS could be higher.
        
    """
cap.release() #closes the webcam.
cv2.destroyAllWindows() #closes the OpenCV window.
