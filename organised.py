from tkinter import *  # type: ignore
from src.main import *

class GUI_mate_org():

    def __init__(self):
        print("initialising UI")
        self.tello = Tello()
        self.joy = XboxController()
        self.space = Space_call()
        self.hand = HandDetection()
        self.face = FaceTracking()
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        self.mate = ImageTk.PhotoImage(Image.open("Pictures/Logo.png")) 
        self.create_window()

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

        icon = ImageTk.PhotoImage(Image.open("Pictures/Icon.png"))
        self.root.iconphoto(False, icon)
        self.assign_variables()
        self.creating_widgets()
        self.placing_widgets()
        print("window created")

    def create_labels(self):
        """Placing necessary Labels for widget placements"""
        print("placing Labels")
        window = self.root
        self.lcam = Label(self.root)
        self.lcam.pack()
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
          
        print("Labels placed")

    def assign_variables(self):
        """Sets up all the necessary Variables for the Programm"""
        print("assigning Variables")
        root = self.root
        self.drone_state = False

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
        self.tello.connect()
        self.tello.streamon()
        self.drone_state = True

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

        # Radiobuttons used to switch between controll modes, still not very pretty...
        self.xbox_btn = Radiobutton(root, text = "Xbox", variable = self.cont_var, value = 1, indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        self.xbox_classic = Radiobutton(root, text = "Classic", variable = self.cont_var, value = 5, indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        self.space_btn = Radiobutton(root, text= "Space Mouse", variable= self.cont_var, value= 2, indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        self.face_btn = Radiobutton(root, text= "Face Tracking", variable= self.cont_var, value = 3, indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore
        self.gest_btn = Radiobutton(root, text= "Gesture Tracking", variable= self.cont_var, value = 4, indicator = 0, background = SAGE, height=1, width= 15)   # type: ignore

        # Button to lift the Drone
        self.lift_off = Radiobutton(root, text= "Lift \noff", variable= self.fly_flag, value= 1, indicator = 0, background = SAGE, height=2, width= 7)   # type: ignore
        self.lift_on =  Radiobutton(root, text= "Land", variable= self.fly_flag, value= 0, indicator = 0, background = SAGE, height=2, width= 7)   # type: ignore

        # Turns the Facecam on
        self.camon_btn = Radiobutton(root, text = "On", variable = self.fcam_var, value = 1, indicator = 0, background = SAGE, height=1, width= 7)         #type: ignore
        self.camoff_btn = Radiobutton(root, text = "Off", variable = self.fcam_var, value = 0, indicator = 0, background = SAGE, height=1, width= 7)       #type: ignore

        #Turning the Drone Camera on
        self.streamon_btn = Radiobutton(root, text = "On", variable = self.dcam_var, value = "1", indicator = 0, background = SAGE, height=1, width= 7)         #type: ignore
        self.streamoff_btn = Radiobutton(root, text = "Off", variable = self.dcam_var, value = "0", indicator = 0, background = SAGE, height=1, width= 7)       #type: ignore
        # Different Buttons that are still unfinished
        self.btn_exit = Button(root, text="Exit", width=10, height=2, background= RED, command = lambda: self.total_annihilation(self.tello, root))       
        self.btn_con = Radiobutton(root, text = "On", variable = self.drone_var, value = 1, indicator = 0, background = SAGE, height=2, width= 15)       #type: ignore
        
        # Different Scales used to visualize Drone speed and Throttle controll
        self.throt_sca = Scale(root,activebackground=NUDE ,troughcolor=SAGE ,from_=100, to = 1, sliderlength = 50, length= 400, width= 25, variable = self.throt_var, bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, label="Throttle")

        self.speed_sca = Scale(root ,troughcolor=SAGE, from_=0, to = 20, sliderlength = 25, length= 300, width= 25,variable= self.speed_var ,orient='horizontal', bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, state='disabled', label="Speed")
        
        self.face_distance_sca = Scale(root, troughcolor=SAGE, from_=10, to = 70, sliderlength = 35, length= 185, width= 25,variable= self.face_distance_var, orient='horizontal' , bg= MONOBLACK, foreground=WHITE, highlightbackground= SAGE, label='Tracking Distance')
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

        # Scales for Stats and Adjustments
        self.throt_sca.pack(anchor=CENTER,side="right", in_ = self.r_btn_frame)

        self.speed_sca.pack(side='bottom', anchor=CENTER, in_= self.low_scale_frame)

        self.face_distance_sca.pack(side='bottom', in_= self.l_frame)
        print("Widgets placed")

    def drone_rotation(self):
        """Writing drone rotation to a txt which gets read with Blender"""
        print("getting drone rotation")
        pitch = self.tello.get_pitch()
        roll = self.tello.get_roll()
        yaw = self.tello.get_yaw()

        with open("drone_data.txt", "w") as txt:
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
        print("reading info")

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

    def xbox(self, var):
        try:
            try:
                if var == 1:
                    self.helper, self.cam_direction, self.throttle = self.joy.flight_xbox(self.tello, self.helper, self.throttle, self.cam_direction)   
            
                elif var == 5:
                    self.helper, self.cam_direction, self.throttle = self.joy.flight_xbox_classic(self.tello, self.helper, self.throttle, self.cam_direction)   
            
            except:
                self.cont_var.set(0)
                messagebox.showerror(title="Controller Error", message="The drone doesnt seem to be connected")
        except:
            self.cont_var.set(0)
            print("couldnt send command")
            messagebox.showerror(title="Controller Error", message="Couldnt Procced with controll Method \nCheck if your Xbox Controller is properly connected")  

    def spacemouse(self):
        try:
            if self.space_flag == False:
                dev = self.space.open(callback=None, button_callback=self.space.toggle_led)
                self.space_flag = True
            elif self.space_flag == True:
                self.helper = self.space.flight(self.tello, self.helper)
        except:
            self.cont_var.set(0)
            messagebox.showerror(title="Spacemouse Error", message="Couldnt Procced with controll Method \nCheck if your Spacemouse is properly connected")

    def face_track(self):
        self.face.tk_facetrack(self.tello, self.distance, self.face_cascade) 

    def controlls(self):
        self.throt_var.set(self.throttle)

        if self.controller == 1:
            self.xbox(1)
        elif self.controller == 5:
            self.xbox(5)
        
        elif self.controller == 2:
            self.spacemouse()
        
        elif self.controller == 3:
            print("not done")
    def main(self):
        print("starting loop")
        root = self.root
        while True:
            self.get_variables()
            if root.state() != 'normal':
                self.total_annihilation(self.tello, root)
                break

            if self.connect_flag == 1:
                if self.drone_state == False:
                    self.drone_connect()
            
            if self.drone_state == True:
                self.landing_widget()
                self.drone_info()
 