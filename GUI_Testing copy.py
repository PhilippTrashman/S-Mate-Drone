from tkinter import *
from tkinter import messagebox
from spacenavigator import *
from xbox_controller import *
from PIL import Image, ImageTk
from GestureandFaceTracking import * 
import mediapipe as mp

class GUI_mate():

    def init(self, window, cam_state:bool, drone_state:bool, lmain):
        print('Started!')
        width, height = 800, 600
        tello = Tello()
        print('Init UI...')
        root = window
        root.title("S.Mate Drone")
        root.bind('<Escape>', lambda e: root.quit())

        print('UI initialized!')
        if cam_state == True:
            print('Init cap...')
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            print('Cap initialized!')
            self.hand_track(lmain, cap)
        
        else:
            print("cam disabled")

        if drone_state == True:
            tello.connect()
        
        else:
            print("Tello disabled")

    def menus(self, window):
        mn = Menu(window) 
        window.config(menu=mn) 
        file_menu = Menu(mn) 
        mn.add_cascade(label='File', menu=file_menu) 
        file_menu.add_command(label='New') 
        file_menu.add_command(label='Open...') 
        file_menu.add_command(label='Save') 
        file_menu.add_separator() 
        file_menu.add_command(label='Settings') 
        file_menu.add_separator() 
        file_menu.add_command(label='Exit', command=window.quit) 
        help_menu = Menu(mn) 
        mn.add_cascade(label='Help', menu=help_menu) 
        help_menu.add_command(label='Feedback') 
        help_menu.add_command(label='Contact') 

    def scale (self, window):
        sc1= Scale(window, from_=100, to=10, sliderlength= 50, length= 250, width= 25) 
        sc1.pack() # Must implement speed controll with drone (set_speed(x))

    def throttle(self, val):
        val = int(val)
        tello = Tello()
        tello.set_speed(val)
        print(val)

    def hand_track(self, label, cap):
        lmain = label
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
        lmain.after(10, self.hand_track)
    
    def buttons(self, v, label, window):
        print("placing buttons...")
        lmain = label

        xbox_btn = Radiobutton(root, text = "Xbox", variable = v, value = "1", indicator = 0, background = "#D6E0EF", height=1, width= 15)
        space_btn = Radiobutton(root, text= "Space Mouse", variable= v, value= "2", indicator = 0, background = "#D6E0EF", height=1, width= 15)
        face_btn = Radiobutton(root, text= "Face Tracking", variable= v, value= "3", indicator = 0, background = "#D6E0EF", height=1, width= 15)
        gest_btn = Radiobutton(root, text= "Gesture Tracking", variable= v, value= "4", indicator = 0, background = "#D6E0EF", height=1, width= 15)

        btn_con = Button(root, text="connect", width=10, height=2, background= '#D6E0EF')
        btn_exit = Button(root, text="Exit", width=10, height=2, background= "#58181F", command = window.destroy)
        xbox_btn.pack(side='bottom', anchor= W)
        space_btn.pack(side='bottom', anchor= W)
        face_btn.pack(side='bottom', anchor= W)
        gest_btn.pack(side='bottom', anchor= W)

        btn_con.pack(side='left', anchor=N)
        btn_exit.pack(side='right', anchor=S)
        lmain.pack(anchor=CENTER)
        print("buttons placed")


if __name__ == "__main__":
    start = GUI_mate()
    tello = Tello()
    root = Tk()
    lmain = Label(root)
    start.init(root, False, False, lmain)

    cont_var = StringVar(root, "0")

    start.buttons(cont_var, lmain, root)

    joy = XboxController()
    help = 0
    xbox_flag = False
    space_flag = False
    while True:
        if root.state() != 'normal':
            root.destroy()

        controller = cont_var.get()

        if controller == "1":
            joy.flight_xbox(tello, help)
            print(joy.read())

        elif controller == "2":
            if space_flag == False:
                dev = open(callback=None, button_callback=toggle_led)
                space_flag = True

            elif space_flag == True:
                flight(tello, help)

        elif controller == "3":
            print("Face tracking")
        
        elif controller == "4":
            print("Gesture tracking")
        
        root.update()
        sleep(0.001)



    # root.after(1, xbox)

    # root.mainloop()