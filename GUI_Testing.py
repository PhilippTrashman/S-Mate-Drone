from tkinter import *
from tkinter import messagebox
from spacenavigator import *
from xbox_controller import *
from PIL import Image, ImageTk
from GestureandFaceTracking import * 
import mediapipe as mp

def connect():
    tello = Tello()
    tello.connect

def controll(schmuggel):

    print(schmuggel)

def controll_selection():
    root = Tk()
    root.title("Controller Selection")
    root.geometry('250x100')

    label = LabelFrame(root, text='Choose your input method') 
    label.pack(expand = "yes", fill="both")

    v = StringVar(root, "1")

    cont_types = {"Xbox" : "1", "Spacemouse" : "2"}

    xbox_btn = Radiobutton(root, text = "Xbox", variable = v,
                    value = "1", indicator = 0,
                    background = "light blue", command= lambda: controll("xbox")).pack(fill = X, ipady = 5)
    
    space_btn = Radiobutton(root, text= "Space Mouse", variable= v,
                    value= "2", indicator = 0,
                    background= "light blue", command= lambda: controll("space")).pack(fill= X, ipady= 5)

def xbox():
    print("xbox controlls")
    flight_xbox()

def btn_e(wind):
    btn_exit = Button(wind, text="Exit", width=10, height=2, command=wind.quit)
    return btn_exit

def menu_buttons():
    mb =  Menubutton ( win, text = 'Menu') 
    mb.grid() 
    mb.menu  =  Menu ( mb, tearoff = 0 ) 
    mb['menu']  =  mb.menu
    var1 = IntVar() 
    var2 = IntVar() 
    var3 = IntVar()
    mb.menu.add_checkbutton ( label ='Settings', variable = var1 ) 
    mb.menu.add_checkbutton ( label = 'Profile', variable = var2 ) 
    mb.menu.add_checkbutton ( label = 'Sign Out', variable = var3 ) 
    mb.pack() 

def menus(window):
    mn = Menu(window) 
    window.config(menu=mn) 
    file_menu = Menu(mn) 
    mn.add_cascade(label='File', menu=file_menu) 
    file_menu.add_command(label='New') 
    file_menu.add_command(label='Open...') 
    file_menu.add_command(label='Save') 
    file_menu.add_separator() 
    file_menu.add_command(label='Settings', command=controll_selection) 
    file_menu.add_separator() 
    file_menu.add_command(label='Exit', command=window.quit) 
    help_menu = Menu(mn) 
    mn.add_cascade(label='Help', menu=help_menu) 
    help_menu.add_command(label='Feedback') 
    help_menu.add_command(label='Contact') 

def scale (window):
    sc1= Scale(window, from_=100, to=10, sliderlength= 50, length= 250, width= 25) 
    sc1.pack() # Must implement speed controll with drone (set_speed(x))

def throttle(val):
    val = int(val)
    tello = Tello()
    tello.set_speed(val)
    print(val)

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

if __name__ == "__main__":
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
    btn_con.pack(side='top', anchor=NW)
    btn2.pack(side='top', anchor=NW)
    lmain.pack(side='left', anchor=CENTER)
    

    hand_track()
    root.mainloop()