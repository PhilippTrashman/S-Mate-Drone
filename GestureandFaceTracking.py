import cv2
from djitellopy import Tello
from time import sleep
import mediapipe as mp


def resize(image):
    resized = cv2.resize(image, (600, 400), interpolation=cv2.INTER_LINEAR)
    return resized

def gray(image):
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_frame

def controlling(tello, faces, distance):
    width_middle = 300
    height_middle = 200
    
    #yaw Abfrage
    if (faces[0][0]-width_middle)/4 > 100:
        controll_yaw = 100
    elif (faces[0][0]-width_middle)/4 < -100:
        controll_yaw = -100
    else:
        controll_yaw = int((faces[0][0]-width_middle)/4)

    #Height Abfrage
    if (height_middle-faces[0][1])/3 > 100:
        controll_updown = 100
    elif (height_middle-faces[0][1])/3 < -100:
        controll_updown = -100
    else:
        controll_updown = int((height_middle-faces[0][1])/3)
    
    #Offset Abfrage
    if distance >= 7:
        offset = 15
    else:
        offset = 5

    #Front Back Abfrage
    if faces[0][2] > (distance*10+offset):
        controll_frontback = -15
    elif faces[0][2] < (distance*10+offset) and faces[0][2] > (distance*10):
        controll_frontback = 0
    elif faces[0][2] < (distance*10):
        controll_frontback = 15
    else:
        controll_frontback = 0

    #Zusammenführung der Signale
    tello.send_rc_control(0, controll_frontback, controll_updown, controll_yaw)
    
    
    
        

def face_track_fly(tello, distance):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        frame = tello.get_frame_read().frame
        frame = resize(frame)
        gray_image = gray(frame)
        detected_faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
        print(detected_faces)
        for (x, y, w, h) in detected_faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
        if len(detected_faces) != 0:
            controlling(tello, detected_faces, distance)
        else:
            tello.send_rc_control(0, 0, 0, 0)
        cv2.imshow("Detection", frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        sleep(1/30)


def hand_tracking():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mphands = mp.solutions.hands
    

    capturing = cv2.VideoCapture(0)
    hands = mphands.Hands()

    while True:
        data,image=capturing.read()

        image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)
        cv2.imshow("Handtracking", image)
        cv2.waitKey(1)

