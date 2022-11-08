from tkinter import *
import cv2
from PIL import Image, ImageTk
from time import sleep
import mediapipe as mp

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = Tk()
root.title("S.Mate Drone")
root.bind('<Escape>', lambda e: root.quit())
lmain = Label(root)

btn2 = Button(root, text = "Xbox", width=10, height=2)
btn_con = Button(root, text="connect", width=10, height=2)
btn_exit = Button(root, text="Exit", width=10, height=2, background= "red")
btn_con.grid(column=0, row=1)
btn2.grid(column=0, row=0)
lmain.grid(column=1, row=0)

def hand_track():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mphands = mp.solutions.hands
    hands = mphands.Hands()

    data,image=cap.read()
    image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    result = hands.process(image)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)
    img = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, hand_track)

hand_track()
root.mainloop()