import math
import threading
from tkinter import *  # type: ignore
from tkinter import messagebox
import subprocess

import cv2
import easygui
import mediapipe as mp
from djitellopy import Tello
from inputs import get_gamepad
from PIL import Image, ImageTk
from time import sleep
from src.spacenavigator import Space_call

COOLGRAY = '#3B3730'
SAGE = '#9D9480'
NUDE = '#8C7460'
MONOBLACK = '#171717'
RED = '#58181F'
WHITE = '#FDFDFD' 

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
        """returns the Xbox Controller Inputs, can be called to check if the controller works, but shouldnt get called \n
        left Stick  y = 0, x = 1 | right Stick = y/2, x/3 | A = 4 | X = 5| Y = 6 | B = 7| Dpad x = 8, y = 9 | RB = 10 | RT = 11 |
        LB = 10 | LT = 13 | start = 14 | select = 15| RT - LT = 16 |        
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
        # left Stick  y = 0, x = 1 | right Stick = y/2, x/3 | A = 4 | X = 5| Y = 6 | B = 7| Dpad x = 8, y = 9 | RB = 10 | RT = 11 |
        # LB = 12 | LT = 13 | start = 14 | select = 15| RT - LT = 16 |
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

    def flight_xbox(self, tello: Tello, helper, speed: int, cam_direction: int):
        """Used as the main Controll function for the drone, needs more jokes, uses the GTA Controll Setup
        returnes Helper for Landing, Left/right, back/forth, up/down, yaw"""
        cont = self

        # print(cont.read())
        if cont.read()[14] == 1:
            easygui.msgbox("Press 'Ok' to engage throw takeoff",title="Info")
            tello.initiate_throw_takeoff()
            helper = 1

        elif cont.read()[15] == 1 and helper == 0:  # Takeoff
            try:
                tello.takeoff()
                helper = 1
                print("Takeoff")
            except:
                pass

        elif cont.read()[15] == 1 and helper != 0:  # Landing
            try:
                tello.land()
                helper = 0
                print("landing")
            except:
                pass

        elif cont.read()[9] == 1:   # Backwards Flip
            try:
                tello.flip("b")
            except:
                pass

        elif cont.read()[8] == -1:  # Left Flip
            try:
                tello.flip("l")
            except:
                pass

        elif cont.read()[9] == -1:  # Forward Flip
            try:
                tello.flip("f")
            except:
                pass

        elif cont.read()[8] == 1:   # Right Flip
            try:
                tello.flip("r")
            except:
                pass

        elif cont.read()[10] == 1 and cont.read()[5] == 1:  # Enters "Funni mode", shuts down the Motors
            try:
                helper = 0
                tello.emergency()
            except:
                pass

        tello.send_rc_control(int(cont.read()[0]*speed), int(cont.read()[1]*speed), int(cont.read()[16]*speed), int(cont.read()[3]*100))
        return helper, cam_direction
        
    def flight_xbox_classic(self, tello: Tello, helper: int, speed :int, cam_direction: int):
        """More Classic Drone Controll, as requested
        returnes Helper for Landing, Left/right, back/forth, up/down, yaw"""
        cont = self

        # print(cont.read())
        if cont.read()[14] == 1:
            easygui.msgbox("Press 'Ok' to engage throw takeoff",title="Info")
            tello.initiate_throw_takeoff()
            helper = 1

        elif cont.read()[15] == 1 and helper == 0:
            try:
                tello.takeoff()
                helper = 1
                print("Takeoff")
            except:
                pass

        elif cont.read()[15] == 1 and helper != 0:
            try:
                tello.land()
                helper = 0
                print("landing")
            except:
                pass

        elif cont.read()[9] == 1:
            try:
                tello.flip("b")
            except:
                pass

        elif cont.read()[8] == -1:
            try:
                tello.flip("l")
            except:
                pass

        elif cont.read()[9] == -1:
            try:
                tello.flip("f")
            except:
                pass

        elif cont.read()[8] == 1:
            try:
                tello.flip("r")
            except:
                pass

        elif cont.read()[10] == 1 and cont.read()[5] == 1:  # Enters "Funni mode", shuts down the Motors
            try:
                helper = 0
                tello.emergency()
            except:
                pass

        # send_rec_control configuration is left/right, back/forth, up/down, yaw
        tello.send_rc_control(int(cont.read()[3]*speed), int(cont.read()[2]*speed), int(cont.read()[1]*speed), int(cont.read()[0]*100))
        return helper, cam_direction

    def define_speed_xbox(self, current_speed) -> int:
        """For Xbox controll mode!, Returns a value to reduce or increase drone speed for controllers in increments of 5"""
        joy = self
        slower = joy.read()[5]
        faster = joy.read()[6]
        speed = 0
        if faster == 1 and slower == 0:
            speed = 1
        elif slower == 1 and faster == 0:
            speed = -1     

        speed = current_speed + speed
        if speed <= 0:
            speed = 1
        
        elif speed > 100:
            speed = 100
        
        return speed        

    def define_speed_classic(self, current_speed) -> int:
        """For Classic controll mode!, Returns a value to reduce or increase drone speed for controllers in increments of 5"""
        joy = self
        input = joy.read()[16]
        speed = 0
        if input > 0.5:
            speed = 1
        elif input < -0.5:
            speed = -1       

        speed = current_speed + speed
        if speed <= 0:
            speed = 1
        
        elif speed > 100:
            speed = 100       
        return speed
           
class GUI_mate():

    def init(self, window: Tk, drone_state:bool, tello):

        print('Init UI...')
        root = window
        root.title("S.Mate Drone")
        root.bind('<Escape>', lambda e: self.total_annihilation(tello, root))

        print('UI initialized!')

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
            self.hand_track(lmain, cap)     #type: ignore

    def menus(self, window:Tk):    #Currently deprecated and not used in current build
        """Makes Dropdown menus for the window... Use may not actually be necessary"""
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

    def throttle(self, val, tello:Tello):
        """Used in conjunction with a Tkinter Scale to Throttle the speed the DJI Drone"""

        tello.set_speed(val)
        print(val)

    def get_drone_speed(self, tello:Tello,) -> int:
        x_speed = tello.get_speed_x()
        y_speed = tello.get_speed_y()
        z_speed = tello.get_speed_z()

        if x_speed >= y_speed and x_speed >= z_speed:
            return x_speed
        elif y_speed >= x_speed and y_speed >= z_speed:
            return y_speed
        else:
            return z_speed

    def Cam(self, label: Label, capture):    # Replaced by the new HandDetection class
        """Older version of the Hand Tracking developed by Calvin (and Google), label = placement as a label widget, cap = camera """
        lmain = label
        cap = capture

        image = cv2.cvtColor(cv2.flip(cap,1),cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)   # type: ignore
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk # type: ignore
        lmain.configure(image=imgtk)
    
    def drone_stream(self, tello: Tello, cam_direction: int):
        """simple drone video Feed"""

        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (960, 720))

        cv2.imshow("stream", frame)

    def total_annihilation(self, tello: Tello, root:Tk):
        """Just used for the Exit button to actually close all the windows""" 
        try:    
            try:
                tello.end()
            except:
                pass
            cv2.destroyAllWindows()
            root.destroy()
        except:
            pass

    def connection_try(self, tello:Tello):
        try:
            tello.connect()
            tello.streamon()
        except:
            pass
          
    def open_blender(self, button:Button):
        # Opens Blender
        myargs = [
        "C:/Users/itlab/Desktop/blender-3.3.1-windows-x64/blender",     # File Path for the Blender Executable
        "Pictures/Dji-Tello.blend"        # The File Path for the Blend file
        ]
        try:
            blend = subprocess.Popen(myargs, stdin=subprocess.PIPE, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
            button.configure(state='disabled')
        except:
            messagebox.showerror(title="Blender not Found", message="Check if you set the correct filepath for Blender\nChange it if necessary in the GUI.py file")
        

    # Starting the Window
    def buttons(self, v: StringVar,throt: IntVar, web_label: Label,window: Tk, drone_state: StringVar,
        tello: Tello, speed_var: IntVar, face_distance_var: IntVar, battery_var : StringVar,
        height_var: StringVar, time_var : StringVar, temperatur_var: StringVar,
        barometer_var: StringVar, drone_var: IntVar, cam_state: IntVar, fly_flag:IntVar):
        """Alot of Variables are needed but for some reason dictionaries dont work with Tk variables, Buttons used by the main Window, v is a variable used to controll the actions taken by the menu, label is for the Hand Tracking Camera and window is the... well window"""
        drone = drone_state.get()
        colour_lib = {"light bluish Grey":"#D6E0EF", "light Grey" : "#ededed", 'grey 16':'#292929', "mono black": "#171717",
                      "Purple": "#613659", "Beige": "#6F5B3E", "Nude": "#8C7460", "Cool Gray": "#3B3730", "Sage": '#9D9480'}
        print("Creating buttons...")
        lmain = web_label
        lmain.configure(background=MONOBLACK)

        root = window
        root['background'] = MONOBLACK
        # Frames for the Placements of the widgets
        l_frame = Frame(window, background= MONOBLACK, width= 30, padx=5, height=40)
        l_frame.pack(side='left',fill=Y)

        l_up_btn_frame = Frame(window, background=COOLGRAY, width= 40,padx=35, pady=5 ,height=40)
        l_up_btn_frame.pack(side='top', in_=l_frame)

        dcam_frame = Frame(window, background=COOLGRAY, width= 40, padx=5, pady=5, height=1, highlightcolor=SAGE)
        dcam_frame.pack(side='bottom', in_= l_up_btn_frame)
        dcam_label = Label(text="Drone Camera", fg=WHITE, bg=COOLGRAY)
        dcam_label.pack(in_=dcam_frame, side="top", anchor=W)

        face_frame = Frame(window, background=COOLGRAY, width= 40, padx=5, pady=5, height=1, highlightcolor=SAGE)
        face_frame.pack(side='bottom', in_= l_up_btn_frame)
        face_label = Label(text="Face Cam", fg=WHITE, bg=COOLGRAY)
        face_label.pack(in_=face_frame, side="top", anchor=W)

        l_lower_btn_frame = Frame(window, background=COOLGRAY, padx=35, pady=5, height=40)
        l_lower_btn_frame.pack(side='bottom', in_=l_frame)

        lift_frame= Frame(window, background=COOLGRAY, pady=10, height=40)
        lift_frame.grid(column=0, row=0, in_= l_lower_btn_frame)
        
        # l2_btn_frame = Frame(window, background= "#292929", width= 15, padx=5)
        # l2_btn_frame.pack(side='bottom', in_=l_frame)

        r_btn_frame = Frame(window, background= MONOBLACK, width= 30, padx=5)
        r_btn_frame.pack(side='right', fill=Y)

        low_scale_frame = Frame(window, background= MONOBLACK, height= 100, pady= 5)
        low_scale_frame.pack(side='bottom', fill= X)

        # Button to enable Blender
        blender_btn = Button(root, text="View in\nBlender", background=SAGE, height= 2, width=15)
        blender_btn.config(command=lambda: self.open_blender(blender_btn))

        # Shows the different measurments of the drone
        battery_label = Label(root, textvariable=battery_var, background=COOLGRAY,activebackground= "white", foreground=WHITE)
        height_label = Label(root, textvariable=height_var, background=COOLGRAY,activebackground= "white", foreground=WHITE)
        time_label = Label(root, textvariable=time_var, background=COOLGRAY,activebackground= "white", foreground=WHITE)
        temp_label = Label(root, textvariable=temperatur_var, background=COOLGRAY,activebackground= "white", foreground=WHITE)
        bar_label = Label(root, textvariable=barometer_var, background=COOLGRAY,activebackground= "white", foreground=WHITE)

        # Radiobuttons used to switch between controll modes, still not very pretty...
        xbox_btn = Radiobutton(root, text = "Xbox", variable = v, value = "1", indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        xbox_classic = Radiobutton(root, text = "Classic", variable = v, value = "5", indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        space_btn = Radiobutton(root, text= "Space Mouse", variable= v, value= "2", indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        face_btn = Radiobutton(root, text= "Face Tracking", variable= v, value= "3", indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        gest_btn = Radiobutton(root, text= "Gesture Tracking", variable= v, value= "4", indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore

        # Button to lift the Drone
        lift_off = Radiobutton(root, text= "Lift \noff", variable= fly_flag, value= 1, indicator = 0, background = SAGE, height=2, width= 7)   # type: ignore
        lift_on =  Radiobutton(root, text= "Land", variable= fly_flag, value= 0, indicator = 0, background = SAGE, height=2, width= 7)   # type: ignore

        # Turns the Facecam on
        camon_btn = Radiobutton(root, text = "On", variable = cam_state, value = "1", indicator = 0, background = SAGE, height=1, width= 7)         #type: ignore
        camoff_btn = Radiobutton(root, text = "Off", variable = cam_state, value = "0", indicator = 0, background = SAGE, height=1, width= 7)       #type: ignore

        #Turning the Drone Camera on
        streamon_btn = Radiobutton(root, text = "On", variable = drone_state, value = "1", indicator = 0, background = SAGE, height=1, width= 7)         #type: ignore
        streamoff_btn = Radiobutton(root, text = "Off", variable = drone_state, value = "0", indicator = 0, background = SAGE, height=1, width= 7)       #type: ignore
        # Different Buttons that are still unfinished
        btn_exit = Button(root, text="Exit", width=10, height=2, background= RED, command = lambda: self.total_annihilation(tello, root))       
        btn_con = Radiobutton(root, text = "On", variable = drone_var, value = 1, indicator = 0, background = SAGE, height=2, width= 15)       #type: ignore
        
        # Different Scales used to visualize Drone speed and Throttle controll
        throt_sca = Scale(window,activebackground=NUDE ,troughcolor=SAGE ,from_=100, to = 1, sliderlength = 50, length= 400, width= 25, variable = throt, bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, label="Throttle")

        speed_sca = Scale(window ,troughcolor=SAGE, from_=0, to = 20, sliderlength = 25, length= 300, width= 25,variable= speed_var ,orient='horizontal', bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, state='disabled', label="Speed")
        
        face_distance_sca = Scale(window, troughcolor=SAGE, from_=10, to = 70, sliderlength = 35, length= 185, width= 25,variable= face_distance_var, orient='horizontal' , bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, label='Tracking Distance')
        
        # Placing everything
        btn_con.pack(in_ = l_up_btn_frame, side='top', anchor=W)
        
        # Placing the Drone stats
        battery_label.pack(in_ = l_up_btn_frame, side='top', anchor=W)
        height_label.pack(in_ = l_up_btn_frame, side='top', anchor=W)
        time_label.pack(in_ = l_up_btn_frame, side='top', anchor=W)
        temp_label.pack(in_ = l_up_btn_frame, side='top', anchor=W)
        bar_label.pack(in_ = l_up_btn_frame, side='top', anchor=W)

        # Buttons fpr the Facecam
        camon_btn.pack(in_= face_frame, side='left', anchor=S)
        camoff_btn.pack(in_= face_frame, side='left', anchor=S)

        # Buttons for the Drone camera
        streamon_btn.pack(in_= dcam_frame, side='left', anchor=S)
        streamoff_btn.pack(in_= dcam_frame, side='left', anchor=S)

        # Lift Buttons
        lift_on.pack(in_= lift_frame, side='left')
        lift_off.pack(in_= lift_frame, side='left')

        # Controll options
        gest_btn.grid(column=0, row=1, in_= l_lower_btn_frame)
        face_btn.grid(column=0, row=2, in_= l_lower_btn_frame)
        space_btn.grid(column=0, row=3, in_= l_lower_btn_frame)
        xbox_classic.grid(column=0, row=4, in_= l_lower_btn_frame)
        xbox_btn.grid(column=0, row=5, in_= l_lower_btn_frame)



        btn_exit.pack(side='bottom', in_= r_btn_frame)

        blender_btn.pack(side='top', anchor=W, in_= r_btn_frame)

        # Scales for Stats and Adjustments
        throt_sca.pack(anchor=CENTER,side="right", in_ = r_btn_frame)

        speed_sca.pack(side='bottom', anchor=CENTER, in_= low_scale_frame)

        face_distance_sca.pack(side='bottom', in_= l_frame)
        # face_label = Label(text="Tracking \n Distance", fg=WHITE, bg=MONOBLACK, )
        # face_label.pack(side='right', in_= l_frame, ipady= 5)

        lmain.pack()

        print("buttons created")

class HandDetection():
    def __init__(self, mode=False, maxHands=2, modelComplexity = 1, detectionCon=float(0.3), trackCon=float(0.3)):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands           #type: ignore
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils    #type: ignore

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

    def tk_handflight(self, tello: Tello, cam, throt: int, controll_flag: bool):
        """Returns an Image with the Fingertracking overlay, turns on controlls if Controll_flag is true"""
        data, img = cam.read()
        img = cv2.cvtColor(cv2.flip(img,1),cv2.COLOR_BGR2RGB)
        img = self.tracking(img)
        lmlist = self.positions(img)
        if controll_flag == True:
            self.tellocontroll(tello, throt)
        return img

class FaceTracking():
    def resize(self, image, width, height):                #Smaller Picture
        """Adjusts the video stream to a specified size and  returns the interpolated image"""
        resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        return resized

    def gray(self, image):
        """Grays the imamge"""
        gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_frame

    def controlling(self, tello, faces, distance):
        """Sends controlls to the Drone"""
        width_middle = 300
        height_middle = 200
        face_reference = 80 - distance

        #yaw Abfrage
        controll_yaw = (faces[0][0]/width_middle)*100
        controll_yaw -= 100
        controll_yaw = round(controll_yaw)
        if controll_yaw <= 5 and controll_yaw >= -5:
            controll_yaw = 0

        #Height Abfrage
        controll_updown = (height_middle/faces[0][1])*100
        controll_updown -= 100
        controll_updown = round(controll_updown)
        if controll_updown >= 50:
            controll_updown = 50
        elif controll_updown <= -50:
            controll_updown = -50

        #front back Abfrage
        controll_frontback = (face_reference/faces[0][2])*100
        controll_frontback -= 100
        controll_frontback = round(controll_frontback)

        #Zusammenführung der Signale
        tello.send_rc_control(0, controll_frontback, controll_updown, controll_yaw)    

    def face_track_fly(self, tello: Tello, distance: int):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        while True:
            frame = tello.get_frame_read().frame
            frame = self.resize(frame, 960, 720)
            gray_image = self.gray(frame)
            detected_faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
            print(detected_faces)
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
            if len(detected_faces) != 0:
                self.controlling(tello, detected_faces, distance)
            else:
                tello.send_rc_control(0, 0, 0, 0)
            cv2.imshow("Detection", frame)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
            sleep(1/30)
    
    def tk_facetrack(self, tello: Tello, distance: int, cascade):
        frame = tello.get_frame_read().frame
        frame = self.resize(frame, 960, 720)
        gray_image = self.gray(frame)
        detected_faces = cascade.detectMultiScale(gray_image, 1.1, 4)
        print(detected_faces)
        for (x, y, w, h) in detected_faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
        if len(detected_faces) != 0:
            self.controlling(tello, detected_faces, distance)
        else:
            tello.send_rc_control(0, 0, 0, 0)
        cv2.imshow("Face Tracking", frame)
        # img = Image.fromarray(frame)    #type: ignore
        # imgtk = ImageTk.PhotoImage(image=img)
        # label.imgtk = imgtk     #type: ignore