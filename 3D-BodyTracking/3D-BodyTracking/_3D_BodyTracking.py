import cv2 as cv
import mediapipe as mp
import time
import socket

width, height = 1280, 720

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

pTime = 0
lmList = []
for i in range(33): lmList.append(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ('127.0.1.60', 5055)

while True:
    success, img = cap.read()
    imageRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = pose.process(imageRGB)
    #print(results.pose_landmarks)

    data = []
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        #print(results.pose_landmarks.landmark)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            #print('c: ',c,'h: ',h,'w: ',w)
            cx, cy, cz = int(lm.x*w), int(lm.y*h), int(lm.z*w)
            cv.circle(img, (cx,cy), 5, (255,0,255), cv.FILLED)
            lmList[id] = [cx,cy,cz]
            #print(lmList)
        for lm in lmList:
            data.extend([lm[0], height-lm[1], lm[2]])
        print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (70,50), cv.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    img = cv.resize(img, (0, 0), None, 0.3, 0.3)
    cv.imshow('Image', img)
    cv.waitKey(1)

