from tkinter import *  # type: ignore
from tkinter import filedialog
from src.main import *
import pygame
from BlumiBird.player import Player
from BlumiBird.game import Game

class GUI_mate_org():
    """The Second Build of the Script, creates an UI and sets the controll methods of the Drone.
    To execute it, call "main(fps) and run the script"""

    def __init__(self):
        print("initialising UI")
        self.tello = Tello()
        self.joy = XboxController()
        self.space = Space_call()
        self.hand = HandDetection()
        self.face = FaceTracking()
        self.face_cascade = cv2.CascadeClassifier("src/haarcascade_frontalface_default.xml")

        self.gamer = Game()

        self.blender = "none"


        self.create_window()
        self.mate = ImageTk.PhotoImage(Image.open("Pictures/Logo.png"))     #type: ignore
        self.width, self.height = 1980, 1080

    def cam(self, label: Label, capture):    # Replaced by the new HandDetection class
        """Older version of the Hand Tracking developed by Calvin (and Google), label = placement as a label widget, cap = camera """
        lmain = label
        cap = capture

        image = cv2.cvtColor(cap,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)   # type: ignore
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk # type: ignore
        lmain.configure(image=imgtk)

    def blumi_setter(self):
        self.gameplay = True
    
    def blumibird_game(self):

        if self.game_init == False:
            print("Gamermode activated")
            self.gamer.init_game()
            self.game_init = True
        
        elif self.gamer.run == True:
            self.gamer.game_loop()
        
        elif self.gamer.run != True and self.game_init == True:
            pygame.quit()
            self.game_init = False
            self.gameplay = False


    def open_blender(self, button:Button):
        """Opens Blender and the Model of the Drone"""
        # Opens Blender
        myargs = [
        self.blender,     # File Path for the Blender Executable
        "-y",
        "Pictures/Dji-Tello.blend"        # The File Path for the Blend file
        ]
        if self.blender == "none":
            messagebox.showerror(title="No Blender Executable", message="You havent selected a Blender Executable")
    
        else:
            try:
                subprocess.Popen(myargs, stdin=subprocess.PIPE, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
                # button.configure(state='disabled')
            except:
                messagebox.showerror(title="Blender not Found", message="Check if you set the correct filepath for Blender\nChange it if necessary in the GUI.py file")

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

    def create_window(self):
        """creates the Tk window"""
        print("creating window")
        self.root = Tk()
        self.root['background'] = MONOBLACK
        self.root.wm_title("S_Mate Drohne")

        icon = ImageTk.PhotoImage(Image.open("Pictures/Icon.png"))      #type: ignore
        blume = Image.open("BlumiBird/assets/sprite_0.png")
        blume = blume.resize((25, 25), Image.ANTIALIAS)
        self.blume = ImageTk.PhotoImage(blume)
        
        self.root.iconphoto(False, icon)        #type: ignore
        self.assign_variables()
        self.create_labels()
        self.creating_widgets()
        self.placing_widgets()
        print("window created")

    def create_labels(self):
        """Placing necessary Labels for widget placements"""
        print("placing Labels")
        window = self.root
        self.lcam = Label(window, background=MONOBLACK)

        self.ldrone = Label(self.root)

        self.l_frame = Frame(window, background= MONOBLACK, width= 30, padx=5, height=40)
        self.l_frame.pack(side='left',fill=Y)

        self.l_up_btn_frame = Frame(window, background=COOLGRAY, width= 40,padx=35, pady=5 ,height=40)
        self.l_up_btn_frame.pack(side='top', in_=self.l_frame)

        self.dcam_frame = Frame(window, background=COOLGRAY, width= 40, padx=5, pady=5, height=1, highlightcolor=SAGE)
        self.dcam_frame.pack(side='bottom', in_= self.l_up_btn_frame)
        self.dcam_label = Label(text="Drone Camera", fg=WHITE, bg=COOLGRAY)
        self.dcam_label.pack(in_=self.dcam_frame, side="top", anchor=W)     

        self.face_frame = Frame(window, background=COOLGRAY, width= 40, padx=5, pady=5, height=1, highlightcolor=SAGE)
        self.face_frame.pack(side='bottom', in_= self.l_up_btn_frame)
        self.face_label = Label(text="Face Cam", fg=WHITE, bg=COOLGRAY)
        self.face_label.pack(in_= self.face_frame, side="top", anchor=W) 

        self.l_lower_btn_frame = Frame(window, background=COOLGRAY, padx=35, pady=5, height=40)
        self.l_lower_btn_frame.pack(side='bottom', in_= self.l_frame)

        self.lift_frame= Frame(window, background=COOLGRAY, pady=10, height=40)
        self.lift_frame.grid(column=0, row=0, in_= self.l_lower_btn_frame)   

        self.r_btn_frame = Frame(window, background= MONOBLACK, width= 30, padx=5)
        self.r_btn_frame.pack(side='right', fill=Y)

        self.low_scale_frame = Frame(window, background= MONOBLACK, height= 100, pady= 5)
        self.low_scale_frame.pack(side='bottom', fill= X) 
        self.lcam.pack()

        print("Labels placed")

    def assign_variables(self):
        """Sets up all the necessary Variables for the Programm"""
        print("assigning Variables")
        root = self.root
        self.cam_state = False

        self.drone_state = False
        self.faceflag = False

        self.facestream_flag = False
        self.dronestream_flag = False

        self.fly_flag = IntVar(root, 0)
        self.cont_var = IntVar(root, 0)
        self.fcam_var = IntVar(root, 0)
        self.dcam_var = IntVar(root, 0)
        self.throt_var = IntVar(root, 70)
        self.face_distance_var = IntVar(root, 20)
        # Variables used to read Drones Speed
        self.speed_var = IntVar(root, 0)

        self.drone_var = IntVar(root, 0)
        # Drone variables
        self.battery_var =    StringVar(root, f'Battery:     {0}%')
        self.height_var =     StringVar(root, f'Height:      {0} cm')
        self.time_var =       StringVar(root, f'Flight Time: {0} s')
        self.temperatur_var = StringVar(root, f'Drone Temp:  {0} °C')
        self.barometer_var =  StringVar(root, f'Barometer:   {0} cm')

        self.gesture_flag = False
        self.space_flag = False

        self.cam_direction = 0      # checks to see what cam is turned on for the drone
        self.helper = 0             # additional helper to check if the drone is flying
        self.countdown = 0          # Countdown to reduce drone load
        self.time_minutes = 0       # Variable to count flight minutes


        self.game_init = False
        self.gameplay = False
        print("variables assigned")

    def get_variables(self):
        """Used to get the necessary variables"""
        self.flight = self.fly_flag.get()
        self.controller = self.cont_var.get()
        self.facecam = self.fcam_var.get()
        self.dronecam = self.dcam_var.get()
        self.throttle = self.throt_var.get()
        self.distance = self.face_distance_var.get()

        self.connect_flag = self.drone_var.get()

    def drone_connect(self):
        """Connects to the drone and sets the connected Flag to True"""
        try:
            self.tello.connect()
            self.tello.streamon()
            self.drone_state = True
        
            # activating the Buttons after the Drone has been connected
            self.xbox_btn.configure(state='active')
            self.xbox_classic.configure(state='active')
            self.space_btn.configure(state='active')
            self.face_btn.configure(state='active')
            self.gest_btn.configure(state='active')

            self.lift_off.configure(state='active')
            self.lift_on.configure(state='active')

            self.streamoff_btn.configure(state='active')
            self.streamon_btn.configure(state='active')

            self.throt_sca.configure(state='active')
            self.face_distance_sca.configure(state='active')
        except:
            self.drone_var.set(0)
            messagebox.showerror(title="Drone Error", message="Couldnt Connect to the Drone, check if you're connected or restart the Drone")


    def dronestream(self):
        """creates a window showing the Drone camera 
        and turns on Facetracking if the flag has been set"""
        if self.dronecam == 1:
            if self.faceflag == True:
                # Checks if the Face Tracking window is opened
                self.cont_var.set(0)
                if cv2.getWindowProperty("Face Tracking", 0) >= 0:
                    cv2.destroyWindow("Face Tracking")

            frame = self.tello.get_frame_read().frame
            frame = cv2.resize(frame, (960, 720))

            cv2.imshow("Drone Stream", frame)

    def facetracking(self):
        """Turns Facetracking on, also closes the "Drone Stream" window if its opened"""
        if self.dronecam == 1:
            try:
                if cv2.getWindowProperty("Drone Stream", 0) >= 0:
                    cv2.destroyWindow("Drone Stream")
            except:
                pass
            self.dcam_var.set(0)
        else:             
            print("Facetracking is on")
            frame = self.tello.get_frame_read().frame
            frame = self.face.resize(frame, 960, 720)
            gray_image = self.face.gray(frame)
            detected_faces = self.face_cascade.detectMultiScale(gray_image, 1.1, 4)
            print(detected_faces)
            for (x, y, w, h) in detected_faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))
            if len(detected_faces) != 0:
                self.face.controlling(self.tello, detected_faces, self.distance)
            else:
                self.tello.send_rc_control(0, 0, 0, 0)
            cv2.imshow("Face Tracking", frame)

    def select_blender_exe(self):
        """used to specify the Blender executable"""
        print("Selectin Blender")
        self.blender = filedialog.askopenfilename(defaultextension = ".exe",filetypes = (("Executable Files", "*.exe"),("All Files", "*.*")))

        if len(self.blender) and self.blender[-4:] != ".exe":
            messagebox.showinfo(message = "Incompatible file format", title = "ERROR")
        
        else:
            print(self.blender)

    def creating_widgets(self):
        """Creating necessary Widgets, shouldnt be called individually"""
        print("creating Widgets")
        root = self.root
        # Drone Stats
        self.battery_label = Label(root, textvariable= self.battery_var, background= COOLGRAY,activebackground= "white", foreground= WHITE)
        self.height_label = Label(root, textvariable= self.height_var, background= COOLGRAY,activebackground= "white", foreground= WHITE)
        self.time_label = Label(root, textvariable= self.time_var, background= COOLGRAY,activebackground= "white", foreground= WHITE)
        self.temp_label = Label(root, textvariable= self.temperatur_var, background= COOLGRAY,activebackground= "white", foreground= WHITE)
        self.bar_label = Label(root, textvariable= self.barometer_var, background= COOLGRAY,activebackground= "white", foreground= WHITE)

        self.blender_btn = Button(root, text="View in\nBlender", background=SAGE, height= 2, width=15)
        self.blender_btn.config(command=lambda: self.open_blender(self.blender_btn))

        self.select_blender = Button(root, text="Select Blender", command=lambda: self.select_blender_exe(), background=SAGE, height= 2, width=15)
        # self.select_blend = Button(root, text="Select File", command=lambda: self.select_file(), background=SAGE, height= 2, width=15)

        self.blumi_but = Button(root, image=self.blume, background=SAGE, pady=5, padx=5, command=lambda: self.blumi_setter())

        # Radiobuttons used to switch between controll modes, still not very pretty...
        self.xbox_btn = Radiobutton(root, text = "Xbox", variable = self.cont_var, value = 1, indicator = 0, background = SAGE, height=1, width= 15, state='disabled')   # type: ignore
        self.xbox_classic = Radiobutton(root, text = "Classic", variable = self.cont_var, value = 5, indicator = 0, background = SAGE, height=1, width= 15, state='disabled')   # type: ignore
        self.space_btn = Radiobutton(root, text= "Space Mouse", variable= self.cont_var, value= 2, indicator = 0, background = SAGE, height=1, width= 15, state='disabled')   # type: ignore
        self.face_btn = Radiobutton(root, text= "Face Tracking", variable= self.cont_var, value = 3, indicator = 0, background = SAGE, height=1, width= 15, state='disabled')   # type: ignore
        self.gest_btn = Radiobutton(root, text= "Gesture Tracking", variable= self.cont_var, value = 4, indicator = 0, background = SAGE, height=1, width= 15, state='disabled')   # type: ignore

        # Button to lift the Drone
        self.lift_off = Radiobutton(root, text= "Lift \noff", variable= self.fly_flag, value= 1, indicator = 0, background = SAGE, height=2, width= 7, state='disabled')   # type: ignore
        self.lift_on =  Radiobutton(root, text= "Land", variable= self.fly_flag, value= 0, indicator = 0, background = SAGE, height=2, width= 7, state='disabled')   # type: ignore

        # Turns the Facecam on
        self.camon_btn = Radiobutton(root, text = "On", variable = self.fcam_var, value = 1, indicator = 0, background = SAGE, height=1, width= 7)         #type: ignore
        self.camoff_btn = Radiobutton(root, text = "Off", variable = self.fcam_var, value = 0, indicator = 0, background = SAGE, height=1, width= 7)       #type: ignore

        #Turning the Drone Camera on
        self.streamon_btn = Radiobutton(root, text = "On", variable = self.dcam_var, value = "1", indicator = 0, background = SAGE, height=1, width= 7, state='disabled')         #type: ignore
        self.streamoff_btn = Radiobutton(root, text = "Off", variable = self.dcam_var, value = "0", indicator = 0, background = SAGE, height=1, width= 7, state='disabled')       #type: ignore
        # Different Buttons that are still unfinished
        self.btn_exit = Button(root, text="Exit", width=10, height=2, background= RED, command = lambda: self.total_annihilation(self.tello, root))       
        self.btn_con = Radiobutton(root, text = "On", variable = self.drone_var, value = 1, indicator = 0, background = SAGE, height=2, width= 15)       #type: ignore
        
        # Different Scales used to visualize Drone speed and Throttle controll
        self.throt_sca = Scale(root,activebackground=NUDE ,troughcolor=SAGE ,from_=100, to = 1, sliderlength = 50, length= 400, width= 25, variable = self.throt_var, bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, label="Throttle", state='disabled')

        self.speed_sca = Scale(root ,troughcolor=SAGE, from_=0, to = 20, sliderlength = 25, length= 300, width= 25,variable= self.speed_var ,orient='horizontal', bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, state='disabled', label="Speed")
        
        self.face_distance_sca = Scale(root, troughcolor=SAGE, from_=10, to = 70, sliderlength = 35, length= 185, width= 25,variable= self.face_distance_var, orient='horizontal' , bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, label='Tracking Distance', state='disabled')
        print("Widgets created")

    def placing_widgets(self):
        """Placing created widgets"""
        print("placing Widgets")
        # Placing everything
        self.btn_con.pack(in_ = self.l_up_btn_frame, side='top', anchor=W)
        
        # Placing the Drone stats
        self.battery_label.pack(in_ = self.l_up_btn_frame, side='top', anchor=W)
        self.height_label.pack(in_ = self.l_up_btn_frame, side='top', anchor=W)
        self.time_label.pack(in_ = self.l_up_btn_frame, side='top', anchor=W)
        self.temp_label.pack(in_ = self.l_up_btn_frame, side='top', anchor=W)
        self.bar_label.pack(in_ = self.l_up_btn_frame, side='top', anchor=W)

        # Buttons fpr the Facecam
        self.camon_btn.pack(in_= self.face_frame, side='left', anchor=S)
        self.camoff_btn.pack(in_= self.face_frame, side='left', anchor=S)

        # Buttons for the Drone camera
        self.streamon_btn.pack(in_= self.dcam_frame, side='left', anchor=S)
        self.streamoff_btn.pack(in_= self.dcam_frame, side='left', anchor=S)

        # Lift Buttons
        self.lift_on.pack(in_= self.lift_frame, side='left')
        self.lift_off.pack(in_= self.lift_frame, side='left')

        # Controll options
        self.gest_btn.grid(column=0, row=1, in_= self.l_lower_btn_frame)
        self.face_btn.grid(column=0, row=2, in_= self.l_lower_btn_frame)
        self.space_btn.grid(column=0, row=3, in_= self.l_lower_btn_frame)
        self.xbox_classic.grid(column=0, row=4, in_= self.l_lower_btn_frame)
        self.xbox_btn.grid(column=0, row=5, in_= self.l_lower_btn_frame)

        # Exit Button
        self.btn_exit.pack(side='bottom', in_= self.r_btn_frame)
        # Button for opening Blender
        self.blender_btn.pack(side='top', anchor=W, in_= self.r_btn_frame)
        self.select_blender.pack(side='top', anchor=W, in_= self.r_btn_frame)
        # self.select_blend.pack(side='top', anchor=W, in_= self.r_btn_frame)

        # Scales for Stats and Adjustments
        self.throt_sca.pack(anchor=CENTER,side="right", in_ = self.r_btn_frame)

        self.speed_sca.pack(side='bottom', anchor=CENTER, in_= self.low_scale_frame)

        self.blumi_but.pack(side= 'top', in_= self.l_frame)

        self.face_distance_sca.pack(side='bottom', in_= self.l_frame)
        print("Widgets placed")

    def drone_rotation(self):
        """Writing drone rotation to a txt which gets read with Blender"""
        # print("getting drone rotation")
        pitch = self.tello.get_pitch()
        roll = self.tello.get_roll()
        yaw = self.tello.get_yaw()

        with open("Pictures/drone_data.txt", "w") as txt:
            txt.write(f'{pitch},{roll},{yaw}')

    def get_drone_speed(self, tello:Tello,) -> int:
        """Gets the current speed of the drone"""
        x_speed = tello.get_speed_x()
        y_speed = tello.get_speed_y()
        z_speed = tello.get_speed_z()

        if x_speed >= y_speed and x_speed >= z_speed:
            return x_speed
        elif y_speed >= x_speed and y_speed >= z_speed:
            return y_speed
        else:
            return z_speed

    def get_flight_time(self):
        """calls current flight time and rounds them up to minutes"""
        self.time = self.tello.get_flight_time()
        if self.time >= 120:
            self.time_minutes = self.time//60
            self.time_second = self.time - 60*self.time_minutes
            self.time_var.set(f'Flight Time: {self.time_minutes} min  {self.time_second} s')
        else:
            self.time_var.set(f'Flight Time: {self.time} s')

    def landing_widget(self):
        """Helps to determine if the Drone is currently flying"""
        if self.flight == 1:
            try:
                if self.helper == 0:
                    self.tello.takeoff()
                    self.helper = 1
            except:
                self.fly_flag.set(0)

        if self.flight == 0:
            try:
                if self.helper == 1:
                    self.tello.land()
                    self.helper = 0
            except:
                self.helper = 0

    def drone_info(self):
        """Reads out the Drones Information"""
        # print("reading info")

        if self.countdown % 2 == 0:
            self.drone_rotation()

        if self.countdown >= 10:
            self.speed_var.set(self.get_drone_speed(self.tello))    
            self.get_flight_time()
            self.battery_var.set(f'Battery:     {self.tello.get_battery()}%')
            self.height_var.set(f'Height:      {self.tello.get_height()} cm')
            self.temperatur_var.set(f'Drone Temp:  {self.tello.get_temperature()} °C')
            self.barometer_var.set(f'Barometer:   {int(self.tello.get_barometer())} cm')
            self.countdown = 0
        self.countdown += 1

    def xbox(self, var):
        """Xbox controlls for the Drone"""
        try:
            try:
                if var == 1:
                    self.throttle = self.joy.define_speed_xbox(self.throttle)
                    self.helper, self.cam_direction = self.joy.flight_xbox(self.tello, self.helper, self.throttle, self.cam_direction)   
            
                elif var == 5:
                    self.throttle = self.joy.define_speed_classic(self.throttle)
                    self.helper, self.cam_directio = self.joy.flight_xbox_classic(self.tello, self.helper, self.throttle, self.cam_direction)   
            
            except:
                self.cont_var.set(0)
                messagebox.showerror(title="Controller Error", message="The drone doesnt seem to be connected")
        except:
            self.cont_var.set(0)
            print("couldnt send command")
            messagebox.showerror(title="Controller Error", message="Couldnt Procced with controll Method \nCheck if your Xbox Controller is properly connected")  

    def spacemouse(self):
        """3D Spacemouse controlls for the Drone"""
        try:
            if self.space_flag == False:
                dev = self.space.open(callback=None, button_callback=self.space.toggle_led)
                self.space_flag = True
            elif self.space_flag == True:
                self.helper = self.space.flight(self.tello, self.helper, self.throttle)
        except:
            self.cont_var.set(0)
            messagebox.showerror(title="Spacemouse Error", message="Couldnt Procced with controll Method \nCheck if your Spacemouse is properly connected")

    def controlls(self):
        """Switches between different controll methods"""
        self.throt_var.set(self.throttle)

        if self.controller == 1:
            self.xbox(1)
        
        elif self.controller == 5:
            self.xbox(5)
        
        elif self.controller == 2:
            self.spacemouse()
        
        elif self.controller == 3:
            if self.faceflag == False:
                self.faceflag = True
            self.facetracking()

        elif self.controller == 4:
            self.gesture_flag = True
            if self.facecam != 1:
                self.fcam_var.set(1)

        if self.controller != 3 and self.faceflag == True:    
            self.faceflag = False

        if self.controller != 4 and self.gesture_flag == True:
            self.gesture_flag = False
        
    def main_label(self):
        """Either sets up the camera or displayes the main logo"""
        if self.facecam == 1:
            if self.cam_state == False:
                print('Init cap...')
                self.cap = cv2.VideoCapture(0)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                print('Cap initialized!') 
                self.cam_state = True  
            elif self.gesture_flag == False:         
                img = self.hand.tk_handflight(self.tello, self.cap, self.throttle, False)       #type: ignore
                self.cam(self.lcam, img)
            
            elif self.gesture_flag == True:
                img = self.hand.tk_handflight(self.tello, self.cap, self.throttle, True)
                print("controlls should work")
                self.cam(self.lcam, img)
        
        elif self.facecam == 0:
            self.lcam.configure(image=self.mate)

    def main(self, framerate: int):
        """Starting the Loop, framerate can be adjusted, but puts more strain on the drone"""
        print("starting loop")
        root = self.root
        root.update()
        while True:
            if self.gameplay == True:
                self.blumibird_game()
            # print("Variabels")
            self.get_variables()
            if root.state() != 'normal' and root.state() != 'zoomed' and root.state() != 'withdrawn' and root.state() != 'iconic':
                print("closing windows")
                self.total_annihilation(self.tello, root)
                break
            self.main_label()
            # print("connect check")
            if self.connect_flag == 1:
                if self.drone_state == False:
                    self.drone_connect()
            # print("drone check")
            if self.drone_state == True:
                self.landing_widget()
                self.drone_info()
                self.dronestream()
                self.controlls()
            # print("update")
            root.update()
            sleep(1/framerate)
            
if __name__ == "__main__":
    mate = GUI_mate_org()
    mate.main(60)