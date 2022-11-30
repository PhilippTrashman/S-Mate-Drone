import cv2 
import mediapipe as mp
from djitellopy import Tello
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
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
        return image




    def positions(self, img, handNo=0, draw=True):
        self.lmlist = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return self.lmlist




    def tellocontroll(self, tello, speed):
        liste = self.lmlist
        if len(liste) != 0:

            #Distance between Index Finger Tip and Index Finger MCP
            if (liste[8][2]-liste[5][2]) < 150 and (liste[8][2]-liste[5][2]) > -150 and (liste[8][1]-liste[5][1]) < 150 and (liste[8][1]-liste[5][1]) > -150:

                #Distance between Thumb Tip and Pinky Tip bigger than 300(x-Achsis)?
                if (liste[4][1]-liste[20][1]) > 300 or (liste[4][1]-liste[20][1]) < -300:
                    
                    #Is Thumb to the left or the right of Pinky 
                    if liste[4][1] < liste[20][1] and (liste[17][2]-liste[20][2]) < 100:
                        tello.send_rc_control(-speed, 0, 0, 0)
                    
                    elif liste[4][1] > liste[20][1] and (liste[17][2]-liste[20][2]) < 100:
                        tello.send_rc_control(speed, 0, 0, 0)
                
                #Distance between Thumb Tip and Pinky Tip smaller than 300 (x-Achsis)?
                elif (liste[4][1]-liste[20][1]) < 300 or (liste[4][1]-liste[20][1]) > -300:
                    
                    #Is Thumb over or under Pinky (y-Achsis)
                    if liste[4][2] < liste[20][2] and (liste[17][1]-liste[20][1]) < 100:
                        tello.send_rc_control(0, 0, speed, 0)
                    
                    elif liste[4][2] > liste[20][2] and (liste[17][1]-liste[20][1]) < 100:
                        tello.send_rc_control(0, 0, -speed, 0)
            
            #Distance between Index Finger Tip and Index Finger MCP below 300 (both Achsis)
            elif (liste[8][2]-liste[5][2]) > 150 or (liste[8][2]-liste[5][2]) < -150 and (liste[12][2]-liste[9][2]) < 100 and (liste[12][2]-liste[9][2]) > -100:
                
                if (liste[8][1]-liste[0][1]) < 300 or (liste[8][1]-liste[0][1]) > -300:
                    if liste[8][2] > liste[5][2]:
                        tello.send_rc_control(0, -speed, 0, 0)
                    elif liste[8][2] < liste[5][2]:
                        tello.send_rc_control(0, speed, 0, 0)
            else:
                if (liste[12][2]-liste[9][2]) < 100 and (liste[12][2]-liste[9][2]) > -100:
                    if liste[8][1] > liste[0][1]:
                        tello.send_rc_control(0, 0, 0, speed)
                    else:
                        tello.send_rc_control(0, 0, 0, -speed)
                else:
                    tello.send_rc_control(0, 0, 0, 0)
        else:
            tello.send_rc_control(0, 0, 0, 0)






def main():
    tello = Tello()
    #tello.connect()
    #tello.streamoff()
    #tello.streamon()
    cap = cv2.VideoCapture(0)
    handtrack = HandDetection()
    help = 0
    while True:
        success, img = cap.read()
        img = cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)
        img = handtrack.tracking(img)
        lmlist = handtrack.positions(img)
        #if len(lmlist) != 0:
            #print(lmlist[8])
            #print(lmlist[12])
        if help == 0:
            #tello.takeoff()
            help += 1
        handtrack.tellocontroll(tello, 100) #Integer refers to speed (0-100)

        cv2.imshow("Hand Tracking", img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            tello.streamoff()
            cv2.destroyAllWindows()
            cv2.waitKey(1)
            break
    tello.land()
    tello.streamoff()




if __name__ == "__main__":
    main()