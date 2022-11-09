import cv2 
import mediapipe as mp
from time import *

class HandDetection():
    def __init__(self, mode=False, maxHands=2, modelComplexity = 1, detectionCon=float(0.5), trackCon=float(0.5)):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

 


    def tracking(self, image, draw = True):

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(image_rgb)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
        return image

    def positions(self, img, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmlist

def main():
    cap = cv2.VideoCapture(0)
    handtrack = HandDetection()
    while True:
        success, img = cap.read()
        img = handtrack.tracking(img)
        lmlist = handtrack.positions(img)
        if len(lmlist) != 0:
            print(lmlist[4])
        cv2.imshow("Hand Tracking", img)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()