import math
import threading
from tkinter import *  # type: ignore

import cv2
import easygui
import mediapipe as mp
from djitellopy import Tello
from inputs import get_gamepad
from PIL import Image, ImageTk

from spacenavigator import Space_call


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0
        # Dpad Fix
        self.DPadY = 0
        self.DPadX = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self):
        """returns the Xbox Controller Inputs, can be called to check if the controller works, but shouldnt get called
        """
        left_y = self.LeftJoystickX
        left_x = self.LeftJoystickY
        right_y = self.RightJoystickY
        right_x = self.RightJoystickX
        # Buttons
        a = self.A
        x = self.X
        b = self.B
        y = self.Y
        # D pad
        
        Dpad_x = self.DPadX
        Dpad_y = self.DPadY
        # Bumbers
        rb = self.RightBumper
        rt = self.RightTrigger
        lb = self.LeftBumper
        lt = self.LeftTrigger
        # Extras
        start = self.Start
        select = self.Back

        # Extra for spacenavigator to controll lift
        extra = self.RightTrigger - self.LeftTrigger
        return [left_y, left_x, right_y, right_x, a, x, y, b, Dpad_x, Dpad_y, rb, rt, lb, lt, start, select, extra]


    def _monitor_controller(self):
        """is used to monitor the events by the Controller and sort them for the read(self) function"""
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state #previously switched with X
                elif event.code == 'BTN_WEST':
                    self.X = event.state #previously switched with Y
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state
                # DPad Fix
                elif event.code == 'ABS_HAT0X':
                    self.DPadX = event.state
                elif event.code == 'ABS_HAT0Y':
                    self.DPadY = event.state

    def flight_xbox(self, tello, help):
        """Used as the main Controll function for the drone, needs more jokes"""
        cont = self

        print(cont.read())
        if cont.read()[15] == 1:
            easygui.msgbox("Press 'Ok' to engage throw takeoff",title="Info")
            tello.initiate_throw_takeoff()
            help = 1
        elif cont.read()[14] == 1 and help == 0:
            tello.takeoff()
            help = 1
            print("Takeoff")
        elif cont.read()[14] == 1 and help != 0:
            tello.land()
        elif cont.read()[9] == 1:
            tello.flip("b")
        elif cont.read()[8] == -1:
            tello.flip("l")
        elif cont.read()[9] == -1:
            tello.flip("f")
        elif cont.read()[8] == 1:
            tello.flip("r")
        tello.send_rc_control(int(cont.read()[0]*100), int(cont.read()[1]*100), int(cont.read()[16]*100), int(cont.read()[3]*100))

class GUI_mate():

    def init(self, window, drone_state:bool):
        """Is the Starting point for the UI, calling if the DJI Drone is enabled, later optional Activation should be implemented"""
        print('Started!')

        tello = Tello()
        print('Init UI...')
        root = window
        root.title("S.Mate Drone")
        root.bind('<Escape>', lambda e: root.quit())

        print('UI initialized!')

        if drone_state == True:
            tello.connect()
        
        else:
            print("Tello disabled")

    def init_camera(self, label: Label, cam_state: bool):    # Does not work when called as a function initself
        """NOT WORKING, DONT USE!"""
        width, height = 800, 600
        lmain = label
        if cam_state == True:
            print('Init cap...')
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            print('Cap initialized!')
            self.hand_track(lmain, cap)

    def menus(self, window:Tk):    #Currently deprecated and not used in current build
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

    def scale (self, window: Tk):   # Scale will be implemented seperatly in Buttons
        sc1= Scale(window, from_=100, to=10, sliderlength= 50, length= 250, width= 25) 
        sc1.pack() # Must implement speed controll with drone (set_speed(x))

    def throttle(self, val, tello:Tello):
        """Used in conjunction with a Tkinter Scale to Throttle the speed the DJI Drone"""
        val = int(val)
        tello.set_speed(val)
        print(val)

    def hand_track(self, label: Label, capture):
        """Older version of the Hand Tracking developed by Calvin (and Google), label = placement as a label widget, cap = camera """
        lmain = label
        cap = capture
        mp_drawing = mp.solutions.drawing_utils   # type: ignore
        mp_drawing_styles = mp.solutions.drawing_styles   # type: ignore
        mphands = mp.solutions.hands   # type: ignore
        hands = mphands.Hands()
        data,image=cap.read()
        image = cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
        result = hands.process(image)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)
        img = Image.fromarray(image)   # type: ignore
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk # type: ignore
        lmain.configure(image=imgtk)
    
    def buttons(self, v: StringVar,throt: IntVar, label: Label, window: Tk):
        """Buttons used by the main Window, v is a variable used to controll the actions taken by the menu, label is for the Hand Tracking Camera and window is the... well window"""

        colour_lib = {"light bluish Grey":"#D6E0EF", "light Grey" : "#ededed"}
        print("Creating buttons...")
        lmain = label
        root = window
        r_btn_frame = Frame(window, background= "#ededed", width= 20, padx=5)
        r_btn_frame.pack(side='left', fill=Y)

        l_btn_frame = Frame(window, background= "#ededed", width= 20, padx=5)
        l_btn_frame.pack(side='right', fill=Y)

        low_scale_frame = Frame(window, background= "#ededed", height= 60, pady= 5)
        low_scale_frame.pack(side='bottom', fill= X)

        # Radiobuttons used to switch between Controll modes, still not very pretty...
        xbox_btn = Radiobutton(root, text = "Xbox", variable = v, value = "1", indicator = 0, background = "#D6E0EF", height=1, width= 15)   # type: ignore
        space_btn = Radiobutton(root, text= "Space Mouse", variable= v, value= "2", indicator = 0, background = "#D6E0EF", height=1, width= 15)   # type: ignore
        face_btn = Radiobutton(root, text= "Face Tracking", variable= v, value= "3", indicator = 0, background = "#D6E0EF", height=1, width= 15)   # type: ignore
        gest_btn = Radiobutton(root, text= "Gesture Tracking", variable= v, value= "4", indicator = 0, background = "#D6E0EF", height=1, width= 15)   # type: ignore

        # Different Buttons that are still unfinished
        btn_con = Button(root, text="connect", width=10, height=2, background= '#D6E0EF')
        btn_exit = Button(root, text="Exit", width=10, height=2, background= "#58181F", command = root.destroy)

        # Different Scales used to visualize Drone speed and Throttle controll
        throt_sca = Scale(window, from_=100, to = 10, sliderlength = 50, length= 250, width= 25, variable = throt)

        accel_sca = Scale(window, from_=10, to = 100, sliderlength = 50, length= 250, width= 25, orient='horizontal')
        speed_sca = Scale(window, from_=10, to = 100, sliderlength = 50, length= 250, width= 25, orient='horizontal')
        # Placing everything
        xbox_btn.pack(side='bottom', in_= r_btn_frame)
        space_btn.pack(side='bottom', in_= r_btn_frame)
        face_btn.pack(side='bottom', in_= r_btn_frame)
        gest_btn.pack(side='bottom', in_= r_btn_frame)

        throt_sca.pack(side='right', anchor = N, in_ = l_btn_frame)
        accel_sca.pack(side='bottom', anchor=CENTER, in_= low_scale_frame)
        speed_sca.pack(side='bottom', anchor=CENTER, in_= low_scale_frame)

        btn_con.pack(side='left', anchor=N, in_ = r_btn_frame)
        btn_exit.pack(side='bottom', anchor=E, in_= l_btn_frame)
        lmain.pack(anchor=CENTER)
        print("buttons created")
